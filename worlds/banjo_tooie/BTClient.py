import asyncio
import json
import os
import multiprocessing
import copy
import subprocess
from typing import Union
import zipfile
from asyncio import StreamReader, StreamWriter

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
from Utils import async_start
from worlds import network_data_package

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart banjoTooie_connector.lua"
CONNECTION_REFUSED_STATUS = "Connection refused. Please start your emulator and make sure banjoTooie_connector.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart banjoTooie_connector.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

"""
Payload: lua -> client
{
    playerName: string,
    locations: dict,
    deathlinkActive: bool,
    isDead: bool,
    gameComplete: bool
}

Payload: client -> lua
{
    items: list,
    playerNames: list,
    triggerDeath: bool,
    messages: string
}

Deathlink logic:
"Dead" is true <-> Banjo is at 0 hp.

deathlink_pending: we need to kill the player
deathlink_sent_this_death: we interacted with the multiworld on this death, waiting to reset with living link

"""

bt_loc_name_to_id = network_data_package["games"]["Banjo-Tooie"]["location_name_to_id"]
bt_itm_name_to_id = network_data_package["games"]["Banjo-Tooie"]["item_name_to_id"]

script_version: int = 4

def get_item_value(ap_id):
    return ap_id


class BanjoTooieCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx): 
        super().__init__(ctx)

    def _cmd_n64(self):
        """Check N64 Connection State"""
        if isinstance(self.ctx, BanjoTooieContext):
            logger.info(f"N64 Status: {self.ctx.n64_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, BanjoTooieContext):
            self.ctx.deathlink_client_override = True
            self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
            async_start(self.ctx.update_death_link(self.ctx.deathlink_enabled), name="Update Deathlink")


class BanjoTooieContext(CommonContext):
    command_processor = BanjoTooieCommandProcessor
    items_handling = 0b111 #full

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = 'Banjo-Tooie'
        self.n64_streams: (StreamReader, StreamWriter) = None # type: ignore
        self.n64_sync_task = None
        self.n64_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.location_table = {}
        self.movelist_table = {}
        self.cheatorewardslist_table = {}
        self.honeybrewardslist_table = {}
        self.notelist_table = {}
        self.stationlist_table = {}
        self.jinjofamlist_table = {}
        self.worldlist_table = {}
        self.chuffy_table = {}
        self.mystery_table = {}
        self.roystenlist_table = {}
        self.jiggychunks_table = {}
        self.goggles_table = False
        self.foodstall_table = {}
        self.deathlink_enabled = False
        self.deathlink_pending = False
        self.deathlink_sent_this_death = False
        self.deathlink_client_override = False
        self.version_warning = False
        self.messages = {}
        self.slot_data = {}
        self.sendSlot = False
        self.sync_ready = False
        self.startup = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BanjoTooieContext, self).server_auth(password_requested)
        if not self.auth:
            await self.get_username()
            await self.send_connect()
            self.awaiting_rom = True
            return
        return

    def _set_message(self, msg: str, msg_id: Union[int, None]):
        if msg_id == None:
            self.messages.update({len(self.messages)+1: msg })
        else:
            self.messages.update({msg_id:msg})

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    def run_gui(self):
        from kvui import GameManager

        class BanjoTooieManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Banjo-Tooie Client"

        self.ui = BanjoTooieManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd, args):
        if cmd == 'Connected':
            self.slot_data = args.get('slot_data', None)
            self.deathlink_enabled = self.slot_data["deathlink"]
            logger.info("Please open Banjo-Tooie and load banjo_tooie_connector.lua")
            self.n64_sync_task = asyncio.create_task(n64_sync_task(self), name="N64 Sync")
        elif cmd == 'Print':
            msg = args['text']
            if ': !' not in msg:
                self._set_message(msg, SYSTEM_MESSAGE_ID)
        elif cmd == "ReceivedItems":
            if self.startup == False:
                for item in args["items"]:
                    player = ""
                    item_name = ""
                    for (i, name) in self.player_names.items():
                        if i == item.player:
                            player = name
                            break
                    for (name, i) in bt_itm_name_to_id.items():
                        if item.item == i:
                            item_name = name
                            break                    
                    logger.info(player + " sent " + item_name)
                logger.info("The above items will be sent when Banjo-Tooie is loaded.")
                self.startup = True

    def on_print_json(self, args: dict):
        if self.ui:
            self.ui.print_json(copy.deepcopy(args["data"]))
            relevant = args.get("type", None) in {"Hint", "ItemSend"}
            if relevant:
                relevant = False
                item = args["item"]
                if self.slot_concerns_self(args["receiving"]):
                    relevant = True 
                elif self.slot_concerns_self(item.player):
                    relevant = True

                if relevant == True:
                    msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                    self._set_message(msg, None)
        else:
            text = self.jsontotextparser(copy.deepcopy(args["data"]))
            logger.info(text)
            relevant = args.get("type", None) in {"Hint", "ItemSend"}
            if relevant:
                msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                self._set_message(msg, None)

        # if relevant:
        #     getitem = False
        #     item = args["item"]
        #     # found in this world
        #     if self.slot_concerns_self(args["receiving"]):
        #         relevant = True 
        #         if args.get("type", None) != "Hint":    
        #             getitem = True
        #     # goes in this world
        #     elif self.slot_concerns_self(item.player):
        #         relevant = True
        #     # not related
        #     else:
        #         relevant = False
        #         item = args["item"]
        #         if getitem:
        #             self.items_received.append(item)



