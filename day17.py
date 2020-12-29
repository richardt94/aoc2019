import io
import sys

class IntcodeComputer:
    def __init__(self, fname, outstream, instring):
        with open(fname,'r') as f:
            self.intcode = f.read()

        self.intcode = self.intcode.split(',')

        #add memory
        self.intcode = self.intcode + ['0']*5000

        self.idx = 0
        self.rbase = 0
        self.done = False
        self.stream = outstream
        self.instring = instring
        self.stridx = 0

    def execute(self):
        while not self.done:
            opcode = int(self.intcode[self.idx][-2:])
            # print("executing opcode", opcode, "at address", self.idx)
            param_modes = [int(c) for c in self.intcode[self.idx][:-2]]
            #deal with possible leading zeros
            while len(param_modes) < 3:
                param_modes = [0] + param_modes
            
            #reverse
            param_modes = param_modes[::-1]

            #compute argument pointers
            params = []
            for x,mode in enumerate(param_modes):
                if mode == 2:
                    params += [int(self.intcode[self.idx+1+x])+self.rbase]
                elif mode:
                    params += [self.idx+1+x]
                else:
                    if len(self.intcode) > self.idx+1+x:
                        params += [int(self.intcode[self.idx+1+x])]
                    else:
                        #either something is wrong or the opcode doesn't need this parameter
                        params += [0]

            if opcode == 99:
                self.done = True
            elif opcode == 1:
                self.intcode[params[2]] = str(int(self.intcode[params[0]]) + int(self.intcode[params[1]]))
                self.idx += 4
            elif opcode == 2:
                self.intcode[params[2]] = str(int(self.intcode[params[0]]) * int(self.intcode[params[1]]))
                self.idx += 4
            elif opcode == 3:
                #intcode[params[0]] = str(int(input('opcode 3 value:')))
                self.intcode[params[0]] = str(ord(self.instring[self.stridx]))
                self.stridx += 1
                self.idx += 2
            elif opcode == 4:
                self.idx += 2
                val = int(self.intcode[params[0]])
                if val >= 256:
                    self.stream.write(str(val))
                else:
                    self.stream.write(chr(val))
            elif opcode == 5:
                if int(self.intcode[params[0]]):
                    self.idx = int(self.intcode[params[1]])
                else:
                    self.idx += 3
            elif opcode == 6:
                if not int(self.intcode[params[0]]):
                    self.idx = int(self.intcode[params[1]])
                else:
                    self.idx += 3
            elif opcode == 7:
                self.intcode[params[2]] = str(int(int(self.intcode[params[0]]) < int(self.intcode[params[1]])))
                self.idx += 4
            elif opcode == 8:
                self.intcode[params[2]] = str(int(int(self.intcode[params[0]]) == int(self.intcode[params[1]])))
                self.idx += 4
            elif opcode == 9:
                self.rbase += int(self.intcode[params[0]])
                self.idx += 2
                
            else:
                print("error, invalid opcode!")
                self.done = True
        return 99

outstream = io.StringIO()
intcomp = IntcodeComputer("inputday17.txt", outstream, "")

# done = False
intcomp.execute()
# while not done:
#     nextcharacter = intcomp.execute(0)
#     if nextcharacter == 99:
#         done = True
#     else:
#         outstream.write(chr(nextcharacter))

charmatrix = outstream.getvalue().split()
ap = 0
for i in range(1, len(charmatrix)-1):
    for j in range(1, len(charmatrix[1]) - 1):
        if (charmatrix[i][j] == '#' and
            charmatrix[i+1][j] == '#' and
            charmatrix[i-1][j] == '#' and
            charmatrix[i][j-1] == '#' and
            charmatrix[i][j+1] == '#'):
            ap += i*j

print(ap)

turnL = {
    (0,1): (1,0),
    (1,0): (0,-1),
    (0,-1): (-1,0),
    (-1,0): (0,1)
}

turnR = {
    (0,1): (-1,0),
    (-1,0): (0,-1),
    (0,-1): (1,0),
    (1,0): (0,1)
}

toVisit = set()
for i in range(len(charmatrix)):
    for j in range(len(charmatrix[0])):
        if charmatrix[i][j] == '#':
            toVisit.add((j,i))

marked = set()

path = ['R', 0]

for line in charmatrix:
    print(line)

print(charmatrix[26][40])

def isscaff(x,y):
    return (y >= 0 and y < len(charmatrix) and x >= 0 and x < len(charmatrix[0])
            and charmatrix[y][x] == '#')

#this may not necessarily find the shortest path but hopefully
#it will at least be compressible
def scaffoldsearch(x, y, direc):
    print(x,y,charmatrix[y][x])
    #we have reached the end of our journey
    if len(toVisit) == 0:
        return True

    marked.add((x,y))
    if (x,y) in toVisit:
        toVisit.remove((x,y))

    nx, ny = x + direc[0], y + direc[1]

    wentforward = False

    if isscaff(nx, ny):
        if (nx, ny) in marked:
            #can I continue across this junction?
            nx2, ny2 = nx + direc[0], ny + direc[1]
            if (isscaff(nx2, ny2) and
                (nx2, ny2) not in marked):
                path[-1] += 2
                wentforward = True
                if scaffoldsearch(nx2, ny2, direc):
                    return True
        else:
            path[-1] += 1
            wentforward = True
            if scaffoldsearch(nx, ny, direc):
                return True


    nd = turnL[direc]
    nx, ny = x + nd[0], y + nd[1]

    wentleft = False

    if isscaff(nx, ny) and (nx,ny) not in marked:
        wentleft = True
        if wentforward:
            path.append('R')
        else:
            path.append('L')
        path.append(1)
        if scaffoldsearch(nx, ny, nd):
            return True

    nd = turnR[direc]
    nx, ny = x + nd[0], y + nd[1]

    wentright = False

    if isscaff(nx,ny) and (nx,ny) not in marked:
        wentright = True
        if wentleft:
            path[-1] += 1
        else:
            if wentforward:
                path.append('L')
            else:
                path.append('R')
            path.append(1)
        if scaffoldsearch(nx, ny, nd):
            return True

    if wentright:
        path.append('L')
        path.append(1)
    elif wentleft:
        path.append('R')
        path.append(1)
    elif wentforward:
        path[-1] += 1
    else:
        path.append('L')
        path.append('L')
        path.append(1)

    marked.remove((x,y))

    return False

print(path)

#A = R,4,L,12,L,8,R,4
#B = L,8,R,10,R,10,R,6
#C = R,4,R,10,L,12

#path = A,B,A,C,A,B,A,C,B,C

inputstring = "A,B,A,C,A,B,A,C,B,C\nR,4,L,12,L,8,R,4\nL,8,R,10,R,10,R,6\nR,4,R,10,L,12\nn\n"
intcomp = IntcodeComputer("inputday17_mod.txt", sys.stdout, inputstring)

intcomp.execute()