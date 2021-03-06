# encoding:utf8
if __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from core.log import *
import time
import sys
import conf as globalconf
import random


if len(sys.argv) >= 3:
    sim_duration = int(sys.argv[2])
else:
    sim_duration = 180
sim_times = 1000


team_dps = 3500 #(1500+1500+500)
energy_efficiency = 5000 * 0.5 * 2 / 5 / sim_duration
mname = ""
base_str = 0
comment = ""
condition = ""
dps = 0
bps = 0
energy = 0
def test(classname, conf, verbose=0, mass=0):
    global mname
    global base_str
    global comment
    global condition
    global loglevel
    if not loglevel:
        loglevel = verbose
    random.seed(0)
    a = time.time()
    mname = classname.__name__
    adv = classname(conf=conf)
    adv.run(sim_duration)
    base_str = adv.conf['base_str']
    if type(adv.conf['mod_d']) == list:
        for i in adv.conf['mod_d']:
            if i[0] == 'att':
                d_aura = i[2]
    else:
        if adv.conf['mod_d'][0] == 'att':
            d_aura = adv.conf['mod_d'][2]

    condition = adv.condition()
    #if 'condition' in adv.conf:
    #    for i in adv.conf['condition']:
    #        if condition == '':
    #            condition = i
    #        else:
    #            condition += ' & %s'%i

    comment = adv.comment



    if loglevel >= 2:
        print adv._acl_str

    if loglevel > 0:
        logcat()
        sum_ac()
    if loglevel == 3:
        if adv.conf['x_type'] == 'melee':
            logcat(['dmg','cancel','fs','cast','buff'])
        if adv.conf['x_type'] == 'ranged':
            logcat(['x','dmg','cancel','fs','cast','buff'])


    if mass:
        if loglevel != -1:
            r = sum_dmg()
        if loglevel <= 0:
            random.seed()
            do_mass_sim(classname, conf)
    else:
        r = sum_dmg()

    dps1 = dps
    bps1 = bps
    energy1 = energy

    if condition != '':
        adv_c = classname(conf=conf)
        adv_c.condition()
        adv_c.run(sim_duration)
        if mass:
            if loglevel != -1:
                rc = sum_dmg()
            if loglevel <= 0:
                random.seed()
                do_mass_sim(classname, conf, 1)
        else:
            rc = sum_dmg()

        if loglevel > 0:
            logcat()
            sum_ac()
        if loglevel == 3:
            if adv.conf['x_type'] == 'melee':
                logcat(['dmg','cancel','fs','cast','buff'])
            if adv.conf['x_type'] == 'ranged':
                logcat(['x','dmg','cancel','fs','cast','buff'])

    if condition == '':
        recount = "%d"%(dps1)
        if bps1:
            recount += '(%.2f)'%bps1
        if energy1:
            recount += '(team_energy:%d)'%energy1
        dps2 = dps
    if condition != '':
        dps2 = dps
        bps2 = bps
        energy2 = energy
        if dps2 < dps1:
            dps2 = dps1
        if bps2 < bps1:
            bps2 = bps1
        if energy2 < energy1:
            energy2 = energy1
        recount = "%d/%d"%(dps1, dps2)
        if bps1:
            recount += '(%.2f/%.2f)'%(bps1, bps2)
        if energy1:
            recount += '(team_energy:%d/%d)'%(energy1, energy2)

    if loglevel >= 0 or loglevel == None:
        if condition != '':
            condition = '<%s>'%(condition)
        print '\n======================='
        #print mname,"%d"%float_dps
        print "%s , %s (str: %d) %s ;%s"%( recount, mname, base_str*(1+d_aura), condition, comment )
        print '-----------------------'
        print "dmgsum     |", r['dmg_sum']
        print "skill_stat |", r['sdmg_sum']
        print "x_stat     |", r['xdmg_sum']
        if r['o_sum']:
            print "others     |", r['o_sum']

        if condition != '':
            recount = "%d"%dps
            if bps:
                recount += '(%.2f)'%bps
            if energy:
                recount += '(team_energy:%d)'%energy
            r = rc
            print '-----------------------'
            #print mname,"%d"%float_dps
            print "condition",condition
            print '-----------------------'
            print "dmgsum     |", r['dmg_sum']
            print "skill_stat |", r['sdmg_sum']
            print "x_stat     |", r['xdmg_sum']
            if r['o_sum']:
                print "others     |", r['o_sum']

    elif loglevel == -1:
        if condition != '':
            condition = '<%s>'%(condition)
        print "%s , %s (str: %d) %s ;%s"%( recount, mname, base_str*(1+d_aura), condition, comment )
    elif loglevel == -2:
        comment += " (str: %d)"%(base_str*(1+d_aura))
        bps1 = team_dps*bps1+energy1*energy_efficiency
        bps_delta = team_dps*bps+energy*energy_efficiency 
        if bps_delta < bps1:
            bps_delta = 0
        else:
            bps_delta = bps_delta - bps1
        if condition != '':
            condition = '<%s>'%condition
        line = "%s,%s,%s,%s,%s,%d,%d,%d,%d"%(
                mname,adv.conf['stars']+'*', adv.conf['element'], adv.conf['weapon'], condition+';'+comment,
                dps1, bps1, 
                dps2-dps1, bps_delta, 
                )
        line = line.replace(',3*,',',3星,').replace(',4*,',',4星,').replace(',5*,',',5星,')
        line = line.replace('sword','剑').replace('blade','刀').replace('axe','斧').replace('dagger','匕')
        line = line.replace('lance','枪').replace('wand','法').replace('bow','弓')
        line = line.replace('shadow','暗').replace('light','光')
        line = line.replace('wind','风').replace('water','水').replace('flame','火')
        print line

    b = time.time()
    if loglevel >= 2:
        print '-----------------------\nrun in %f'%(b-a)
    return


