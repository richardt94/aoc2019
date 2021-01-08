class Painter:
    
    def __init__(self, x, y, vec):
        self.x = x
        self.y = y
        self.maxx = x
        self.minx = x
        self.maxy = y
        self.miny = y
        self.vec = vec
        self.colours = [[0 for _ in range(80)] for _ in range(150)]
        self.colours[self.x][self.y] = 1
        self.painted = [[False for _ in range(80)] for _ in range(150)]

    def paint(self,colour):
        self.colours[self.x][self.y] = colour
        self.painted[self.x][self.y] = True

    def turn_and_move(self,direction):
        self.vec = (self.vec + 2*direction - 1) % 4
        if self.vec == 0:
            self.y -= 1
        elif self.vec == 1:
            self.x += 1
        elif self.vec == 2:
            self.y += 1
        else:
            self.x -= 1
        if self.x > self.maxx:
            self.maxx = self.x
        elif self.x < self.minx:
            self.minx = self.x
        elif self.y > self.maxy:
            self.maxy = self.y
        elif self.y < self.miny:
            self.miny = self.y

    def get_colour(self):
        return self.colours[self.x][self.y]

    def num_painted(self):
        return sum([sum(col) for col in self.painted])

    def get_image(self):
        return self.colours

    def get_minmax(self):
        return [[self.minx,self.maxx],[self.miny,self.maxy]]


ptr = Painter(75,40,0)

with open('inputday11.txt','r') as f:
    intcode = f.read()

intcode = intcode.split(',')

#add memory
intcode = intcode + ['0']*500

idx = 0
rbase = 0

done = False

painting = True

while not done:
    opcode = int(intcode[idx][-2:])
    param_modes = [int(c) for c in intcode[idx][:-2]]
    #deal with possible leading zeros
    while len(param_modes) < 3:
        param_modes = [0] + param_modes
    
    #reverse
    param_modes = param_modes[::-1]

    #compute argument pointers
    params = []
    for x,mode in enumerate(param_modes):
        if mode == 2:
            params += [int(intcode[idx+1+x])+rbase]
        elif mode:
            params += [idx+1+x]
        else:
            if len(intcode) > idx+1+x:
                params += [int(intcode[idx+1+x])]
            else:
                #either something is wrong or the opcode doesn't need this parameter
                params += [0]


    if opcode == 99:
        done = True
    elif opcode == 1:
        intcode[params[2]] = str(int(intcode[params[0]]) + int(intcode[params[1]]))
        idx += 4
    elif opcode == 2:
        intcode[params[2]] = str(int(intcode[params[0]]) * int(intcode[params[1]]))
        idx += 4
    elif opcode == 3:
        intcode[params[0]] = ptr.get_colour()
        idx += 2
    elif opcode == 4:
        if painting: 
            ptr.paint(int(intcode[params[0]]))
            painting = False
        else:
            ptr.turn_and_move(int(intcode[params[0]]))
            painting = True
        idx += 2
    elif opcode == 5:
        if int(intcode[params[0]]):
            idx = int(intcode[params[1]])
        else:
            idx += 3
    elif opcode == 6:
        if not int(intcode[params[0]]):
            idx = int(intcode[params[1]])
        else:
            idx += 3
    elif opcode == 7:
        intcode[params[2]] = str(int(int(intcode[params[0]]) < int(intcode[params[1]])))
        idx += 4
    elif opcode == 8:
        intcode[params[2]] = str(int(int(intcode[params[0]]) == int(intcode[params[1]])))
        idx += 4
    elif opcode == 9:
        rbase += int(intcode[params[0]])
        idx += 2
        
    else:
        print("error, invalid opcode!")
        done = True


print(ptr.num_painted())

image = ptr.get_image()

for y in range(len(image[0])):
    scanline = ''
    for x in range(len(image)):
        scanline += '#' if image[x][y] else ' '
    print(scanline)

print(ptr.get_minmax())