xctr = 0
for x in range(183564,657474):
    x = str(x)
    x = [int(dig) for dig in x]
    rep = False
    for idx in range(len(x)-1):
        if x[idx] > x[idx+1]:
            break
        if x[idx] == x[idx+1]:
            if idx > 0 and idx < len(x) - 2:
                if x[idx] != x[idx-1] and x[idx] != x[idx+2]:
                    rep = True
            elif idx > 0:
                if x[idx] != x[idx-1]:
                    rep = True
            elif idx < len(x) - 2:
                if x[idx] != x[idx+2]:
                    rep = True


    else:
        if rep:
            xctr += 1

print xctr
        
