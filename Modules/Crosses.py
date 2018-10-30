import itertools, copy, Structs, fcns, pandas, random
import numpy as np
                                                                                            #Attempts to achieve PC clutter reduction via the minimization of crossing lines in a PC visualzation.
class Crossover(Structs.rank_method):                                                       #Inherits from rank_method to ensure consistency among all ranking methods utilizing this architecture.
    def rank(self, perms):                                                                  #IN: an array of permutations. Every permutation is a 2D matrix with each row representing a coordinate and column representing a single dimension. Therefore, this is a 3D array.
        min_taken = []                                                                      #NOTE: Each permutation array is split into COLUMN VECTORS. Therefore the second dimension of your array SHOULD BE YOUR MATRIX COLUMNS.
        min_perm = []
        crosses = []
        temp = []

        for i in range(len(perms)):                                                         #This loop follows the following procedure:
            cross = 0                                                                       #The current PERMUTATION (i) is taken in. number of cross overs is set to 0.
            
            for j in range(len(perms[i])):                                                  #The current ROW (j) is taken in. The goal is to see how many times coordinates will cross over each other as they progress.
                                                                                            #Example: p1(1,3) will cross over the coordinate p2(3,1) once as p1.x < p2.x while p1.y > p2.y                
                for k in range(1, len(perms[i][j])):                                        
                    temp.append(perms[i][j][k])

                if j == 0:
                    prev_vec = copy.copy(fcns.sel_sort(temp))                               #Dimensions are compared two at a time - a selection sort keeping track of which value belongs to what coordinate sorts every coordinate in ascending order.
                    continue                                                                #The two sorted dimensions are then passed to the next part of the algorithm:

                elif j == 1:
                    cur_vec = copy.copy(fcns.sel_sort(temp))

                else:
                    prev_vec = copy.copy(cur_vec)
                    cur_vec = copy.copy(fcns.sel_sort(temp))
                
                if (i > 0):
                    cross += fcns.get_Cross(prev_vec,cur_vec,min_cross)                     #By generating the line equation for every coordinate between these two dimensions on the PC, we can figure out how many cross-overs occur through simple equations.
                    if (cross > min_cross):
                        break
                else:
                    cross += fcns.get_Cross(prev_vec,cur_vec,-1)

            crosses.append(cross)                                                           #Counting of all cross-overs in this permutation has completed. The number is to an array index corresponding to the permutation number.

            if (i == 0):                                                                    #This process sorts the crosses array into key-value entries (nodes) in ascending order. This makes it usable by the NDS algorithm. TODO: Improve efficiency by changing to heapsort.
                min_cross = cross
                min_perm.append(Structs.entry(i,crosses[i]))
                min_taken = [i]

            elif (cross < min_cross):
                del min_taken[:]

                min_perm.insert(0,Structs.entry(i,crosses[i]))
                min_taken.append(i)
                min_cross = cross

            elif (cross == min_cross):
                for j in range(len(min_perm)):
                    if cross != crosses[min_perm[j].getK()]:
                        min_perm.insert(j,Structs.entry(i,crosses[i]))
                        break
                    elif j == (len(min_perm)-1):
                        min_perm.append(Structs.entry(i,crosses[i]))
                        break

                min_taken.append(i)
            
            else:
                for j in range(len(min_perm)):
                    if cross < crosses[min_perm[j].getK()]:
                        min_perm.insert(j,Structs.entry(i,crosses[i]))
                        break
                        
                    elif j == (len(min_perm)-1):
                        min_perm.append(Structs.entry(i,crosses[i]))
                        break

#            print(str(((i+1)/len(perms))*100) + '% complete')
        return min_perm                                                                     #OUT: A sorted array of key-value entries(nodes) that go from permutations with maximum cross overs to minimum cross overs.

     