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

#part 2
def inidx(i, decksize):
    #trace the path backwards
    for ins in instrs[::-1]:
        if ins.startswith("deal into new stack"):
            i = decksize - i - 1
        elif ins.startswith("deal with increment"):
            inc = int(ins.split()[-1])
            m = 0
            while (m * decksize + i)%inc != 0:
                m += 1
            i = (m * decksize + i) // inc
        elif ins.startswith("cut"):
            n = int(ins.split()[-1])
            i = (i + n) % decksize
    return i

ds = 119315717514047
ii = 2020
print(inidx(ii, ds))
