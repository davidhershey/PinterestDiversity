f1 = open('../graphs/usersByBoards.txt')
o1 = open('../graphs/top100usersByBoards.txt', 'w')
mostBoards = {}
count = 0
for line in f1:
	count += 1
	user_id, num_boards = line.split('\t')
	mostBoards[user_id] = count
	o1.write(line)
	if (count == 100):
		break
f1.close()
o1.close()

mostPins = {}
f2 = open('../graphs/usersByPins.txt')
o2 = open('../graphs/top100usersByPins.txt', 'w')
count = 0
for line in f2:
	count += 1
	user_id, num_pins = line.split('\t')
	mostPins[user_id] = count
	o2.write(line)
	if (count == 100):
		break
f2.close()
o2.close()

intersection = set(mostBoards.keys()) & set(mostPins.keys())
for elem in intersection:
	print elem + ": " + str(mostBoards[elem]) + ", " + str(mostPins[elem])
