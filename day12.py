import re
from math import gcd

with open('inputday12.txt','r') as f:
    moonpos_str = f.readlines()

print(moonpos_str)


moonpos = [[0,0,0] for _ in range(len(moonpos_str))]
moonvel = [[0,0,0] for _ in range(len(moonpos_str))]

posreg = re.compile('([xyz])=(-{0,1}[0-9]+)')

for idx,line in enumerate(moonpos_str):
    print(idx)
    coords = dict(posreg.findall(line))
    moonpos[idx][0] = int(coords['x'])
    moonpos[idx][1] = int(coords['y'])
    moonpos[idx][2] = int(coords['z'])

print(moonpos)
print(moonvel)


period = [0,0,0]

for i in range(3):
    state_x = [pos[i] for pos in moonpos]
    vel_x = [vel[i] for vel in moonvel]

    done = False

    while not done:
        for moon1 in range(len(vel_x)):
            for moon2 in range(moon1+1,len(vel_x)):
                vel_x[moon1] += (2*(state_x[moon1] < state_x[moon2])-1
                    + (state_x[moon1] == state_x[moon2]))
                vel_x[moon2] += (2*(state_x[moon1] > state_x[moon2])-1                
                    + (state_x[moon1] == state_x[moon2]))
            state_x[moon1] += vel_x[moon1]
        period[i] += 1
        done = True
        for moon,pos in enumerate(state_x):
            if pos != moonpos[moon][i]:
                done = False
                break
        for moon,vel in enumerate(vel_x):
            if vel != moonvel[moon][i]:
                done = False


pxy = period[0]*period[1]//gcd(period[0],period[1])

pxyz = pxy*period[2]//gcd(pxy,period[2])

print(pxyz)