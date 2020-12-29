class Map:
    displaychars = ['#','.','X','O']
    def __init__(self):
        self.displaydict = {}
        self.distdict = {}
        self.target_position = (0,0)

    def show(self):
        xvals = [coords[0] for coords in self.displaydict]
        yvals = [coords[1] for coords in self.displaydict]

        xr = range(min(xvals),max(xvals)+1)
        yr = range(min(xvals),max(yvals)+1)

        for y in yr:
            linestr = ''
            for x in xr:
                if (x,y) in self.displaydict:
                    linestr+= self.displaychars[self.displaydict[(x,y)]]
                else:
                    linestr+= ' '
            print(linestr)

    def show_dist(self):
        xvals = [coords[0] for coords in self.displaydict]
        yvals = [coords[1] for coords in self.displaydict]

        xr = range(min(xvals),max(xvals)+1)
        yr = range(min(xvals),max(yvals)+1)

        for y in yr:
            linestr = ''
            for x in xr:
                if (x,y) in self.distdict:
                    if not self.displaydict[(x,y)]:
                        diststr = '....'
                        linestr += diststr
                        continue
                    if self.distdict[(x,y)]:
                        diststr = str(self.distdict[(x,y)])
                        diststr = '0'*(3-len(diststr))+diststr+','
                    else:
                        diststr = '....'
                        if (x,y) == (0,0) or (x,y) == self.target_position:
                            diststr = '000,'
                else:
                    diststr = '....'
                linestr += diststr
            print(linestr)

    def update(self,pos,val,dist):
        self.displaydict[pos] = val
        self.distdict[pos] = dist
        if val == 2:
            self.target_position = pos

    def explored(self,pos):
        return pos in self.distdict

    def get_dist(self,pos):
        return self.distdict[pos]

    def get_target(self):
        return self.target_position

    def dist_to_target(self):
        return self.get_dist(self.target_position)

    def max_dist(self):
        ret = 0
        for pos in self.distdict:
            if self.displaydict[pos] == 1 and self.distdict[pos] > ret:
                ret = self.distdict[pos]
        return ret

    vecs = [(0,1),(0,-1),(1,0),(-1,0)]
    def _dfsdist(self,pos,dist,back):
        self.distdict[pos] = dist
        for vec in self.vecs:
            if vec == back:
                continue
            newpos = (pos[0] + vec[0],pos[1] + vec[1])
            if newpos in self.displaydict:
                if newpos in self.distdict:
                    if self.distdict[newpos] <= dist + 1:
                        continue
                if self.displaydict[newpos] == 0:
                    continue
                self._dfsdist(newpos,dist+1,(-pos[0],-pos[1]))



    def dists_from_target(self):
        self.distdict = {}
        self._dfsdist(self.target_position,0,(0,0))


class IntcodeComputer:
    def __init__(self):
        with open('inputday15.txt','r') as f:
            self.intcode = f.read()

        self.intcode = self.intcode.split(',')

        #add memory
        self.intcode = self.intcode + ['0']*500

        self.idx = 0
        self.rbase = 0
        self.done = False

    def execute(self,inputval):
        while not self.done:
            opcode = int(self.intcode[self.idx][-2:])
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
                self.intcode[params[0]] = str(inputval)
                self.idx += 2
            elif opcode == 4:
                self.idx += 2
                return int(self.intcode[params[0]])
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

m = Map()
comp = IntcodeComputer()

dirlist = [(0,-1),(0,1),(-1,0),(1,0)]

fliplist = [2,1,4,3]

#recursively traverse the maze depth-first
def explore(returndir,pos,dist):
    m.update(pos,1,dist)

    if pos == (0,0):
        m.update(pos,3,dist)

    for direction in range(1,5):
        #don't go backwards
        if direction == returndir:
            continue
        reversedir = fliplist[direction-1]
        vec = dirlist[direction-1]
        newpos = (pos[0]+vec[0],pos[1]+vec[1])
        if m.explored(newpos):
            if dist >= m.get_dist(newpos):
                #this path was not better than the previous best, stop exploring here
                continue
        ret = comp.execute(direction)
        if ret == 0:
            m.update(newpos,0,dist+1)
        elif ret == 2:
            #keep exploring to ensure a complete map
            explore(reversedir,newpos,dist+1)
            #the target was found here
            m.update(newpos,2,dist+1)
            comp.execute(reversedir)
        elif ret == 1:
            #explore from the new position
            explore(reversedir,newpos,dist+1)
            #reverse the move to keep exploring
            comp.execute(reversedir)


explore(0,(0,0),0)

m.show()
print(m.dist_to_target())

#there should now be a complete map available

m.dists_from_target()
m.show_dist()
print(m.max_dist())