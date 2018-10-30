import Structs, random

class NDS():                                                                            #Class to handle non-dominated sorting.
    
    def __init__(self, ranks):
        self.ranks = ranks                                                              #Array of ranks, input as a set of entries where the K is the 


    def pointMaker(self):                                                               #Turns every single permutation into a set of points, with each dimension being their ranking.
        sample = []                                                                     #Sample: A list of entires that will be used as a reference point so tehat all relevant rankings for permutations can be gathered
        dims = []                                                                       #Dims: A 2D entry list containing all other permutation ranking methods and their results
        pnts = []                                                                       #Pnts: The final list containing an entry for every permutation, Key being perm number and Value being an array with ranking information from each method.

        for i in range(len(self.ranks)):                                                #A loop that dumps the first ranking method into Sample, and the rest into Dims.
            if i == 0:
                sample = self.ranks[i]
            else:
                dims.append(self.ranks[i])

        for i in range(len(sample)):                                                    #The loop that looks at the current permutation, retrieves its rankings, and then compiles them into a list. This list is then used as the Value for that permutation's entry
            cur = []                                                                    #Cur: List of all rankings for current permutation. Used as Value for permutation's entry.
            cur.append(sample[i].getV())#i                                              #Currently, rank of the permutation is being placed into Cur, which results in no dominating points! Should be changed to metric disicovered during ranking process.

            for j in range(len(dims)):                                                  #A loop that compares perm numbers, trying to find the rankings that belong together.
                for k in range(len(dims[j])):
                    if dims[j][k].getK() == sample[i].getK():
                        cur.append(dims[j][k].getV()) #k                                #Once again, conglomerates rankings, shoud be changed to metric
                        break
                    
            pnts.append(Structs.entry(sample[i].getK(),cur[:]))                         #Line that generates entry.
        
        return(pnts)

    def Sort(self):                                                                    
        pf = []                                                                         #pf: Array containing points within the Pareto Front
        pnts = self.pointMaker()                                                        #pnts: Array containing all points on the ranking graph



        for i in range(len(pnts)):
            for j in range (len(pnts)):
                domD = 0
                recip = 0

                if i == j:
                    continue
                
                else:
                    for k in range(len(pnts[i].getV())):
                        if (pnts[i].getV()[k] >= pnts[j].getV()[k]):
                            domD += 1
                            if (pnts[i].getV()[k] == pnts[j].getV()[k]):
                                recip += 1
                        else:
                            break

                    if (domD == len(pnts[i].getV()) and recip != domD):
                        break

                    elif j == (len(pnts)-1):
                        pf.append(pnts[i])


        sample_found = False
        sample = None

        while (sample_found == False):
            rand = random.randint(0,len(self.ranks[0])-1)
            for i in range(len(pf)):
                if (pf[i].getK() == rand):
                    print(self.ranks[0][i].getK())
                    break
                
                elif (i == len(pf)-1):
                    sample = self.ranks[0][3]
                    sample_found = True

    
#        for i in range (len(pf)):
#            print(pf[i].getAll())

        return(pf,sample)

'''
    def Sort(self):                                                                     #Simple sorter that adds rankings together and picks the lowest number from that. Not true NDS.
        mins = []
        pnts = self.pointMaker()

        for i in range(len(pnts)):
            pnts[i].ent[1] = sum(pnts[i].getV())
        
        for i in range(len(pnts)):
            if i == 0:
                _min = pnts[i].getV()
                mins.append(pnts[i].getK())

            elif pnts[i].getV() < _min:
                del mins[:]

                _min = pnts[i].getV()
                mins.append(pnts[i].getK())

            elif pnts[i].getV() == _min:
                mins.append(pnts[i].getK())

        sample_found = False

        while (sample_found == False):
            rand = random.randint(0,len(pnts))
            for i in range(len(mins)):
                if (mins[i] == rand):
                    break
                
                elif (i == len(mins)-1):
                    mins.append(pnts[rand].getK())
                    sample_found = True

        return(mins)
        


            sample_found = False

        while (sample_found == False):
            rand = random.randint(0,len(pnts))
            for i in range(len(pf)):
                if (pf[i].getK() == rand):
                    break
                
                elif (i == len(pf)-1):
                    pf.append(pnts[rand])
                    sample_found = True

'''