def get_payload(ctx: BanjoTooieContext):
    if ctx.deathlink_enabled and ctx.deathlink_pending:
        trigger_death = True
        ctx.deathlink_sent_this_death = True
        ctx.deathlink_pending = False
    else:
        trigger_death = False

    # if(len(ctx.items_received) > 0) and ctx.sync_ready == True:
    #   print("Receiving Item")

    if ctx.sync_ready == True:
        ctx.startup = True
        payload = json.dumps({
                "items": [get_item_value(item.item) for item in ctx.items_received],
                "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
                "triggerDeath": trigger_death,
                "messages": [message for (i, message) in ctx.messages.items() if i != 0],
            })
    else:
        payload = json.dumps({
                "items": [],
                "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
                "triggerDeath": trigger_death,
                "messages": [message for (i, message) in ctx.messages.items() if i != 0],
            })
    if len(ctx.messages) > 0:
        ctx.messages = {}

    # if len(ctx.items_received) > 0 and ctx.sync_ready == True:
    #     ctx.items_received = []

    return payload

def get_slot_payload(ctx: BanjoTooieContext):
    payload = json.dumps({
            "slot_player": ctx.slot_data["player_name"],
            "slot_seed": ctx.slot_data["seed"],
            "slot_deathlink": ctx.deathlink_enabled,
            "slot_disable_text": ctx.slot_data["disable_text"],
            "slot_skip_tot": ctx.slot_data["skip_tot"],
            "slot_honeycomb": ctx.slot_data["honeycomb"],
            "slot_pages": ctx.slot_data["pages"],
            "slot_moves": ctx.slot_data["moves"],
            "slot_bkmoves": ctx.slot_data["bk_moves"],
            "slot_cheatorewards": ctx.slot_data["cheato_rewards"],
            "slot_honeybrewards": ctx.slot_data["honeyb_rewards"],
            "slot_doubloon": ctx.slot_data["doubloons"],
            "slot_minigames": ctx.slot_data["minigames"],
            "slot_treble": ctx.slot_data["trebleclef"],
            "slot_skip_puzzles": ctx.slot_data["skip_puzzles"],
            "slot_open_hag1": ctx.slot_data["open_hag1"],
            "slot_stations": ctx.slot_data["stations"],
            "slot_chuffy": ctx.slot_data["chuffy"],
            "slot_jinjo": ctx.slot_data["jinjo"],
            "slot_notes": ctx.slot_data["notes"],
            "slot_mystery": ctx.slot_data["mystery"],
            "slot_worlds": ctx.slot_data["worlds"],
            "slot_world_order": ctx.slot_data["world_order"],
            "slot_keys": ctx.slot_data['world_keys'],
            "slot_skip_klungo": ctx.slot_data["skip_klungo"],
            "slot_skip_king": ctx.slot_data["skip_king"],
            "slot_goal_type": ctx.slot_data["goal_type"],
            "slot_minigame_hunt_length": ctx.slot_data["minigame_hunt_length"],
            "slot_boss_hunt_length": ctx.slot_data["boss_hunt_length"],
            "slot_jinjo_family_rescue_length": ctx.slot_data["jinjo_family_rescue_length"],
            "slot_token_hunt_length": ctx.slot_data["token_hunt_length"]
        })
    ctx.sendSlot = False
    return payload


