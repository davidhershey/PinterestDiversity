import snap
import random
import pickle
import operator
from collections import defaultdict


pinfile = open('../data/pins.tsv')
boards2pins = {}
count = 0

for line in pinfile:
  count += 1
  if (count % 10000 == 0):
    print count
  time, board_id, pin_id = line.split('\t')
  
  if (boards2pins.get(board_id) == None):
    boards2pins[board_id] = 1
  else:
    boards2pins[board_id] += 1
pinfile.close()
print 'Loaded Pins'

print 'Sorting/Outputting'
sorted_tuples = sorted(boards2pins.items(), key=operator.itemgetter(1), reverse=True)
f = open('../graphs/boardsByPins.txt', 'w')
count = 0
for board in sorted_tuples:
  count += 1
  if (count % 10000 == 0):
    print count
  entry = board[0] + "\t" + str(board[1]) + "\n"
  f.write(entry)
f.close()
print 'Done'