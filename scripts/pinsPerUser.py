import snap
import random
import pickle
import operator
from collections import defaultdict

# load users to boards
print 'Unpickling'
u2b = open('../datastructures/user2boards.p', 'rb')
user2boards = pickle.load(u2b) # dict of user_ids to arrays
u2b.close()
print 'Unpickled'

print 'Loading boards'
#load boards-->pins
boards2pins = {}
count = 0
f = open('../graphs/boardsByPins.txt')
for line in f:
  count += 1
  if (count % 10000 == 0):
    print count
  board_id, num_pins = line.split('\t')
  num_pins = int(num_pins)
  boards2pins[board_id] = num_pins
f.close()
print len(boards2pins) # 12,372,073
print 'Done loading boards'
#get pins per user
count = 0
nf = 0
found = 0
user2pins = {}
for user in user2boards.keys():
  count += 1
  pins = 0
  if (count % 10000 == 0):
    print count
  for board in user2boards[user]:
    if (boards2pins.get(board) != None):
      pins += boards2pins[board]
      found += 1
    else:
      nf += 1
      print int(board)
      
  if (user2pins.get(user) == None):
    user2pins[user] = pins
  else:
    user2pins[user] += pins
print nf

print 'Sorting/Outputting'
sorted_tuples = sorted(user2pins.items(), key=operator.itemgetter(1), reverse=True)
f = open('../graphs/usersByPins.txt', 'w')
for user in sorted_tuples:
  entry = user[0] + "\t" + str(user[1]) + "\n"
  f.write(entry)
f.close()
print 'Done'