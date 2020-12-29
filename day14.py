import re
from math import ceil
with open('inputday14.txt','r') as f:
	reactionlist = f.readlines()

reactionlist = [reaction.split('=>') for reaction in reactionlist]


reactant_regex = re.compile('([0-9]+) ([A-Z]+)')

ingredient_dict = {}
for reaction in reactionlist:
	if len(reaction) != 2:
		continue
	reactant_list = reactant_regex.findall(reaction[0])

	product = reactant_regex.search(reaction[1]).groups()

	ingredient_dict[product[1]] = [product[0],reactant_list]

target = 'FUEL'

origin = 'ORE'

remainder = {}
def amount_of_ore(quantity, target):
	#print('producing',quantity,target)
	if target == origin:
		return quantity

	required = 0
	multiplier, ingredients = ingredient_dict[target]
	multiplier = int(multiplier)
	#print('need to produce',multiplier,target,'at a time')
	num_reacts = ceil(quantity / multiplier)
	for quant, ingredient in ingredients:
		quant = int(quant)*num_reacts
		#print('need',quant,ingredient)
		if ingredient in remainder:
			#print('there are',remainder[ingredient],ingredient,'left over')
			if quant > remainder[ingredient]:
				quant -= remainder[ingredient]
				remainder[ingredient] = 0
			else:
				remainder[ingredient]-= quant
				continue
		required += amount_of_ore(quant, ingredient)

	overprod = multiplier * num_reacts - quantity

	remainder[target] = remainder[target] + overprod if target in remainder else overprod

	#print(required,origin,'required for',quantity,target)

	return required


or_supply = 10**12
reqforone = amount_of_ore(1,target)
min_tar = or_supply//reqforone

#reset remainder
remainder = {}

req_for_min = amount_of_ore(min_tar,target)
print (req_for_min,origin,'required for',min_tar,target)


or_supply -= req_for_min
fuelct = min_tar
next_tar = or_supply // reqforone
while next_tar > 0:
	or_inc = amount_of_ore(next_tar,target)
	fuelct += next_tar
	or_supply -= or_inc
	next_tar = or_supply // reqforone

while 1:
	or_inc = amount_of_ore(1,target)
	or_supply -= or_inc
	if or_supply >= 0:
		fuelct += 1
	else:
		break

print(fuelct)