from math import floor

basepattern = [0,1,0,-1]
dbase = [1,1,-1,-1]

with open('inputday16.txt','r') as f:
	inputseq = f.read()

offset = int(inputseq[0:7])

inputseq *= 10000

#we can discard everything before the message offset

digits = [int(dig) for dig in inputseq]

for _ in range(100):
    cumsum = [0 for _ in range(len(digits))]
    fft = [0 for _ in range(len(digits))]

    cumsum[-1] = digits[-1]
    fft[-1] = cumsum[-1]

    #backwards cumulative sum. Last value and last digit of FFT
    #are just the last digit of the signal
    for reps in range(len(digits)-1,offset-1,-1):
        cumsum[reps-1] = cumsum[reps] + digits[reps-1]
        fft[reps-1] = abs(sum([dbase[(i+1) % 4] * cumsum[(i+1)*reps-1] for i in range(len(digits)//reps)]))%10
    digits = fft

    print(fft[offset:offset+8])