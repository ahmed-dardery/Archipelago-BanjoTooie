import typing
from BaseClasses import Region

import worlds.banjo_tooie
from .Names import regionName, locationName, itemName
from .Locations import BanjoTooieLocation
from .Rules import BanjoTooieRules


BANJOTOOIEREGIONS: typing.Dict[str, typing.List[str]] = {
    "Menu":              [],
    regionName.SM:       [
        locationName.CHEATOSM1,
        locationName.JINJOIH5,
    #    locationName.FSWIM
    ],
    regionName.IOHJV:    [
        locationName.JIGGYIH1,
        locationName.JIGGYIH2,
        locationName.JIGGYIH3,
        locationName.JIGGYIH4,
        locationName.JIGGYIH5,
        locationName.JIGGYIH6,
        locationName.JIGGYIH7,
        locationName.JIGGYIH8,
        locationName.JIGGYIH9,
        locationName.JIGGYIH10,
        locationName.TREBLEJV
    ],
    regionName.IOHWH:    [
        locationName.JINJOIH1,

        locationName.W1,
        locationName.W2,
        locationName.W3,
        locationName.W4,
        locationName.W5,
        locationName.W6,
        locationName.W7,
        locationName.W8
    ],
    regionName.MT:       [
        locationName.JINJOMT1, 
        locationName.JINJOMT2,
        locationName.JINJOMT3,
        locationName.JINJOMT4,
        locationName.JINJOMT5,
        locationName.JIGGYMT1,
        locationName.JIGGYMT2,
        locationName.JIGGYMT3,
        locationName.JIGGYMT4,
        locationName.JIGGYMT5,
        locationName.JIGGYMT6,
        locationName.JIGGYMT7,
        locationName.JIGGYMT8,
        locationName.JIGGYMT9,
        locationName.JIGGYMT10,
        locationName.GLOWBOMT1,
        locationName.GLOWBOMT2,
        locationName.HONEYCMT1,
        locationName.HONEYCMT2,
        locationName.HONEYCMT3,
        locationName.CHEATOMT1,
        locationName.CHEATOMT2,
        locationName.CHEATOMT3,
        locationName.GGRAB,
        locationName.BBLASTER,
        locationName.EGGAIM,
        locationName.TREBLEMT,
        locationName.NOTEMT1,
        locationName.NOTEMT2,
        locationName.NOTEMT3,
        locationName.NOTEMT4,
        locationName.NOTEMT5,
        locationName.NOTEMT6,
        locationName.NOTEMT7,
        locationName.NOTEMT8,
        locationName.NOTEMT9,
        locationName.NOTEMT10,
        locationName.NOTEMT11,
        locationName.NOTEMT12,
        locationName.NOTEMT13,
        locationName.NOTEMT14,
        locationName.NOTEMT15,
        locationName.NOTEMT16    
    ],
    regionName.IOHPL:    [
        locationName.JINJOIH4,
        locationName.HONEYCIH1,
        locationName.FEGGS,
        locationName.NOTEIH1,
        locationName.NOTEIH2,
        locationName.NOTEIH3,
        locationName.NOTEIH4,
    ],
    regionName.GM:       [
        # locationName.JINJOGM1, moved to GMWSJT
        locationName.JINJOGM2,
        locationName.JINJOGM3,
        locationName.JINJOGM4,
        locationName.JINJOGM5,
        locationName.JIGGYGM2,
        locationName.JIGGYGM3,
        locationName.JIGGYGM4,
        locationName.JIGGYGM5,
        locationName.JIGGYGM6,
        locationName.JIGGYGM7,
        locationName.JIGGYGM8,
        locationName.JIGGYGM9,
        locationName.JIGGYGM10,
        locationName.GLOWBOGM1,
        locationName.GLOWBOGM2,
        locationName.GLOWBOMEG,
        locationName.HONEYCGM1,
        locationName.HONEYCGM2,
        locationName.HONEYCGM3,
        locationName.CHEATOGM1,
        locationName.CHEATOGM2,
        locationName.CHEATOGM3,
        locationName.BDRILL,
        locationName.BBAYONET,
        locationName.TREBLEGM,
        locationName.NOTEGGM1,
        locationName.NOTEGGM2,
        locationName.NOTEGGM3,
        locationName.NOTEGGM4,
        locationName.NOTEGGM5,
        locationName.NOTEGGM6,
        locationName.NOTEGGM7,
        locationName.NOTEGGM8,
        locationName.NOTEGGM9,
        locationName.NOTEGGM10,
        locationName.NOTEGGM11,
        locationName.NOTEGGM12,
        locationName.NOTEGGM13,
        locationName.NOTEGGM14,
        locationName.NOTEGGM15,
        locationName.NOTEGGM16  
    ],
    regionName.GMWSJT: [
        locationName.JINJOGM1,
    ],
    regionName.CHUFFY: 
    [
        locationName.JIGGYGM1,
        locationName.CHUFFY
 
    ],
    regionName.IOHPG:   [
        locationName.GEGGS,
        locationName.NOTEIH5,
        locationName.NOTEIH6,
        locationName.NOTEIH7,
        locationName.NOTEIH8,
    ],
    regionName.WW:      [
        locationName.JINJOWW1,
        locationName.JINJOWW2,
        locationName.JINJOWW3,
        locationName.JINJOWW4,
        locationName.JINJOWW5,
        locationName.JIGGYWW1,
        locationName.JIGGYWW2,
        locationName.JIGGYWW3,
        locationName.JIGGYWW4,
        locationName.JIGGYWW5,
        locationName.JIGGYWW6,
        locationName.JIGGYWW7,
        locationName.JIGGYWW8,
        locationName.JIGGYWW9,
        locationName.JIGGYWW10,
        locationName.GLOWBOWW1,
        locationName.GLOWBOWW2,
        locationName.HONEYCWW1,
        locationName.HONEYCWW2,
        locationName.HONEYCWW3,
        locationName.CHEATOWW1,
        locationName.CHEATOWW2,
        locationName.CHEATOWW3,
        locationName.AIREAIM,
        locationName.SPLITUP,
        locationName.PACKWH,
        locationName.TREBLEWW,
        locationName.TRAINSWWW,
        locationName.NOTEWW1,
        locationName.NOTEWW2,
        locationName.NOTEWW3,
        locationName.NOTEWW4,
        locationName.NOTEWW5,
        locationName.NOTEWW6,
        locationName.NOTEWW7,
        locationName.NOTEWW8,
        locationName.NOTEWW9,
        locationName.NOTEWW10,
        locationName.NOTEWW11,
        locationName.NOTEWW12,
        locationName.NOTEWW13,
        locationName.NOTEWW14,
        locationName.NOTEWW15,
        locationName.NOTEWW16  
    ],
    regionName.IOHCT:   [
        locationName.JINJOIH3,
        locationName.IEGGS,
        locationName.TRAINSWIH,

    ],
    regionName.IOHCT_HFP_ENTRANCE: [
        locationName.GLOWBOIH1,
        locationName.NOTEIH9,
        locationName.NOTEIH10,
        locationName.NOTEIH11,
        locationName.NOTEIH12,
    ],
    regionName.JR:      [
        locationName.JRLDB1,
        locationName.JRLDB2,
        locationName.JRLDB3,
        locationName.JRLDB4,
        locationName.JRLDB5,
        locationName.JRLDB6,
        locationName.JRLDB7,
        locationName.JRLDB8,
        locationName.JRLDB9,
        locationName.JRLDB10,
        locationName.JRLDB11,
        locationName.JRLDB12,
        locationName.JRLDB13,
        locationName.JRLDB14,
        locationName.JRLDB15,
        locationName.JRLDB16,
        locationName.JRLDB17,
        locationName.JRLDB18,
        locationName.JRLDB19,
        locationName.JRLDB20,
        locationName.JRLDB21,
        locationName.JRLDB22,
        locationName.JRLDB23,
        locationName.JRLDB24,
        locationName.JRLDB25,
        locationName.JRLDB26,
        locationName.JRLDB27,
        locationName.JRLDB28,
        locationName.JRLDB29,
        locationName.JRLDB30,
        locationName.JINJOJR1,
        locationName.JINJOJR2,
        locationName.JINJOJR3,
        locationName.JINJOJR4,
        locationName.JINJOJR5,
        locationName.JINJOGI3,
        locationName.JIGGYJR1,
        locationName.JIGGYJR2,
        locationName.JIGGYJR3,
        locationName.JIGGYJR4,
        locationName.JIGGYJR5,
        locationName.JIGGYJR6,
        locationName.JIGGYJR7,
        locationName.JIGGYJR8,
        locationName.JIGGYJR9,
        locationName.JIGGYJR10,
        locationName.GLOWBOJR1,
        locationName.GLOWBOJR2,
        locationName.HONEYCJR1,
        locationName.HONEYCJR2,
        locationName.HONEYCJR3,
        locationName.CHEATOJR1,
        locationName.CHEATOJR2,
        locationName.CHEATOJR3,
        locationName.WWHACK,
        locationName.TTORP,
        locationName.AUQAIM,
        locationName.TREBLEJR,
        locationName.NOTEJRL1,
        locationName.NOTEJRL2,
        locationName.NOTEJRL3,
        locationName.NOTEJRL4,
        locationName.NOTEJRL5,
        locationName.NOTEJRL6,
        locationName.NOTEJRL7,
        locationName.NOTEJRL8,
        locationName.NOTEJRL9,
        locationName.NOTEJRL10,
        locationName.NOTEJRL11,
        locationName.NOTEJRL12,
        locationName.NOTEJRL13,
        locationName.NOTEJRL14,
        locationName.NOTEJRL15,
        locationName.NOTEJRL16 
    ],
    regionName.IOHWL:   [
        locationName.JINJOIH2,
        locationName.CEGGS,
        locationName.NOTEIH13,
        locationName.NOTEIH14,
        locationName.NOTEIH15,
        locationName.NOTEIH16,
    ],
    regionName.TL:      [
        locationName.JINJOTL1,
        locationName.JINJOTL2,
        locationName.JINJOTL3,
        locationName.JINJOTL4,
        locationName.JINJOTL5,
        locationName.JIGGYTD1,
        #locationName.JIGGYTD2, #In CCL
        locationName.JIGGYTD3,
        locationName.JIGGYTD4,
        locationName.JIGGYTD5,
        locationName.JIGGYTD6,
        locationName.JIGGYTD7,
        locationName.JIGGYTD8,
        locationName.JIGGYTD9,
        locationName.JIGGYTD10,
        locationName.JIGGYHP7,
        locationName.GLOWBOTL1,
        locationName.GLOWBOTL2,
        locationName.HONEYCTL1,
        locationName.HONEYCTL2,
        locationName.HONEYCTL3,
        locationName.CHEATOTL1,
        locationName.CHEATOTL2,
        locationName.CHEATOTL3,
        locationName.SPRINGB,
        locationName.TAXPACK,
        locationName.TREBLETL,
        locationName.TRAINSWTD,
        locationName.NOTETDL1,
        locationName.NOTETDL2,
        locationName.NOTETDL3,
        locationName.NOTETDL4,
        locationName.NOTETDL5,
        locationName.NOTETDL6,
        locationName.NOTETDL7,
        locationName.NOTETDL8,
        locationName.NOTETDL9,
        locationName.NOTETDL10,
        locationName.NOTETDL11,
        locationName.NOTETDL12,
        locationName.NOTETDL13,
        locationName.NOTETDL14,
        locationName.NOTETDL15,
        locationName.NOTETDL16
    ],
    regionName.TL_HATCH: [
        locationName.HATCH,
    ],
    regionName.IOHQM:   [],
    regionName.GIO: [
        locationName.TRAINSWGI,
    ],
    regionName.GI1: [
        # locationName.JINJOGI3, Moved to JRL
        locationName.JIGGYGI8,
        locationName.JIGGYGI10,
        locationName.CHEATOGI1,
        locationName.HONEYCGI2,
        locationName.SNPACK,
        locationName.CLAWBTS,
        locationName.NOTEGI4,
        locationName.NOTEGI5,
        locationName.NOTEGI1,
        locationName.NOTEGI2,
        locationName.NOTEGI3,
        locationName.NOTEGI13,
        locationName.NOTEGI14,
        locationName.NOTEGI11,
        locationName.NOTEGI12,
    ],
    regionName.GI2: [
        locationName.GLOWBOGI1,
        locationName.LSPRING,
        locationName.JIGGYGI7,
        locationName.TREBLEGI,
        locationName.NOTEGI6,
        locationName.NOTEGI7,
        locationName.NOTEGI8,
        locationName.NOTEGI9,
        locationName.NOTEGI10,
    ],
    regionName.GI3ALL: [
        locationName.JINJOGI1,
        locationName.JINJOGI2,
        locationName.JINJOGI4,
        locationName.JINJOGI5,
        locationName.JIGGYGI1,
        locationName.JIGGYGI2,
        locationName.JIGGYGI3,
        locationName.JIGGYGI4,
        locationName.JIGGYGI5,
        locationName.JIGGYGI6,
        locationName.JIGGYGI9,
        locationName.HONEYCGI1,
        locationName.HONEYCGI3,
        locationName.GLOWBOGI2,
        locationName.CHEATOGI2,
        locationName.CHEATOGI3,
        locationName.NOTEGI15,
        locationName.NOTEGI16,
        
    ],
    regionName.HP: [
        locationName.JINJOHP1,
        locationName.JINJOHP2,
        locationName.JINJOHP3,
        locationName.JINJOHP4,
        locationName.JINJOHP5,
        locationName.JIGGYHP1,
        locationName.JIGGYHP2,
        locationName.JIGGYHP3,
        locationName.JIGGYHP4,
        locationName.JIGGYHP5,
        locationName.JIGGYHP6,
        #locationName.JIGGYHP7, # in TDL
        locationName.JIGGYHP8,
        locationName.JIGGYHP9,
        locationName.JIGGYHP10,
        locationName.GLOWBOHP1,
        locationName.GLOWBOHP2,
        locationName.HONEYCHP1,
        locationName.HONEYCHP2,
        locationName.HONEYCHP3,
        locationName.CHEATOHP1,
        locationName.CHEATOHP2,
        locationName.CHEATOHP3,
        locationName.SHPACK,
        locationName.GLIDE,
        locationName.TREBLEHP,
        locationName.TRAINSWHP1,
        locationName.TRAINSWHP2,
        locationName.NOTEHFP1,
        locationName.NOTEHFP2,
        locationName.NOTEHFP3,
        locationName.NOTEHFP4,
        locationName.NOTEHFP5,
        locationName.NOTEHFP6,
        locationName.NOTEHFP7,
        locationName.NOTEHFP8,
        locationName.NOTEHFP9,
        locationName.NOTEHFP10,
        locationName.NOTEHFP11,
        locationName.NOTEHFP12,
        locationName.NOTEHFP13,
        locationName.NOTEHFP14,
        locationName.NOTEHFP15,
        locationName.NOTEHFP16
    ],
    regionName.CC:      [
        locationName.JINJOCC1,
        locationName.JINJOCC2,
        locationName.JINJOCC3,
        locationName.JINJOCC4,
        locationName.JINJOCC5,
        locationName.JIGGYCC1,
        locationName.JIGGYCC2,
        locationName.JIGGYCC3,
        locationName.JIGGYCC4,
        locationName.JIGGYCC5,
        locationName.JIGGYCC6,
        locationName.JIGGYCC7,
        locationName.JIGGYCC8,
        locationName.JIGGYCC9,
        locationName.JIGGYCC10,
        locationName.JIGGYTD2,
        locationName.GLOWBOCC1,
        locationName.GLOWBOCC2,
        locationName.HONEYCCC1,
        locationName.HONEYCCC2,
        locationName.HONEYCCC3,
        locationName.CHEATOCC1,
        locationName.CHEATOCC2,
        locationName.CHEATOCC3,
        locationName.SAPACK,
        locationName.TREBLECC,
        locationName.NOTECCL1,
        locationName.NOTECCL2,
        locationName.NOTECCL3,
        locationName.NOTECCL4,
        locationName.NOTECCL5,
        locationName.NOTECCL6,
        locationName.NOTECCL7,
        locationName.NOTECCL8,
        locationName.NOTECCL9,
        locationName.NOTECCL10,
        locationName.NOTECCL11,
        locationName.NOTECCL12,
        locationName.NOTECCL13,
        locationName.NOTECCL14,
        locationName.NOTECCL15,
        locationName.NOTECCL16
    ],
    regionName.CK: [],
    regionName.H1: [
        locationName.HAG1
    ]
}
    
