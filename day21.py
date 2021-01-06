import sys

class IntcodeComputer:
    def __init__(self, fname, outstream, invals, asc=False):
        with open(fname,'r') as f:
            codestring = f.read()

        self.intcode = [int(code) for code in codestring.split(',')]

        #add memory
        self.intcode = self.intcode + [0]*5000

        self.idx = 0
        self.rbase = 0
        self.done = False
        self.stream = outstream
        self.invals = invals
        self.inidx = 0
        self.ascii = asc

    def execute(self):
        while not self.done:
            instruction = self.intcode[self.idx]
            opcode = instruction % 100
            # print("executing opcode", opcode, "at address", self.idx)
            param_modes = [(instruction // (10 ** n)) % 10 for n in range(2,5)]

            #compute argument pointers
            params = []
            for x,mode in enumerate(param_modes):
                if mode == 2:
                    params += [self.intcode[self.idx+1+x]+self.rbase]
                elif mode:
                    params += [self.idx+1+x]
                else:
                    if len(self.intcode) > self.idx+1+x:
                        params += [self.intcode[self.idx+1+x]]
                    else:
                        #either something is wrong or the opcode doesn't need this parameter
                        params += [0]

            if opcode == 99:
                self.done = True
            elif opcode == 1:
                self.intcode[params[2]] = self.intcode[params[0]] + self.intcode[params[1]]
                self.idx += 4
            elif opcode == 2:
                self.intcode[params[2]] = self.intcode[params[0]] * self.intcode[params[1]]
                self.idx += 4
            elif opcode == 3:
                #intcode[params[0]] = str(int(input('opcode 3 value:')))
                self.intcode[params[0]] = self.invals[self.inidx]
                self.inidx += 1
                self.idx += 2
            elif opcode == 4:
                self.idx += 2
                val = self.intcode[params[0]]
                if self.ascii and val < 256:
                    self.stream.write(chr(val))
                else:
                    self.stream.write(str(val))
            elif opcode == 5:
                if self.intcode[params[0]]:
                    self.idx = self.intcode[params[1]]
                else:
                    self.idx += 3
            elif opcode == 6:
                if not self.intcode[params[0]]:
                    self.idx = self.intcode[params[1]]
                else:
                    self.idx += 3
            elif opcode == 7:
                self.intcode[params[2]] = int(self.intcode[params[0]] < self.intcode[params[1]])
                self.idx += 4
            elif opcode == 8:
                self.intcode[params[2]] = int(self.intcode[params[0]] == self.intcode[params[1]])
                self.idx += 4
            elif opcode == 9:
                self.rbase += self.intcode[params[0]]
                self.idx += 2
                
            else:
                print("error, invalid opcode!")
                self.done = True
        return 99


# inst = input()
# prog = inst + "\n"
# while inst != "WALK":
#     inst = input()
#     prog += inst + "\n"

#can i jump now and cross a hole? Will the jump strand me?
#a jump that crosses a hole means (!A or !B or !C) and D
#I am not stranded after the jump only iff (E and (F or I)) or H
prog = \
"""NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT I T
AND I T
OR I T
OR F T
AND E T
OR H T
AND T J
RUN
"""

#part 1 program
"""NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

intcomp = IntcodeComputer("inputday21.txt", sys.stdout, [ord(c) for c in prog], asc=True)
intcomp.execute()