async def parse_payload(payload: dict, ctx: BanjoTooieContext, force: bool):

    # Refuse to do anything if ROM is detected as changed
    if ctx.auth and payload['playerName'] != ctx.auth:
        logger.warning("ROM change detected. Disconnecting and reconnecting...")
        ctx.deathlink_enabled = False
        ctx.deathlink_client_override = False
        ctx.finished_game = False
        ctx.location_table = {}
        ctx.chuffy_table = {}
        ctx.movelist_table = {}
        ctx.deathlink_pending = False
        ctx.deathlink_sent_this_death = False
        ctx.auth = payload['playerName']
        await ctx.send_connect()
        return

    # Turn on deathlink if it is on, and if the client hasn't overriden it
    if payload['deathlinkActive'] and ctx.deathlink_enabled and not ctx.deathlink_client_override:
        await ctx.update_death_link(True)
        ctx.deathlink_enabled = True

    # Locations handling
    locations = payload['locations']
    chuffy = payload['chuffy']
    notelist = payload['treble']
    stationlist = payload['stations']
    mystery = payload['mystery']
    roystenlist = payload['roysten']
    jinjofamlist = payload['jinjofam']
    cheatorewardslist = payload['cheato_rewards']
    honeybrewardslist = payload['honeyb_rewards']
    jiggychunklist = payload['jiggy_chunks']
    goggles = payload['goggles']
    food_stalls = payload['food_stalls']

    worldslist = payload['worlds']

    # The Lua JSON library serializes an empty table into a list instead of a dict. Verify types for safety:
    if isinstance(locations, list):
        locations = {}
    if isinstance(chuffy, list):
        chuffy = {}
    if isinstance(notelist, list):
        notelist = {}
    if isinstance(stationlist, list):
        stationlist = {}
    if isinstance(mystery, list):
        mystery = {}
    if isinstance(roystenlist, list):
        roystenlist = {}
    if isinstance(jinjofamlist, list):
        jinjofamlist = {}
    if isinstance(cheatorewardslist, list):
        cheatorewardslist = {}
    if isinstance(honeybrewardslist, list):
        honeybrewardslist = {}
    if isinstance(jiggychunklist, list):
        jiggychunklist = {}
    if isinstance(worldslist, list):
        worldslist = {}
    if isinstance(food_stalls, list):
        food_stalls = {}
    if isinstance(goggles, bool) == False:
        goggles = False

    if "DEMO" not in locations and ctx.sync_ready == True:
        locs1 = []
        if ctx.location_table != locations: 
            for item_group, BTlocation_table in locations.items():
                    if len(BTlocation_table) == 0:
                        continue

                    # Game completion handling
                    if (("1230027" in BTlocation_table and BTlocation_table["1230027"] == True) 
                    and (ctx.slot_data["goal_type"] == 0 or ctx.slot_data["goal_type"] == 4) and not ctx.finished_game):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": 30
                        }])
                        ctx.finished_game = True

                    else:
                        for locationId, value in BTlocation_table.items():
                            if value == True:
                                if (locationId == "1230676" or locationId == "1230677" or locationId == "1230678" or
                                    locationId == "1230679" or locationId == "1230680" or locationId == "1230681" or
                                    locationId == "1230682" or locationId == "1230683" or locationId == "1230684") \
                                    and ctx.slot_data["jinjo"] == "true":
                                    continue
                                if locationId not in ctx.location_table:
                                    locs1.append(int(locationId))
                                    if ctx.slot_data["goal_type"] == 1 or ctx.slot_data["goal_type"] == 2 or \
                                    ctx.slot_data["goal_type"] == 3 or ctx.slot_data["goal_type"] == 4:
                                       locs1 = mumbo_tokens_loc(locs1, int(locationId), ctx.slot_data["goal_type"])
                                   
            ctx.location_table = locations       
        if ctx.chuffy_table != chuffy:
            ctx.chuffy_table = chuffy
            for locationId, value in chuffy.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.notelist_table != notelist:
            ctx.notelist_table = notelist
            for locationId, value in notelist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.stationlist_table != stationlist:
            ctx.stationlist_table = stationlist
            for locationId, value in stationlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.mystery_table != mystery:
            ctx.mystery_table = mystery
            for locationId, value in mystery.items():
                if locationId == "REMOVE": #Don't need to handle this here
                    continue
                if value == True:
                    locs1.append(int(locationId))
        if ctx.roystenlist_table != roystenlist:
            ctx.roystenlist_table = roystenlist
            for locationId, value in roystenlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.jiggychunks_table != jiggychunklist:
            ctx.jiggychunks_table = jiggychunklist
            for locationId, value in jiggychunklist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.goggles_table != goggles:
            ctx.goggles_table = goggles
            if goggles == True:
                locs1.append(1231005)
        if ctx.foodstall_table != food_stalls:
            ctx.foodstall_table = food_stalls
            for locationId, value in food_stalls.items():
                if value == True:
                    locs1.append(int(locationId))

        if ctx.slot_data["moves"] == "true":
            # Locations handling
            movelist = payload['unlocked_moves']
            # The Lua JSON library serializes an empty table into a list instead of a dict. Verify types for safety:
            if isinstance(movelist, list):
                movelist = {}

            if ctx.movelist_table != movelist:
                ctx.movelist_table = movelist

                for locationId, value in movelist.items():
                    if value == True:
                        locs1.append(int(locationId))
        if ctx.slot_data["jinjo"] == "true":
            if ctx.jinjofamlist_table != jinjofamlist:
                ctx.jinjofamlist_table = jinjofamlist
                for locationId, value in jinjofamlist.items():
                    if value == True:
                        locs1.append(int(locationId))
                        if ctx.slot_data["goal_type"] == 3 or ctx.slot_data["goal_type"] == 4:
                            locs1 = mumbo_tokens_loc(locs1, int(locationId), ctx.slot_data["goal_type"])
        if ctx.slot_data["cheato_rewards"] == "true":
            if ctx.cheatorewardslist_table != cheatorewardslist:
                ctx.cheatorewardslist_table = cheatorewardslist
                for locationId, value in cheatorewardslist.items():
                    if value == True:
                        locs1.append(int(locationId))
        if ctx.slot_data["honeyb_rewards"] == "true":
            if ctx.honeybrewardslist_table != honeybrewardslist:
                ctx.honeybrewardslist_table = honeybrewardslist
                for locationId, value in honeybrewardslist.items():
                    if value == True:
                        locs1.append(int(locationId))
        if ctx.slot_data["skip_puzzles"] == "true":
            if ctx.worldlist_table != worldslist:
                ctx.worldlist_table = worldslist
                for locationId, value in worldslist.items():
                    if value == True:
                        locs1.append(int(locationId))
        if len(locs1) > 0:
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": locs1
            }])
            
        #GAME VICTORY
        if (ctx.slot_data["goal_type"] == 1 or ctx.slot_data["goal_type"] == 2 or 
            ctx.slot_data["goal_type"] == 3 or ctx.slot_data["goal_type"] == 5) and not ctx.finished_game:
            mumbo_tokens = 0
            for networkItem in ctx.items_received:
                if networkItem.item == 1230798:
                    mumbo_tokens += 1
                    if ((ctx.slot_data["goal_type"] == 1 and mumbo_tokens >= ctx.slot_data["minigame_hunt_length"]) or
                        (ctx.slot_data["goal_type"] == 2 and mumbo_tokens >= ctx.slot_data["boss_hunt_length"]) or
                        (ctx.slot_data["goal_type"] == 3 and mumbo_tokens >= ctx.slot_data["jinjo_family_rescue_length"]) or
                        (ctx.slot_data["goal_type"] == 5 and mumbo_tokens >= ctx.slot_data["token_hunt_length"])): 
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": 30
                        }])
                        ctx.finished_game = True

    #Send Aync Data.
    if "sync_ready" in payload and payload["sync_ready"] == "true" and ctx.sync_ready == False:
        # ctx.items_handling = 0b101
        # await ctx.send_connect()
        ctx.sync_ready = True
        
    # Deathlink handling
    if ctx.deathlink_enabled:
        if payload['isDead']: #Banjo died
            ctx.deathlink_pending = False
            if not ctx.deathlink_sent_this_death:
                ctx.deathlink_sent_this_death = True
                await ctx.send_death()
        else: # Banjo is somehow still alive
            ctx.deathlink_sent_this_death = False