def create_regions(self):
    multiworld = self.multiworld
    player = self.player
    active_locations = self.location_name_to_id
    dellist = []

    # if self.options.skip_puzzles == False:
    #     for location in active_locations:
    #         if location.find("Unlocked") != -1:
    #             dellist.append(location)

    #     for name in dellist:
    #         if( name in active_locations):
    #             del active_locations[name]

    multiworld.regions += [create_region(multiworld, player, active_locations, region, locations) for region, locations in
                           BANJOTOOIEREGIONS.items()]
    
    if multiworld.worlds[player].options.victory_condition == 0:
        multiworld.get_location(locationName.HAG1, player).place_locked_item(
         	multiworld.worlds[player].create_event_item(itemName.VICTORY))

    # if self.options.skip_puzzles == True:
    #     sm = multiworld.get_region(regionName.IOHWH, player)
    #     sm.add_locations({locationName.W1: None,
    #         locationName.W2: None,
    #         locationName.W3: None,
    #         locationName.W4: None,
    #         locationName.W5: None,
    #         locationName.W6: None,
    #         locationName.W7: None,
    #         locationName.W8: None
    #     })


def create_region(multiworld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        loc_to_id = {loc: active_locations.get(loc, 0) for loc in locations if active_locations.get(loc, None)}
        if multiworld.worlds[player].options.victory_condition == 0 and locationName.HAG1 in locations:
            ret.add_locations({locationName.HAG1: None})
        else:
            ret.add_locations(loc_to_id, BanjoTooieLocation)
    return ret

def connect_regions(self):
    multiworld = self.multiworld
    player = self.player
    rules = BanjoTooieRules(self)

    region_menu = multiworld.get_region("Menu", player)
    region_menu.add_exits({regionName.SM})

    region_SM = multiworld.get_region(regionName.SM, player)
    region_SM.add_exits({regionName.IOHJV})

    region_JV = multiworld.get_region(regionName.IOHJV, player)
    region_JV.add_exits({regionName.IOHWH})

    region_WH = multiworld.get_region(regionName.IOHWH, player)
    region_WH.add_exits({regionName.MT, regionName.IOHPL},
                        {regionName.MT: lambda state: rules.mt_jiggy(state), regionName.IOHPL: lambda state: rules.WH_to_PL(state)})

    region_MT = multiworld.get_region(regionName.MT, player)
    region_MT.add_exits({regionName.TL_HATCH, regionName.GM},
                        {regionName.TL_HATCH: lambda state: rules.jiggy_treasure_chamber(state),\
                        regionName.GM: lambda state: rules.dilberta_free(state)})

    region_PL = multiworld.get_region(regionName.IOHPL, player)
    region_PL.add_exits({regionName.GM, regionName.IOHPG, regionName.IOHCT},
                        {regionName.GM: lambda state: rules.PL_to_GGM(state), 
                         regionName.IOHPG: lambda state: rules.PL_to_PG(state),
                        regionName.IOHCT: lambda state: state.has(itemName.SPLITUP, player)})
    
    region_GM = multiworld.get_region(regionName.GM, player)
    region_GM.add_exits({regionName.GMWSJT, regionName.IOHPL, regionName.CHUFFY, regionName.WW},
    {regionName.GMWSJT: lambda state: rules.can_access_water_storage_jinjo_from_GGM(state),
     regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state),
     regionName.IOHPL: lambda state: rules.GGM_to_PL(state),
     regionName.WW: lambda state: rules.ggm_to_ww(state)})
    
    region_PG = multiworld.get_region(regionName.IOHPG, player)
    region_PG.add_exits({regionName.WW, regionName.IOHWL},
    {regionName.WW: lambda state: rules.ww_jiggy(state),
     regionName.IOHWL: lambda state: state.has(itemName.TTORP, player)})
    
    region_WW = multiworld.get_region(regionName.WW, player)
    region_WW.add_exits({regionName.IOHPG, regionName.CHUFFY},
    {regionName.IOHPG: lambda state: rules.ww_jiggy(state),
     regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and state.has(itemName.TRAINSWWW, player)})

    region_IOHCT = multiworld.get_region(regionName.IOHCT, player)
    region_IOHCT.add_exits({regionName.IOHCT_HFP_ENTRANCE, regionName.HP, regionName.JR, regionName.CHUFFY},
        {regionName.HP:lambda state: rules.hfp_jiggy(state),
         regionName.JR: lambda state: rules.jrl_jiggy(state),
         regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and state.has(itemName.TRAINSWIH, player)})
  
    region_JR = multiworld.get_region(regionName.JR, player)
    region_JR.add_exits({regionName.GMWSJT, regionName.IOHCT},
                        {regionName.GMWSJT: lambda state: rules.can_access_water_storage_jinjo_from_JRL(state), regionName.IOHCT: lambda state: rules.JRL_to_CT(state)})

    region_HP = multiworld.get_region(regionName.HP, player)
    region_HP.add_exits({regionName.IOHCT_HFP_ENTRANCE, regionName.MT, regionName.JR, regionName.CHUFFY, regionName.IOHCT},
                        {regionName.IOHCT_HFP_ENTRANCE: lambda state: rules.HFP_to_CTHFP(state),
                         regionName.MT: lambda state: rules.HFP_to_MT(state),
                         regionName.JR: lambda state: rules.can_access_ccl(state) and state.has(itemName.SPLITUP, player),
                         regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and state.has(itemName.TRAINSWHP1, player),
                         regionName.IOHCT: lambda state: rules.HFP_to_CTHFP(state)})
    region_IOHWL = multiworld.get_region(regionName.IOHWL, player)
    region_IOHWL.add_exits({regionName.IOHPG, regionName.IOHQM, regionName.TL, regionName.CC},
                        {regionName.IOHPG: lambda state: rules.WL_to_PG(state),
                         regionName.IOHQM: lambda state: state.has(itemName.SPRINGB, player),
                         regionName.TL: lambda state: rules.tdl_jiggy(state),
                         regionName.CC: lambda state: rules.ccl_jiggy(state)})
    
    region_TL = multiworld.get_region(regionName.TL, player)
    region_TL.add_exits({regionName.TL_HATCH, regionName.WW, regionName.CHUFFY, regionName.IOHWL},
                        {regionName.WW: lambda state: rules.TDL_to_WW(state),
                         regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and state.has(itemName.TRAINSWTD, player),
                         regionName.IOHWL: lambda state: rules.TDL_to_IOHWL(state),
                         })
    
    region_QM = multiworld.get_region(regionName.IOHQM, player)
    region_QM.add_exits({regionName.GIO, regionName.IOHWL, regionName.CK},
                        {regionName.GIO: lambda state: rules.gi_jiggy(state),
                         regionName.IOHWL: lambda state: rules.QM_to_WL(state),
                         regionName.CK: lambda state: rules.quag_to_CK(state)})
    
    region_GIO = multiworld.get_region(regionName.GIO, player)
    region_GIO.add_exits({regionName.GI1, regionName.GI2, regionName.GI3ALL, regionName.IOHQM},
                        {regionName.GI1: lambda state: rules.outside_gi_to_floor1(state),
                         regionName.GI2: lambda state: rules.outside_gi_to_floor2(state),
                         regionName.GI3ALL: lambda state: rules.outside_gi_to_floor3(state),
                         regionName.IOHQM: lambda state: rules.gi_jiggy(state)})
    
    region_GI1 = multiworld.get_region(regionName.GI1, player)
    region_GI1.add_exits({regionName.GIO, regionName.GI2, regionName.CHUFFY},
                        {regionName.GIO: lambda state: state.has(itemName.SPLITUP, self.player),
                         regionName.GI2: lambda state: rules.can_access_gi_fl1_2fl2(state),
                         regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and state.has(itemName.TRAINSWGI, player)})
    
    region_GI2 = multiworld.get_region(regionName.GI2, player)
    region_GI2.add_exits({regionName.GIO, regionName.GI1, regionName.GI3ALL},
                        {regionName.GI1: lambda state: rules.F2_to_F1(state), regionName.GI3ALL: lambda state: rules.F2_to_F3(state)})
    
    region_GI3ALL = multiworld.get_region(regionName.GI3ALL, player)
    region_GI3ALL.add_exits({regionName.GIO, regionName.GI2})

    region_CK = multiworld.get_region(regionName.CK, player)
    region_CK.add_exits({regionName.H1},
                        {regionName.H1: lambda state: rules.check_hag1_options(state)})
    
    region_chuffy = multiworld.get_region(regionName.CHUFFY, player)
    region_chuffy.add_exits({regionName.GM, regionName.WW, regionName.IOHCT, regionName.TL,regionName.GI1,regionName.HP},
                        {regionName.GM: lambda state: state.has(itemName.CHUFFY, self.player),
                         regionName.WW: lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWWW, player),
                         regionName.IOHCT: lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWIH, player),
                         regionName.TL: lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWTD, player),
                         regionName.GI1: lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWGI, player),
                         regionName.HP: lambda state: state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, player)
                         })
 