freq = 0

with open('input1.txt','r') as f:
   deltas = f.readlines()

deltas = [int(delta) for delta in deltas]

freqs = []

for delta in deltas:
   freq += delta
   freqs.append(freq)

cumdelta = [freq for freq in freqs]

done = False

while not done:
   frequpdate = [freqs[-1]+change for change in cumdelta]

   for freq in frequpdate:
      if freq in freqs:
         done = True
         break
   freqs += frequpdate
   print len(freqs)
print(freq)
