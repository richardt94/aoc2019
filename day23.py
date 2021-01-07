from collections import deque

class IntcodeComputerNIC:
    def __init__(self, fname, addr):
        with open(fname,'r') as f:
            codestring = f.read()

        self.intcode = [int(code) for code in codestring.split(',')]

        #add memory
        self.intcode = self.intcode + [0]*5000

        self.idx = 0
        self.rbase = 0
        self.addr = addr
        self.invals = deque([addr])
        self.outbuffer = []

    #execute until a packet send or recv instruction
    def execute(self):
        while True:
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
                return [0]
            elif opcode == 1:
                self.intcode[params[2]] = self.intcode[params[0]] + self.intcode[params[1]]
                self.idx += 4
            elif opcode == 2:
                self.intcode[params[2]] = self.intcode[params[0]] * self.intcode[params[1]]
                self.idx += 4
            elif opcode == 3:
                #input values from the network buffer
                idle = False
                if len(self.invals) == 0:
                    self.intcode[params[0]] = -1
                    idle = True
                else:
                    self.intcode[params[0]] = self.invals.popleft()
                self.idx += 2
                if idle:
                    return [0]
                else:
                    return [1]
            elif opcode == 4:
                self.idx += 2
                self.outbuffer.append(self.intcode[params[0]])
                if len(self.outbuffer) == 3: # packet is ready
                    ret = self.outbuffer
                    self.outbuffer = []
                    return ret
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
                return []
        return []

    def recv(self, packet):
        [self.invals.append(val) for val in packet]

#initialise networked computers
comps = []
for i in range(50):
    comps.append(IntcodeComputerNIC("inputday23.txt", i))

#emulate all computers simultaneously
done = False
natpack = [-1, -1]
alreadysent = False
while not done:
    idle = [False for _ in range(50)]
    for i in range(50):
        packet = comps[i].execute()
        if len(packet) == 3:
            addr = packet[0]
            print("computer", i, "sending packet to computer", addr)
            if addr == 255:
                alreadysent = natpack[1] == packet[2] and alreadysent
                natpack = packet[1:]
            else:
                comps[addr].recv(packet[1:])
        elif not packet[0]:
            idle[i] = True

    alli = True
    for compidle in idle:
        alli &= compidle
    if alli:
        print("sending NAT packet", natpack)
        comps[0].recv(natpack)
        if alreadysent:
            print(natpack[1])
            done = True
        alreadysent = True