def mumbo_tokens_loc(locs: list, locationId: int, goaltype: int) -> list:
    if goaltype == 1 or goaltype == 4:
        if locationId == 1230598: #MT
            locs.append(1230968)
        if locationId == 1230610: #GM
            locs.append(1230969)
        if locationId == 1230616: #WW
            locs.append(1230970)
        if locationId == 1230617: #WW
            locs.append(1230971)
        if locationId == 1230619: #WW
            locs.append(1230972)
        if locationId == 1230620: #WW
            locs.append(1230973)
        if locationId == 1230626: #JRL
            locs.append(1230974)
        if locationId == 1230641: #TDL
            locs.append(1230975)
        if locationId == 1230648: #GI
            locs.append(1230976)
        if locationId == 1230654: #GI
            locs.append(1230977)
        if locationId == 1230663: #HFP
            locs.append(1230978)
        if locationId == 1230668: #CCL
            locs.append(1230979)
        if locationId == 1230670: #CCL
            locs.append(1230980)
        if locationId == 1230673: #CCL
            locs.append(1230981)
        if locationId == 1230749: #CCL
            locs.append(1230982)
    if goaltype == 2 or goaltype == 4:
        if locationId == 1230596: #MT
            locs.append(1230960)
        if locationId == 1230606: #GGM
            locs.append(1230961)
        if locationId == 1230618: #WW
            locs.append(1230962)
        if locationId == 1230632: #JRL
            locs.append(1230963)
        if locationId == 1230639: #TDL
            locs.append(1230964)
        if locationId == 1230745: #GI
            locs.append(1230965)
        if locationId == 1230656: #HFP
            locs.append(1230966)
        if locationId == 1230666: #CC
            locs.append(1230967)
    if goaltype == 3 or goaltype == 4:
        if locationId == 1230676: #JINJOFAM
            locs.append(1230983)
        if locationId == 1230677: #JINJOFAM
            locs.append(1230984)
        if locationId == 1230678: #JINJOFAM
            locs.append(1230985)
        if locationId == 1230679: #JINJOFAM
            locs.append(1230986)
        if locationId == 1230680: #JINJOFAM
            locs.append(1230987)
        if locationId == 1230681: #JINJOFAM
            locs.append(1230988)
        if locationId == 1230682: #JINJOFAM
            locs.append(1230989)
        if locationId == 1230683: #JINJOFAM
            locs.append(1230990)
        if locationId == 1230684: #JINJOFAM
            locs.append(1230991)
    return locs

