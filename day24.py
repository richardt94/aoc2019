import io

def show(bugbits):
    outstream = io.StringIO()
    for i in range(25):
        if not i%5:
            outstream.write('\n')
        if bugbits % 2:
            outstream.write('#')
        else:
            outstream.write('.')
        bugbits >>= 1
    print(outstream.getvalue()[::-1])


with open("inputday24.txt") as f:
    bugmap = f.readlines()

bugbits = 0
for i in range(25):
    bugbits *= 2
    if bugmap[i//5][i%5] == '#':
        bugbits += 1

visited = set()
while bugbits not in visited:
    show(bugbits)
    visited.add(bugbits)
    nbugbits = 0
    for i in range(25):
        l = (bugbits>>(i+1))%2 if (i % 5 != 4) else 0
        r = ((bugbits<<1)>>i)%2 if (i % 5 != 0) else 0
        u = (bugbits>>(i+5))%2
        d = ((bugbits<<5)>>i)%2
        nn = l + r + u + d
        # print(i, l, r, u, d)
        #if bug here now
        if (bugbits>>i)%2:
            if nn == 1:
                nbugbits += 2**i
        elif 1 <= nn <= 2:
            nbugbits += 2**i
    bugbits = nbugbits

score = 0
for _ in range(25):
    score <<= 1
    if bugbits % 2:
        score += 1
    bugbits >>= 1
print(score)