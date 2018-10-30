import Structs,itertools
import numpy as np

def sel_sort(arr):                                              #Selection Sort
    size = len(arr)                                             #Size of the array to sort
    sort = []                                                   #List of sorted indecies
    
    for cnt in range(size):

        i_max = 0                                               #Index of the current max value within the array
        for in_cnt in range(0, len(arr)):                       #Count through entire list
            
            try:
                if (arr[in_cnt].getK() > arr[i_max].getK()):    #If the value of the current dimension is larger than the value of the current max dimension in list, replace the index of max variable with this one.
                   i_max = in_cnt
            except:
                i_max += 1                                      #Deals with headers

        sort.append(arr[i_max].getV())                          #Append the top ranked item to the sorted list

        try:
            del arr[i_max]                                      #Try to straight-forward delete the item
        except:
            arr = np.delete(arr, i_max)                         #If an error is raised, use the less efficient way of deletion.
        

    return sort

def line_cross(line1,line2):                                    #Determines whether or not two lines cross over each other.
    del_x = [1,1]                                               #Calculates delta x and delta y
    del_y = [line1.y1 - line1.y2, line2.y1 - line2.y2]

    def det(L1,L2):                                             #Calculates the determinate; if 0, then the lines are parallel
        return L1[0] * L2[1] - L1[1] * L2[0]

    div = det(del_x, del_y)
    if div == 0:                                                #Determines whether or not lines are parallel and calculation should stop
        return False

    conn = float(line2.y1 - line1.y1)/(line1.getM()-line2.getM()) #Determines the point of intersection between the two lines.

    if conn > 0 and conn < 1:                                   #If the lines intersect within the bounds of the two axis they originate from, then intersection occurs
        return True
    else:
        return False
    

def get_Cross(preArr,endArr, cap):                              #Determines the number of crossovers between two sets of axis
    cross = 0                                                   #Number of crosses found
    lines = []                                                  #Array holding the info for each line in the PC system
    combos = []                                                 #Array for holding all possible crossovers

    for i in range(0, len(preArr)):                             #A nested loop to find the start and end points of each line in the current axis pair
        for j in range(0, len(preArr)):
            if (preArr[i] == endArr[j]):                        #If the two points are identified as being from the same set of coordinates, then form a line between the two points
                lines.append(Structs.line(i,j))                 
                break

    combos = np.asarray(list(itertools.combinations(lines,2)))  #Generate every possible line combination to determine whether or not they intersect

    for i in range(0,len(combos)):                              #Loop to determine crossovers
        truth = line_cross(combos[i][0],combos[i][1])           #Retrieves a pair of lines to check

        if (truth == True):                                     #Counts the number of times a crossover occurs.
                cross += 1

    return (cross)

def parse2csv(perm,aData):
    csv_str = ''
    for i in range(len(perm)):                  #Creates header for CSV data
        csv_str += (perm[i][0].getK())
        if (i < len(perm)-1):
            csv_str += ','
        else:
            csv_str +=  (','+aData[0][0].getK())

            

    for i in range(1, len(perm[0])):               #Formats permutation data entires into coordinate sets
        for j in range(len(perm)):
            csv_str += str(perm[j][i].getK())
            if j < len(perm)-1:
                csv_str += ','
            else:
                csv_str += (','+aData[0][i].getK())
    
    return csv_str

def export2csv(csv_str):
    with open('output.csv','w') as file:
        file.write(csv_str)