def statis(data, mname):
    total = 0
    dmin = data[0][0]
    dmax = data[0][0]
    bmin = data[0][1]
    bmax = data[0][1]
    size = len(data)
    buff_sum = 0
    energy_sum = 0
    for i in data:
        total += i[0]
        buff_sum += i[1]
        energy_sum += i[2]
        if i[0] < dmin:
            dmin = i[0]
        if i[0] > dmax:
            dmax = i[0]
        if i[1] < bmin:
            bmin = i[1]
        if i[1] > bmax:
            bmax = i[1]
    
    global dps
    global bps
    global energy
    global comment
    dps = float(total)/size
    bps = float(buff_sum)/size
    energy = float(energy_sum)/size
    if bps and bmin != bmax:
        comment = '(%.0f~%.0f)(%.2f~%.2f) %s'%(dmin, dmax, bmin, bmax, comment)
    else:
        comment = '(%.0f~%.0f) %s'%(dmin, dmax, comment)
    if energy:
        comment += '(team_energy:%.0f)'%energy

    #print "%d , %s (str: %d) %s ;(%.2f, %.2f) %s"%(total/size, mname, base_str, condition, dmin, dmax, comment)

def do_mass_sim(classname, conf, cond=0):
    a = time.time()
    mname = classname.__name__

    results = []
    for i in range(sim_times):
        adv = classname(conf=conf)
        if cond:
            adv.condition()
        adv.run(sim_duration)
        r = sum_dmg(1)
        results.append(r)
    statis(results, mname)

    b = time.time()
    if loglevel >= 2:
        print '-----------------------\nrun in %f'%(b-a)
    return 

def sum_ac():
    l = logget()
    prev = 0
    ret = []
    for i in l:
        if i[2] == 'succ':
            i[2] = 'fs'
        if i[1] == 'x':
            if i[2] == 'x5':
                ret.append('c5')
            prev = int(i[2][1])
        if i[1] == 'cast' or i[1] == 'fs':
            if prev:
                if prev != 5:
                    ret.append("c%d"%prev)
                ret.append(i[2])
                prev = 0
            else:
                ret.append(i[2])
    print ret
    prev = 'c0'
    row = 0
    rowend = 11
    c5count = 0
    for i in ret:
        if prev == 'c' and i[0] != 'c' and c5count!=0:
            print 'c5*%d'%(c5count),
            c5count = 0
            row += 5

        if i[0] == 's':
            if prev != 's':
                print '-'*(rowend - row), i,
                row = 0
            else:
                print i
            prev = 's'
        elif i[0] == 'c':
            if prev == 's':
                row = 0
                print ''
            elif prev == 'fs':
                row = 0
                print ''
            if i == 'c5':
                c5count+=1
            else:
                if c5count == 0:
                    print i,
                    row += 3
                else:
                    print 'c5*%d %s'%(c5count, i),
                    c5count=0
                    row += 8
            prev = 'c'
        elif i == 'fs':
            if prev == 'fs':
                print '\nfs',
                row = 3
            else:
                print 'fs',
                row +=3
            prev = 'fs'
    print ''

