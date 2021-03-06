
conf = {}
conf.update( {
        "x_type"         : "melee" ,

        "x1_dmg"         : 97     / 100.0 ,
        "x1_sp"          : 130            ,
        "x1_startup"     : 10     / 60.0  ,
        "x1_recovery"    : 23     / 60.0  ,

        "x2_dmg"         : 97     / 100.0 ,
        "x2_sp"          : 130            ,
        "x2_startup"     : 0              ,
        "x2_recovery"    : 41     / 60.0  ,

        "x3_dmg"         : 63*2   / 100.0 ,
        "x3_sp"          : 220            ,
        "x3_startup"     : 6      / 60.0  ,
        "x3_recovery"    : 37     / 60.0  ,

        "x4_dmg"         : 129    / 100.0 ,
        "x4_sp"          : 360            ,
        "x4_startup"     : 0              ,
        "x4_recovery"    : 65     / 60.0  ,

        "x5_dmg"         : 194    / 100.0 ,
        "x5_sp"          : 660            ,
        "x5_startup"     : 0              ,
        "x5_recovery"    : 33     / 60.0  ,

        "fsf_startup"    : 0              ,
        "fsf_recovery"   : 33     / 60.0  ,

        "fs_dmg"         : 92     / 100.0 ,
        "fs_sp"          : 200            ,
        "fs_startup"     : 30     / 60.0  ,
        "fs_recovery"    : 41     / 60.0  ,

        "dodge_recovery" : 43     / 60.0  ,

        "mod_wep" : ("crit", "chance", 0.02) ,

        }
        )

import blade5b1
import blade5b2
import blade5b3

flame  = blade5b1
wind   = blade5b1

water  = blade5b2
light  = blade5b2

shadow = blade5b3
