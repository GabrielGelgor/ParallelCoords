import Structs, importlib, Modules, copy, math
import numpy as np

class VIKOR():

    def __init__(self, pf):
        self.pf = pf


    def sort(self):
        '''
        STEP 1: BUILD DECISION MATRIX
        '''
        DM = []                                                     #Building decision matrix

        for i in range (len(self.pf)):
            for j in range (len(self.pf[i].getV())):
                if i == 0:
                    start = []
                    DM.append(start)
                    DM[j].append(self.pf[i].getV()[j])

                else:
                    DM[j].append(self.pf[i].getV()[j])

        '''
        STEP 2: NORMALIZE VALUES 
        '''

        NM = copy.deepcopy(DM)                                                  #Creating normalized decision matrix
        calc = 0
        try:
            for i in range (len(NM)):
                for j in range (len(NM[i])):
                    calc = NM[i][j]/math.sqrt(sum(DM[i])**2)
                    NM[i][j] = calc

            '''
            STEP 3: DETERMINE IDEAL AND NEGATIVE IDEAL SET
            '''

            f_i = []                                                                #ideal set
            f_neg = []                                                              #negative ideal set

            for i in range(len(NM)):
                f_i.append(min(NM[i]))
                f_neg.append(max(NM[i]))

            '''
            STEP 4: FIND MANHATTAN (S) AND CHEBYSHEV (R) DISTANCES OF THE M ALTERNATIVE METHODS
            '''

            rawS = []
            rawR = []
            S = []
            R = []
            weights = []

            '''
            Temporary filler!! AS of right now there is no weighting on individual dimensions. This is an optimization problem to be solved at a later date.
            '''

            for i in range(len(NM)):
                weights.append(1/len(NM))

            '''
            End filler
            '''

            for i in range(len(self.pf)):
                for j in range(len(NM)):
                    item = (NM[j][i]-f_i[j])/(f_neg[j]-f_i[j])
                    rawS.append(weights[j]*item)
                    rawR.append(item)

                S.append((sum(rawS)))
                R.append((max(rawR)))
                del rawS[:]
                del rawR[:]


            '''
            STEP 5: FIND VIKOR INDEX
            '''

            s_I = min(S)
            r_I = min(R)
            s_N = max(S)
            r_N = max(S)
            alpha = 0.5

            Q = []


            for i in range (len(self.pf)):
                Q.append((alpha*(S[i]-s_I))/(s_N-s_I)+(1-alpha)*((R[i]-r_I)/(r_N-r_I)))
            
            '''
            FIND BEST VIKOR SCORE (LOWEST)
            '''
            print(Q)
            best = []
            best.append(self.pf[np.argmin(Q)])

            return best

        except:
            return self.pf                              #Sometimes this process will throw a dividebyzero exception, when the ranking methods overlap too much. In this case, the parity front is returned unaltered.