# Get % of followers that follow a user after a specified user follows that user
#
# Node: 9512301   InDeg: 110      OutDeg: 83
# Node: 7297014   InDeg: 103      OutDeg: 60
# Node: 4928477   InDeg: 53       OutDeg: 265
# Node: 13074048  InDeg: 52       OutDeg: 53
# Node: 5072565   InDeg: 45       OutDeg: 318
# Node: 2886137   InDeg: 42       OutDeg: 85
# Node: 12521800  InDeg: 36       OutDeg: 263
# Node: 9471321   InDeg: 35       OutDeg: 117
# Node: 13684676  InDeg: 35       OutDeg: 47
# Node: 12608616  InDeg: 51       OutDeg: 35
# Node: 7318553   InDeg: 438      OutDeg: 35
# Node: 7402575   InDeg: 32       OutDeg: 74
# Node: 7431024   InDeg: 30       OutDeg: 35
# Node: 12420637  InDeg: 26       OutDeg: 859
# Node: 3534431   InDeg: 25       OutDeg: 25
# Node: 2667151   InDeg: 27       OutDeg: 24
# Node: 5115048   InDeg: 25       OutDeg: 24
# Node: 3454404   InDeg: 24       OutDeg: 27
# Node: 3452897   InDeg: 29       OutDeg: 24
# Node: 7616387   InDeg: 27       OutDeg: 24

#Results:
# Node: 9512301	Uptake Rate: 0.008415246664406987
# Node: 7297014	Uptake Rate: 0.014230418943533697
# Node: 4928477	Uptake Rate: 0.01684352896996575
# Node: 13074048	Uptake Rate: 0.019167836134388282
# Node: 5072565	Uptake Rate: 0.0038475081812368753
# Node: 2886137	Uptake Rate: 0.0019198935753609238
# Node: 12521800	Uptake Rate: 0.00469566766813415
# Node: 9471321	Uptake Rate: 0.031165949931363717
# Node: 13684676	Uptake Rate: 0.0
# Node: 12608616	Uptake Rate: 0.007626901152301152
# Node: 7318553	Uptake Rate: 0.05355247582458173
# Node: 7402575	Uptake Rate: 0.03561872256279377
# Node: 7431024	Uptake Rate: 0.06780427075564467
# Node: 12420637	Uptake Rate: 0.006338119260121586
# Node: 3534431	Uptake Rate: 0.09261441537175955
# Node: 2667151	Uptake Rate: 0.0
# Node: 5115048	Uptake Rate: 0.007284660886475975
# Node: 3454404	Uptake Rate: 0.01813639035861258
# Node: 3452897	Uptake Rate: 0.09194732322632747
# Node: 7616387	Uptake Rate: 0.0118402465220901


import pickle


def calculateUptakeRate(leader):
    followers = []

    following = []
    countAtFollow = {}
    uptake = {}
    uptakeDates = {}
    kk = 0

    followfile = open('../graphs/fullEdgesByDate.txt')
    for line in followfile:
        if kk % 1000000 == 0:
            print kk
        if kk > 7000000:
            break
        kk+=1

        src,dst,date = line.split('\t')
        src = int(src)
        dst = int(dst)
        if dst == leader: #Someone followed our leader
            if src not in followers:
                followers.append(src)
                # print src, " is now following the leader!  We now have ",len(followers)," followers."

        if src == leader: #leader is following someone
            if dst not in following:
                following.append(dst)
                countAtFollow[dst] = max(1,len(followers))
                uptake[dst] = []
                uptakeDates[dst] = []
                # print "Our fearless leader is now following ", dst

        if src in followers:
            if dst in following:
                if src not in uptake[dst]:
                    # print src, " FOLLOWED OUR LEAD AND FOLLOWED ", dst
                    uptake[dst].append(src)
                    uptakeDates[dst].append(date)

    pickle.dump(uptake,open('uptakePickles/uptake{}.p'.format(leader),'w'))
    pickle.dump(uptakeDates,open('uptakePickles/uptakeDates{}.p'.format(leader),'w'))
    pickle.dump(countAtFollow,open('uptakePickles/countAtFollow{}.p'.format(leader),'w'))
    # print uptake
    count = 0
    meanPct = 0.0
    for key in uptake:
        count+=1
        # print "After following ", key
        # print len(uptake[key]),"/",countAtFollow[key], " uptook."
        pct = float(len(uptake[key]))/float(countAtFollow[key])
        meanPct +=pct

    print "average uptake for ",leader," = ",meanPct/float(count)
    return meanPct/float(count)

leaders = [9512301,7297014,4928477,13074048,5072565,2886137,12521800,9471321,13684676,12608616,7318553,7402575,7431024,12420637,3534431,2667151,5115048,3454404,3452897,7616387]

rates = []
for leader in leaders:
    rate = calculateUptakeRate(leader)

    rates.append((leader,rate))

print rates
