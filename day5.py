freq = 0

with open('inputday5.txt','r') as f:
    intcode = f.read()

intcode = intcode.split(',')

backup = [i for i in intcode]



idx = 0

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
        if mode:
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
        intcode[params[0]] = str(int(raw_input('opcode 3 value:')))
        idx += 2
    elif opcode == 4:
        print(intcode[params[0]])
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
    else:
        print("error, invalid opcode!")
        done = True


