import adv_test
from adv import *

def module():
    return Laranoa

class Laranoa(Adv):
    comment = 'doesn\'t count spbuff for teammates'
    conf = {}
    conf['mod_a3'] = ('s', 'passive', 0.3)
    if 1:
        conf['mod_d'] = [('att', 'passive', 0.30),
                                ('crit','chance',0.15)]
        conf['str_d'] = 91*1.5
    else:
        conf['mod_d'] = ('att', 'passive', 0.60)
        conf['str_d'] = 125*1.5
    
    def pre(this):
        if this.condition('buff all team'):
            this.s2_proc = this.c_s2_proc
        if this.condition('never lose comboes'):
            this.dmg_proc = this.c_dmg_proc
        if this.condition('c4+fs'):
            this.conf['acl'] = """
                `s3,s1.charged>=s1.sp
                `s1
                `s2
                `fs, seq=4
                """

    def init(this):
        this.hits = 0
    
    def c_s2_proc(this, e):
        Teambuff('s2_str',0.10,10).on()
        Selfbuff('s2_sp',0.20,10,'sp','passive').on()

    def s2_proc(this, e):
        Selfbuff('s2_str',0.10,10).on()
        Selfbuff('s2_sp',0.20,10,'sp','passive').on()

    def c_dmg_proc(this, name, amount):
        if name[:2] == 'x1':
            this.hits += 3
        elif name[:2] == 'x2':
            this.hits += 2
        elif name[:2] == 'x3':
            this.hits += 3
        elif name[:2] == 'x4':
            this.hits += 2
        elif name[:2] == 'x5':
            this.hits += 5
        elif name[:2] == 'fs':
            this.hits += 8
        elif name[:2] == 's1':
            this.hits += 14
        if this.hits >= 20:
            this.hits -= 20
            Selfbuff('sylvan critdmg',0.10,20,'crit','damage').on()



if __name__ == '__main__':
    conf = {}
    conf['acl'] = """
        `s3,s1.charged>=s1.sp
        `s1
        `s2
        """
    adv_test.test(module(), conf, verbose=0)


