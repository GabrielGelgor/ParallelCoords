import Structs, re, itertools, os, importlib, Modules, NDS, pandas, fcns, VIKOR
import numpy as np
from pandas.plotting import parallel_coordinates
import matplotlib.pyplot as plt

'''
HANDLES THE PROCESSING OF INPUT CSV FILES INTO USABLE FORMS FOR METHODS
_________________________________________________________________________________________________________________________________
'''
data = []                                              #Matrix is raw of composed of points, data is composed of columns
matrix = []
cData = []                                             #cData: numerical data to be used as dimensions in parallel coordinate graphs
aData = []                                             #aData: alphanumerical data used to catagorize points, rather than actual dimensions
Alphacols = []                                          
perms = []                                             #perms: column permutation list; 3D.

Firstline = True

with open("data.txt","rt") as src:                      #Opening data source
    temp = []
    for line in src:
        currentline = line.split(",")

        
        for i in range(0,len(currentline)):             #First line of file is the header - These are always treated as strings
            if Firstline == True:
                temp.append(currentline[i])   

            elif re.search('[a-zA-Z]',currentline[i]):  #NOTE:Converts categorical data into categories for permutations. For now, only use a single category, as current PC Wrapper can only handle 1.
                temp.append(currentline[i])

                if i not in Alphacols:
                    Alphacols.append(i)                 #Saving the column location of the alphanumeric data. This will be removed and saved for later.
            else:
                try:
                    temp.append(float(currentline[i]))
                except:
                    print(i)

        Firstline = False

        matrix.append(temp[:])
        del temp[:]

for i in range(0,len(matrix[0])):                       #Loop for the creation of our usable column-vector data set.
    for j in range(len(matrix)):
        temp.append(Structs.entry(matrix[j][i],j))
        
    data.append(temp[:])
    del temp[:]


for i in range(0,len(data)):
    if i not in Alphacols:
        cData.append(data[i])
    else:
        aData.append(data[i]) 

fullData = Structs.data(cData[:],aData[:])

perms = np.asarray(list(itertools.permutations(fullData.getC())))
print('Done step 1!')

'''
HANDLES THE DYNAMIC IMPORTATION AND UTILIZATION OF DIFFERENT USER-CREATED AXIS REORDING METHODS
_________________________________________________________________________________________________________________________________
'''

mods = os.listdir('Modules')
Sorts = []
ranks = []

for i in range(0,len(mods)):                                    #Loop handling the importation of all methods
    if mods[i].endswith('.py') and ('init' not in mods[i]):
        mods[i] = '.' + re.sub('.py$', '', mods[i])
        Sorts.append(importlib.import_module(mods[i],package = 'Modules'))

subs = Structs.rank_method.__subclasses__()                     #Retrieves all ranking methods and their location

for i in range(len(subs)):
    curr_class = str(subs[i])
    curr_class = curr_class[curr_class.rfind('.')+1:curr_class.rfind('\'')]
    exec('temp = Sorts['+str(i)+'].'+curr_class+'()')           #Creates temporary object for sorting method and provides sorting ranks.
    print('Utilizing method '+str(i+1)+' of '+str(len(subs)))
    ranks.append(temp.rank(perms))


'''
HANDLES PARETO DOMINATION SORTING
___________________________________________________________________________________________________________________________________

'''

sort = NDS.NDS(ranks)                                           #Executes non-dominated sorting.

items,sample = sort.Sort()
Front = VIKOR.VIKOR(items)
VIKOR_best = Front.sort()

x_val = []
y_val = []

for i in range(len(items)):
    x_val.append(items[i].getV()[0])
    y_val.append(items[i].getV()[1])

plt.plot(x_val,y_val)
plt.plot(x_val,y_val,'or')
plt.savefig('Output/Pareto.png', bbox_inches='tight')
plt.show()


VIKOR_best.append(sample)
print(VIKOR_best)



status = input('Skip individual graph display?[Y/n] ')          #Handles conversion of pareto items into CSV files that can be converted to graphs

for i in range (len(VIKOR_best)):
    print ('ding')
    cur_graph = fcns.parse2csv(perms[VIKOR_best[i].getK()],aData)
    fcns.export2csv(cur_graph)
    
    if (status != 'Y' and status != 'y'):                       #Handles drawing of graphs.
        data = pandas.read_csv('output.csv', sep=',')
        parallel_coordinates(data, aData[0][0].getK())
        plt.show()
        plt.savefig('Output/'+str(i)+'.png', bbox_inches='tight')
        plt.gcf().clear()
        status = input('Skip remaining individual graph display?[Y/n] ')

    else:
        data = pandas.read_csv('output.csv', sep=',')
        parallel_coordinates(data, aData[0][0].getK()[:-1])
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        plt.savefig('Output/'+str(i)+'.png', bbox_inches='tight')

        plt.gcf().clear()