def sum_dmg(silence=0):
    l = logget()
    dmg_sum = {'x': 0, 's': 0, 'fs': 0, 'others':0 }
    sdmg_sum = {'s1':{"dmg":0, "count": 0}, 
                's2':{"dmg":0, "count": 0}, 
                's3':{"dmg":0, "count": 0}, 
                }
    xdmg_sum = {"x1":0, "x2":0, "x3":0, "x4":0, "x5":0, "fs":0}
    team_buff_powertime = 0
    team_buff_power = 0
    team_buff_start = 0
    team_energy = 0
    o_sum = {}
    for i in l:
        if i[1] == 'dmg':
            #dmg_sum[i[2][0]] += i[3]
            if i[2][0] == 'x':
                dmg_sum['x'] += i[3]
            elif i[2][:2] == 's1':
                dmg_sum['s'] += i[3]
                sdmg_sum['s1']['dmg'] += i[3]
            elif i[2][:2] == 's2':
                dmg_sum['s'] += i[3]
                sdmg_sum['s2']['dmg'] += i[3]
            elif i[2][:2] == 's3':
                dmg_sum['s'] += i[3]
                sdmg_sum['s3']['dmg'] += i[3]
            elif i[2][:2] == 'fs':
                dmg_sum['fs'] += i[3]
                xdmg_sum['fs'] += 1
            elif i[2][0] == 'o':
                dmg_sum['others'] += i[3]
                if i[2][2:] in o_sum:
                    o_sum[i[2][2:]] += i[3]
                else:
                    o_sum[i[2][2:]] = i[3]
        elif i[1] == 'cast' or i[1] == 's':
            if i[2] == 's1':
                sdmg_sum['s1']['count'] += 1
            elif i[2] == 's2':
                sdmg_sum['s2']['count'] += 1
            elif i[2] == 's3':
                sdmg_sum['s3']['count'] += 1
        elif i[1] == 'x' :
            xdmg_sum[i[2]] += 1
        elif i[1] == 'buff' and i[2] == 'team':
            if team_buff_power != 0:
                team_buff_powertime += team_buff_power*(i[0] - team_buff_start)
            team_buff_start = i[0]
            team_buff_power = i[3]
        elif i[1] == 'energy' and i[2] == 'team':
            team_energy += i[3]
    team_buff_powertime += (sim_duration - team_buff_start)*team_buff_power


    total = dmg_sum['x'] + dmg_sum['s'] + dmg_sum['fs'] + dmg_sum['others']
    dmg_sum['total'] = total
    xdmg_sum['x1'] -= xdmg_sum['x5']
    xdmg_sum['x2'] -= xdmg_sum['x5']
    xdmg_sum['x3'] -= xdmg_sum['x5']
    xdmg_sum['x4'] -= xdmg_sum['x5']

    xdmg_sum['x1'] -= xdmg_sum['x4']
    xdmg_sum['x2'] -= xdmg_sum['x4']
    xdmg_sum['x3'] -= xdmg_sum['x4']

    xdmg_sum['x1'] -= xdmg_sum['x3']
    xdmg_sum['x2'] -= xdmg_sum['x3']

    xdmg_sum['x1'] -= xdmg_sum['x2']
    tmp = xdmg_sum
    xdmg_sum = {}
    for i in tmp:
        if tmp[i] != 0:
            xdmg_sum[i] = tmp[i]

    global dps
    global bps
    global energy
    dps = dmg_sum['total']/sim_duration
    bps = team_buff_powertime/sim_duration
    energy = team_energy
    if silence:
        return dps, bps, energy 

    for i in dmg_sum:
        dmg_sum[i] = '%.0f'%dmg_sum[i]
    for i in sdmg_sum:
        sdmg_sum[i] = "%.0f (%d)"%(sdmg_sum[i]['dmg'], sdmg_sum[i]['count'])
    for i in o_sum:
        o_sum[i] = "%.0f"%(o_sum[i])
    
    r = {}
    r['dmg_sum'] = dmg_sum
    r['sdmg_sum'] = sdmg_sum
    r['xdmg_sum'] = xdmg_sum
    r['o_sum'] = o_sum
    r['buff_sum'] = team_buff_powertime/sim_duration
    r['energy_sum'] = team_energy

    #if loglevel >= 0 or loglevel == None:
    #    print '\n======================='
    #    #print mname,"%d"%float_dps
    #    print "%d , %s (str: %d) %s ;%s"%( float_dps, mname, base_str, condition, comment )
    #    print '-----------------------'
    #    print "dmgsum     |", dmg_sum
    #    print "skill_stat |", sdmg_sum
    #    print "x_stat     |", xdmg_sum
    #    print "others     |", o_sum
    #elif loglevel == -1:
    #    print "%d , %s (str: %d) %s ;%s"%( float_dps, mname, base_str, condition, comment )
    return r
