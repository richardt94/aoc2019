import io

def show(bugbits):
    outstream = io.StringIO()
    for i in range(25):
        if not i%5:
            outstream.write('\n')
        if i == 12:
            outstream.write('?')
        elif bugbits % 2:
            outstream.write('#')
        else:
            outstream.write('.')
        bugbits >>= 1
    print(outstream.getvalue()[::-1])

def rshow(rbugbits, nlvls):
    for lv in range(201-nlvls, 201+nlvls+1):
        print("level", lv - 201)
        show(rbugbits[lv])


with open("inputday24.txt") as f:
    bugmap = f.readlines()

bugbits = 0
for i in range(25):
    bugbits *= 2
    if bugmap[i//5][i%5] == '#':
        bugbits += 1

rbugbits = [0 for _ in range(403)]

rbugbits[201] = bugbits
u7 = [0, 1, 2, 3, 4]
l11 = [0, 5, 10, 15, 20]
r13 = [4, 9, 14, 19, 24]
d17 = [20, 21, 22, 23, 24]

for _ in range(200):
    nbugbits = [0 for _ in range(403)]
    for lv in range(1,402):
        bugbits = rbugbits[lv]
        ibugbits = rbugbits[lv+1]
        obugbits = rbugbits[lv-1]
        for i in range(25):
            if i == 12:
                continue
            
            if i % 5 == 0:
                r = (obugbits>>11)%2
            elif i == 13:
                r = 0
                for j in r13:
                    r += (ibugbits>>j)%2
            else:
                r = ((bugbits<<1)>>i)%2

            if i % 5 == 4:
                l = (obugbits>>13)%2
            elif i == 11:
                l = 0
                for j in l11:
                    l += (ibugbits>>j)%2
            else:
                l = (bugbits>>(i+1))%2

            if i // 5 == 0:
                d = (obugbits>>7)%2
            elif i == 17:
                d = 0
                for j in d17:
                    d += (ibugbits>>j)%2
            else:
                d = ((bugbits<<5)>>i)%2


            if i // 5 == 4:
                u = (obugbits>>17)%2
            elif i == 7:
                u = 0
                for j in u7:
                    u += (ibugbits>>j)%2
            else:
                u = (bugbits>>(i+5))%2

            nn = l + r + u + d
            # print(i, l, r, u, d)
            #if bug here now
            if (bugbits>>i)%2:
                if nn == 1:
                    nbugbits[lv] += 2**i
            elif 1 <= nn <= 2:
                nbugbits[lv] += 2**i
    rbugbits = nbugbits

rshow(rbugbits,100)

nbugs = 0
for bugbits in rbugbits:
    while bugbits > 0:
        nbugs += bugbits % 2
        bugbits >>= 1

print(nbugs)