async def n64_sync_task(ctx: BanjoTooieContext): 
    logger.info("Starting n64 connector. Use /n64 for status information.")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.n64_streams:
            (reader, writer) = ctx.n64_streams
            if ctx.sendSlot == True:
                msg = get_slot_payload(ctx).encode()
            else:
                msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=10)
                    data_decoded = json.loads(data.decode())
                    reported_version = data_decoded.get('scriptVersion', 0)
                    getSlotData = data_decoded.get('getSlot', 0)
                    if getSlotData == True:
                        ctx.sendSlot = True
                    elif reported_version >= script_version:
                        if ctx.game is not None and 'locations' in data_decoded:
                            # Not just a keep alive ping, parse
                            async_start(parse_payload(data_decoded, ctx, False))
                        if not ctx.auth:
                            ctx.auth = data_decoded['playerName']
                            if ctx.awaiting_rom:
                                await ctx.server_auth(False)
                    else:
                        if not ctx.version_warning:
                            logger.warning(f"Your Lua script is version {reported_version}, expected {script_version}. "
                                "Please update to the latest version. "
                                "Your connection to the Archipelago server will not be accepted.")
                            ctx.version_warning = True
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.n64_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.n64_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.n64_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.n64_streams = None
            if ctx.n64_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to N64")
                    ctx.n64_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.n64_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.n64_status = error_status
                logger.info("Lost connection to N64 and attempting to reconnect. Use /n64 for status updates")
        else:
            try:
                logger.debug("Attempting to connect to N64")
                ctx.n64_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 21221), timeout=10)
                ctx.n64_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.n64_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                continue


def main():
    Utils.init_logging("Banjo-Tooie Client")
    parser = get_base_parser()
    args = parser.parse_args()

    async def _main():
        multiprocessing.freeze_support()

        ctx = BanjoTooieContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.n64_sync_task:
            await ctx.n64_sync_task

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == '__main__':
    main()
