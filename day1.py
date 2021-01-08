freq = 0

with open('inputday1.txt','r') as f:
   masses = f.readlines()

masses = [int(mass) for mass in masses]

fuel = 0
for mass in masses:
   addfuel = mass//3 - 2
   fuel += addfuel
   addfuel = addfuel//3 - 2
   while addfuel > 0:
      fuel += addfuel
      addfuel = addfuel//3 - 2
   

print(fuel)
