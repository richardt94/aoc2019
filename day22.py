deck = list(range(10007))

with open("inputday22.txt") as f:
    instrs = f.readlines()

for ins in instrs:
    if ins.startswith("deal into new stack"):
        deck = deck[::-1]
    elif ins.startswith("deal with increment"):
        inc = int(ins.split()[-1])
        ndeck = deck.copy()
        for (i, card) in enumerate(deck):
            ndeck[(inc*i)%len(deck)] = card
        deck = ndeck
    elif ins.startswith("cut"):
        n = int(ins.split()[-1])
        deck = deck[n:] + deck[:n]

i = 0
while deck[i] != 2019:
    i += 1
print(i)

#use modular arithmetic to do the thing

with open("inputday22.txt") as f:
    instrs = f.readlines()

offset = 0
inc = 1
ds = 119315717514047

for ins in instrs:
    if ins.startswith("deal into new stack"):
        offset -= inc
        offset %= ds
        inc = ds - inc
    elif ins.startswith("deal with increment"):
        #replace with non-brute-force for actual input
        dinc = int(ins.split()[-1])
        i = 0
        while (i*ds + 1) % dinc:
            i += 1
        j = (i*ds + 1)//dinc
        inc = (inc * j) % ds
    elif ins.startswith("cut"):
        n = int(ins.split()[-1])
        offset += n * inc
        offset %= ds

#exponentiate by squaring
ntimes = 101741582076661
ioffset = offset
iinc = inc
offset = 0
inc = 1
while ntimes > 0:
    nsquares = 1
    noffset = ioffset
    ninc = iinc
    while (2**nsquares < ntimes):
        noffset = (noffset + noffset*ninc) % ds
        ninc = (ninc * ninc) % ds
        nsquares += 1
    offset = (offset + noffset*inc) % ds
    inc = (inc * ninc) % ds
    ntimes -= 2**(nsquares - 1)

print((offset + 2020 * inc) % ds)