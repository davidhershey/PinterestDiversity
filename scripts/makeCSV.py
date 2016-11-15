
old = open('../graphs/first50kGraph.txt')
new = open('../graphs/first50kGraph.csv','w')
new.write('source,target\n')
for line in old:
    src,dst,_ = line.split('\t')
    new.write('{},{}\n'.format(src,dst))

old.close()
new.close()
