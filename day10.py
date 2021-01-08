from math import gcd, atan, pi



with open('inputday10.txt','r') as f:
    astmap = f.readlines()

xr = len(astmap[0])-1
yr = len(astmap)


asts = []
for y,line in enumerate(astmap):
    for x, mapval in enumerate(line):
        if mapval == '#':
            asts.append([x,y])


bestast = 0
bestseen = 0

for astnum,ast in enumerate(asts):
    seen = 0

    #scan directions (N,E,S,W first)
    for step in range(1,yr-ast[1]):
        if astmap[ast[1]+step][ast[0]] == '#':
            seen += 1
            break
    for step in range(1,xr-ast[0]):
        if astmap[ast[1]][ast[0]+step] == '#':
            seen += 1
            break
    for step in range(1,ast[1]+1):
        if astmap[ast[1]-step][ast[0]] == '#':
            seen += 1
            break
    for step in range(1,ast[0]+1):
        if astmap[ast[1]][ast[0]-step] == '#':
            seen += 1
            break
   
    for xinc in range(1,max(ast[0]+1,xr-ast[0])):
        for yinc in range(1,max(ast[1]+1,yr-ast[1])):
            #avoid scanning the same direction twice with an integer multiple step
            if yinc == 1 or xinc == 1 or gcd(xinc,yinc) == 1:
                #'SE'
                for step in range(1,1+min((yr-1-ast[1])//yinc,(xr-1-ast[0])//xinc)):
                    if astmap[ast[1]+step*yinc][ast[0]+step*xinc] == '#':
                        seen += 1
                        break
                #'SW'
                for step in range(1,1+min((yr-1-ast[1])//yinc,ast[0]//xinc)):
                    if astmap[ast[1]+step*yinc][ast[0]-step*xinc] == '#':
                        seen += 1
                        break
                #'NW'
                for step in range(1,1+min(ast[1]//yinc,ast[0]//xinc)):
                    if astmap[ast[1]-step*yinc][ast[0]-step*xinc] == '#':
                        seen += 1
                        break
                #'NE'
                for step in range(1,1+min(ast[1]//yinc,(xr-1-ast[0])//xinc)):
                    if astmap[ast[1]-step*yinc][ast[0]+step*xinc] == '#':
                        seen += 1
                        break

    if seen > bestseen:
        bestseen = seen
        bestast = astnum

bestloc = asts[bestast]

print(bestloc, bestseen)

dists = [[ast[0]-bestloc[0],ast[1]-bestloc[1]] for ast in asts]

ordered = []
for dist in dists:
    #don't blow yourself up
    if dist == [0,0]:
        continue
    norm = dist[0]**2 + dist[1]**2
    vec = [dist[0]/norm, dist[1]/norm]
    if dist[0] == 0:
        arg = pi/2 * (2*(dist[1] > 0)-1)
    else:
        arg = atan(dist[1]/dist[0])

    if dist[0] < 0:
        arg += pi
    for idx,orderpt in enumerate(ordered):
        if orderpt[0] > arg:
            ordered = ordered[:idx] + [[arg,dist[0],dist[1]]] + ordered[idx:]
            break
        elif orderpt[0] == arg:
            while ordered[idx][0] == arg and (abs(ordered[idx][1]) < abs(dist[0]) or abs(ordered[idx][2]) < abs(dist[1])):
                idx += 1
            ordered = ordered[:idx] + [[arg,dist[0],dist[1]]] + ordered[idx:]
            break
    else:
        ordered.append([arg,dist[0],dist[1]])

#zap
zapctr = 1
while len(ordered):
    idx = 0
    while idx < len(ordered):
        arg = ordered[idx][0]
        print("Asteroid number",zapctr,"was at",ordered[idx][1]+bestloc[0],bestloc[1]+ordered[idx][2],"angle",arg)
        if idx < len(ordered) - 1:
            ordered = ordered[:idx] + ordered[idx+1:]
            while idx < len(ordered) and ordered[idx][0] == arg:
                idx += 1
        else:
            ordered = ordered[:idx]
        zapctr += 1
