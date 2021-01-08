
with open('inputday3.txt','r') as f:
    paths = f.readlines()

paths = [path.strip().split(',') for path in paths]


o = [0,0]

pts = [[o],[o]]
isec = []

vec = {'U':[0,1],'D':[0,-1],'R':[1,1],'L':[1,-1]}

plens=[[0],[0]]

for num,path in enumerate(paths):
    for step in path:
        ax,d = vec[step[0]]
        slen = int(step[1:])
        plens[num].append(plens[num][-1]+slen)
        nextpt = [coord for coord in pts[num][-1]]
        nextpt[ax] += slen*d
        pts[num].append(nextpt)


#do two path segments intersect
def intersect_length(i1,i2):
    cc1 = vec[paths[0][i1][0]][0]
    cc2 = vec[paths[1][i2][0]][0]

    inter_length = -1
    if cc1 == cc2:
        if pts[0][i1][1-cc1] == pts[1][i2][1-cc2]:
            x11 = min(pts[0][i1][cc1],pts[0][i1+1][cc1])
            x12 = max(pts[0][i1][cc1],pts[0][i1+1][cc1])
            x21 = min(pts[1][i2][cc1],pts[1][i2+1][cc1])
            x22 = max(pts[1][i2][cc1],pts[1][i2+1][cc1])

            for x in range(x11,x12+1):
                if x >= x21 and x <= x22:
                    ilen = abs(x - pts[0][i1][cc1]) + abs(x - pts[1][i2][cc1]) + plens[0][i1] + plens[1][i2]
                    if ilen < inter_length or inter_length <= 0:
                        inter_length = inter_length    

    else:
        x0 = pts[1][i2][cc1]
        x1 = min(pts[0][i1][cc1],pts[0][i1+1][cc1])
        x2 = max(pts[0][i1][cc1],pts[0][i1+1][cc1])
        
        y0 = pts[0][i1][cc2]
        y1 = min(pts[1][i2][cc2],pts[1][i2+1][cc2])
        y2 = max(pts[1][i2][cc2],pts[1][i2+1][cc2])

        if x0 >= x1 and x0 <= x2 and y0 >= y1 and y0 <= y2:
            inter_length = (plens[0][i1] + plens[1][i2]
                             + abs(x0 - pts[0][i1][cc1]) + abs(y0 - pts[1][i2][cc2]))

    return inter_length

    
        
i1r = len(paths[0])
i2r = len(paths[1])

isecpts = []
min_inter_length = -1
for i1 in range(i1r):
    for i2 in range(i2r):
        inter_length = intersect_length(i1,i2)
        if (inter_length < min_inter_length or min_inter_length <= 0) and inter_length > 0:
            min_inter_length = inter_length

print(min_inter_length)
