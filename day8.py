with open('inputday8.txt','r') as f:
    imagedata = f.read()

imagedata = [int(c) for c in imagedata[:-1]]

w = 25
h = 6

nlayers = len(imagedata)//(w*h)

minlayer = 0
minz = w*h

for layer in range(nlayers):
    nz = sum([px==0 for px in imagedata[layer*w*h:(layer+1)*w*h]])
    if nz < minz:
        minlayer = layer
        minz = nz

n1 = sum([px==1 for px in imagedata[minlayer*w*h:(minlayer+1)*w*h]])
n2 = sum([px==2 for px in imagedata[minlayer*w*h:(minlayer+1)*w*h]])

assert(minz+n1+n2 == w*h)

print(n1*n2)

finimg = [2 for _ in range(w*h)]

for layer in range(nlayers):
    finimg = [imagedata[layer*w*h+i] if finimg[i] == 2 else finimg[i] for i in range(w*h)]

printchars = [' ','#']

for z in range(h):
    pstr = ''
    for x in range(w):
        pstr += printchars[finimg[z*w+x]]
    print(pstr)

