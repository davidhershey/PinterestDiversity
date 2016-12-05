import snap
import random
import pickle
import operator
from collections import defaultdict
# userfile = open('../data/users.tsv')
numToSample = 100000
# users = []
# for line in userfile:
#     users.append(int(line))
# userfile.close()

boardfile = open('../data/boards.tsv')
user2boards = {}
count = 0

for line in boardfile:
  count += 1
  if (count % 1000 == 0):
    print count
  
  board_id, board_name, board_description, user_id, board_create_time = line.split('\t')
  if (user2boards.get(user_id) == None):
    user2boards[user_id] = [board_id]
  else:
    user2boards[user_id].append(board_id)
boardfile.close()
print 'Pickling...'
pickle.dump(user2boards, open('../datastructures/user2boards.p', 'wb'))
print 'Loaded Boards'

print 'Sorting/Outputting'
sorted_tuples = sorted(user2boards.items(), key=operator.itemgetter(1), reverse=True)
f = open('../graphs/usersByBoards.txt', 'w')
for user in sorted_tuples:
  entry = user[0] + "\t" + str(user[1]) + "\n"
  f.write(entry)
f.close()
print 'Done'