import io

class IntcodeComputer:
    def __init__(self, fname, outstream, invals):
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
                self.stream.write(str(self.intcode[params[0]]))
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

def isbeam(x,y):
    outstream = io.StringIO()
    intcomp = IntcodeComputer("inputday19.txt", outstream, [x,y])
    intcomp.execute()
    return outstream.getvalue() == "1"

nfilled = 0
for y in range(50):
    s = ""
    for x in range(50):
        if isbeam(x,y):
            nfilled += 1
            s += "#"
        else:
            s += "."
    print(s)

print(nfilled)

x = 4
y = 5

found = False

while not found:
    print(x,y)
    if not isbeam(x,y):
        x += 1
        continue
    if not isbeam(x + 99, y):
        y += 1
        continue
    if not isbeam(x, y + 99):
        x += 1
        continue

    found = True

print(x * 10000 + y)