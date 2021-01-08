import os

class Display:
    displaychars = [' ','X','#','_','O']
    def __init__(self):
        self.outputctr = 0
        self.displaydict = {}
    def output(self,val):
        if self.outputctr == 0:
            self.x = val
            self.outputctr += 1
        elif self.outputctr == 1:
            self.y = val
            self.outputctr += 1
        else:
            self.displaydict[(self.x,self.y)] = val
            self.outputctr = 0

    def count(self,val):
        ctr = 0
        for tup in self.displaydict:
            if self.displaydict[tup] == val:
                ctr += 1
        return ctr

    def show(self):
        os.system("cls")
        xvals = [coords[0] for coords in self.displaydict]
        yvals = [coords[1] for coords in self.displaydict]

        xr = range(max(xvals)+1)
        yr = range(max(yvals)+1)

        print('score',self.displaydict[(-1,0)])

        for y in yr:
            linestr = ''
            for x in xr:
                if (x,y) in self.displaydict:
                    linestr+= self.displaychars[self.displaydict[(x,y)]]
                else:
                    linestr+= ' '
            print(linestr)
    def find(self,val):
        retval = (-1,-1)
        for tup in self.displaydict:
            if self.displaydict[tup] == val:
                retval = tup
                break
        return retval


class AutoJoystick:
    def __init__(self,disp):
        self.disp = disp

    def get_input(self):
        ballpos = self.disp.find(4)
        paddlepos = self.disp.find(3)

        instr = '0'
        if paddlepos[0] < ballpos[0]:
            instr = '1'
        elif paddlepos[0] > ballpos[0]:
            instr = '-1'

        return instr


disp = Display()
joy = AutoJoystick(disp)

with open('inputday13.txt','r') as f:
    intcode = f.read()

intcode = intcode.split(',')

#free money
intcode[0] = '2'

#add memory
intcode = intcode + ['0']*500

idx = 0
rbase = 0

done = False
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
        disp.show()
        #intcode[params[0]] = str(int(input('opcode 3 value:')))
        intcode[params[0]] = joy.get_input()
        idx += 2
    elif opcode == 4:
        disp.output(int(intcode[params[0]]))
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

disp.show()