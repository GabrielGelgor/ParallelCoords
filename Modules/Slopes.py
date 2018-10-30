import Structs,fcns, copy
import numpy as np

class Slopes(Structs.rank_method):                                  #Inherits from rank_method to ensure consistency among all ranking methods utilizing this architecture.
    def linemaker(self, col1_t, col2_t):                            #Takes in two PC dimensions, and generates the line equations connecting them.  
        lines = []                                                  
        found = None

        col1 = col1_t[:]
        col2 = col2_t[:]


        col1 = copy.copy(fcns.sel_sort(col1))                       #A selection sort keeping track of which value belongs to what coordinate sorts every coordinate in ascending order.
        col2 = copy.copy(fcns.sel_sort(col2))

        for i in range(len(col1)):
            search = col1[i]
            for j in range(len(col2)):
                if col2[j] == search:
                    found = j
                    break
            
            lines.append(Structs.line(i,found))

        return(lines)


    def rank(self, perms):                                          #IN: an array of permutations. Every permutation is a 2D matrix with each row representing a coordinate and column representing a single dimension. Therefore, this is a 3D array.
        perm_score = []                                             #NOTE: Each permutation array is split into COLUMN VECTORS. Therefore the second dimension of your array SHOULD BE YOUR MATRIX COLUMNS.
        best = []

        for i in range(len(perms)):                                 #How this algorithm operates: Compares two dimensions in a permutation to one another, draws the lines for that segment, and determines how similar the slopes are to one another.
            for j in range(len(perms[i])-2):                        #More similar slopes means a more overall uniform direction for the segment.
                tot = 0                                             #NOTE: In most data I have found that the overall simmilarity of a permutation hovers around 50%. By ranking based on individual segments, pattern recognition can take form.
                pos = 0
                neg = 0
                neu = 0                                             #Problem: Dimension header is being put into the comparison. In Crossovers this was worked around by skipping the first element of each column. A similar mechanism must be put in place here.

                lines = self.linemaker(perms[i][j],perms[i][j+1])

                for k in range(len(lines)):
                    M = lines[k].getM()

                    if M > 0:
                        pos += 1
                    elif M < 0:
                        neg += 1
                    else:
                        neu += 1

                tot += (max(pos,neg,neu)/len(lines))

            perm_score.append(tot) 

        for i in range(len(perm_score)):                                    #This process sorts the crosses array into key-value entries (nodes) in ascending order. This makes it usable by the NDS algorithm. TODO: Improve efficiency by changing to heapsort.
            if i == 0:
                top = i
                best.append(Structs.entry(top,1-perm_score[top]))           #For the purposes of a uniform NDS minimzation, the complement of every permutation is taken.

            elif perm_score[i] == perm_score[top]:
                for j in range(len(best)):
                    if perm_score[i] != perm_score[best[j].getK()]:
                        best.insert(j,Structs.entry(i,1-perm_score[i]))
                        break
                    elif j == (len(best)-1):
                        best.append(Structs.entry(i,perm_score[i]))
                        break
                
                #best.append(i)

            elif perm_score[i] > perm_score[top]:
                top = i
                best.insert(0, Structs.entry(i,1-perm_score[i]))
            
            else:
                for j in range(len(best)):
                    if perm_score[i] >  perm_score[best[j].getK()]:
                        best.insert(j,Structs.entry(i,1-perm_score[i]))
                        break
                    elif j == (len(best)-1):
                        best.append(Structs.entry(i,1-perm_score[i]))
                        break
            
        print('Best similarity score: '+str(perm_score[top]*100)+'%')

        return(best)                                                         #OUT: A sorted array of key-value entries(nodes) that go from maximum similarity to minimum similarity.

                    