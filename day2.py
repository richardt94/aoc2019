freq = 0

with open('inputday2.txt','r') as f:
    intcode = f.read()

intcode = intcode.split(',')

intcode = [int(code) for code in intcode]

backup = [i for i in intcode]

ir = range(100)

for i1 in ir:
    for i2 in ir:
        intcode = [i for i in backup]    

        intcode[1]=i1
        intcode[2]=i2

        idx = 0

        done = False
        while not done:
            opcode = intcode[idx]
            if opcode == 99:
                done = True
            elif opcode == 1:
                intcode[intcode[idx+3]] = intcode[intcode[idx+1]] + intcode[intcode[idx+2]]
                idx += 4
            elif opcode == 2:
                intcode[intcode[idx+3]] = intcode[intcode[idx+1]] * intcode[intcode[idx+2]]
                idx += 4
            else:
                print("error, invalid opcode!")
                done = True
        if intcode[0] == 19690720:
            print i1,i2
            break

    else:
        continue
    break
