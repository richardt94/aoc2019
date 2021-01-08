import itertools

with open('inputday7.txt','r') as f:
    intcode = f.read()

basecode = intcode.split(',')


def outsig(phase):
    #initialise amp computers
    amps = range(5)
    ampcode = [[i for i in basecode] for _ in amps]
    
    current_out = [0,0,0,0,0]
    initialised = [0,0,0,0,0]

    aidx = [0,0,0,0,0]
    
    current_amp = 0    

    done = [False, False, False, False, False]
    while sum(done) < 5:

        intcode = ampcode[current_amp]
        idx = aidx[current_amp]


        paused = False
        while not paused and not done[current_amp]:
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
                if mode:
                    params += [idx+1+x]
                else:
                    if len(intcode) > idx+1+x:
                        params += [int(intcode[idx+1+x])]
                    else:
                        #either something is wrong or the opcode doesn't need this parameter
                        params += [0]


            if opcode == 99:
                done[current_amp] = True
            elif opcode == 1:
                intcode[params[2]] = str(int(intcode[params[0]]) + int(intcode[params[1]]))
                idx += 4
            elif opcode == 2:
                intcode[params[2]] = str(int(intcode[params[0]]) * int(intcode[params[1]]))
                idx += 4
            elif opcode == 3:
                if initialised[current_amp]:
                    intcode[params[0]] = str(current_out[current_amp-1])
                else:
                    intcode[params[0]] = str(phase[current_amp])
                    initialised[current_amp] = True
                idx += 2
            elif opcode == 4:
                current_out[current_amp] = int(intcode[params[0]])
                idx += 2
                paused = True
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
            else:
                # print("error, invalid opcode!")
                done[current_amp] = True
        aidx[current_amp] = idx        
        current_amp = (current_amp + 1) % 5
        

    return current_out[-1]

#run the program on all the amps in succession for every possible phase

maxout = 0

phase = (9,7,8,5,6)
print(outsig(phase))


perms = itertools.permutations(range(5,10))

for perm in perms:

    sig = outsig(perm)
    if sig > maxout:
        maxout = sig
        maxphase = perm

print(maxout,maxphase)

