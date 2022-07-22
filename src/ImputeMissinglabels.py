from tkinter import E
import numpy as np
import numpy.ma as ma
import pandas as pd

def getConditionalProba(A,B):
    delta=0.000000000000000000001
    count=0.0
    total=0.0
    i=0
    for value in A:
        if(value==1 and B.at[i] ==1):
            count=count+1
            total=total+1
        elif (value==1 and B.at[i]==0):
            total=total+1
        i=i+1
    return count/(total+delta),total

def getConditionalProbaSus(A,B):
    delta=0.000000000000000000001
    count=0.0
    total=0.0
    i=0
    for value in A:
        if(value==0 and B.at[i] ==0):
            count=count+1
            total=total+1
        elif (value==0 and B.at[i]==1):
            total=total+1
        i=i+1
    return count/(total+delta), total

'''
def getConditionalProb(df,labels, size, MinDatNum=50, getnumber=0):
    Parray = np.arange(size*size, dtype="object").reshape(size, size)
    Sarray = np.arange(size*size, dtype="object").reshape(size, size)
    if(getnumber==1):
        PNumarray = np.arange(size * size, dtype="object").reshape(size, size)
        SNumarray = np.arange(size * size, dtype="object").reshape(size, size)

    for i, felement in enumerate(labels):
        PTotal, NTotal, PNum, NNum = 0.0, 0.0, 0, 0
        for j, selement in enumerate(labels):

            if (i == j):
                Parray[j][i] = 1
                Sarray[j][i] = 1
                continue
            df1 = df[[felement, selement]]
            df1.dropna(subset=[felement], inplace=True)
            df1 = df1.reset_index()
            pfsP, lengthP = getConditionalProba(df1[felement], df1[selement])
            if (lengthP >= MinDatNum):
                PTotal = PTotal + pfsP
                PNum = PNum + 1
                Parray[j][i] = round(pfsP, 4)
            else:
                Parray[j][i]=-1
            if(getnumber==1):
                PNumarray[j][i]=lengthP
            #print(felement + ',' + selement + ':' + str(pfsP) + '(' + str(lengthP) + ')')
            pfsS, lengthS = getConditionalProbaSus(df1[felement], df1[selement])
            if (lengthS >= MinDatNum):
                NTotal = NTotal + pfsP
                NNum = NNum + 1
                Sarray[j][i] = round(pfsS, 4)
            else:
                Sarray[j][i]=0
            if (getnumber == 1):
                SNumarray[j][i] = lengthS
            #print(felement + ',' + selement + ':' + str(pfsS) + '(' + str(lengthS) + ')')
    if (getnumber == 1):
        return Parray, Sarray, PNumarray, SNumarray
    return Parray, Sarray


def Imputelabels(df,label):
    ResArray, SusArray =getConditionalProb(df,label,len(label),50)
    weightdf = pd.DataFrame(columns=label, index=df.index)
    #updatedf=pd.DataFrame(columns=label, index=df.index)
    updatedf=df.copy()
    #i=0
    print (len(df.values))
    for i, value in enumerate(df.values):
        weightlist = []
        for j, val in enumerate(value):
            maxvalue=0.8
            predict=-1
            skip=0
            if (np.isnan(val)):
                k=0
                for prob in ResArray[j]:
                    #print(prob,value[k])
                    if(prob >= maxvalue and not(np.isnan(value[k])) and value[k]==1):
                        maxvalue =prob
                        predict=value[k]
                        if(prob==1):
                            #print('skip')
                            skip=1
                            break
                    k = k + 1
                k=0
                if(skip !=1):
                    #print('checking sus')
                    for prob in SusArray[j]:
                        if(prob >= maxvalue and not(np.isnan(value[k])) and value[k]==0):
                            maxvalue =prob
                            predict=value[k]
                            if (prob == 1):
                                skip = 1
                                break
                        k = k + 1

                if (predict != -1):
                    #print('Predict updated')
                    value[j]=predict
                    weightlist.append(maxvalue)
                else:
                    weightlist.append(0)
            else:
                weightlist.append(1)

        weightdf.loc[i] = weightlist
        updatedf.loc[i]=value
        #i=i+1
    print ('Done' +str(i)+':'+str(updatedf.shape))
    return updatedf, weightdf
'''
def getConditionalProbability(df,labels, size, MinDatNum=50):
    Parray = np.arange(size*size, dtype="object").reshape(size, size)
    Sarray = np.arange(size*size, dtype="object").reshape(size, size)

    for i, felement in enumerate(labels):
        for j, selement in enumerate(labels):
            if (i == j):
                Parray[i][j] = 1
                Sarray[i][j] = 1
                continue
            df1 = df[[felement, selement]]
            #print (df1)
            pfsP, lengthP = getConditionalProba(df1[selement],df1[felement])
            if (lengthP >= MinDatNum):
                Parray[i][j] = round(pfsP, 4)
            else:
                Parray[i][j]=-1

            pfsS, lengthS = getConditionalProbaSus(df1[selement],df1[felement])
            if (lengthS >= MinDatNum):
                Sarray[i][j] = round(pfsS, 4)
            else:
                Sarray[i][j]=-1

    return Parray, Sarray

def getLikelihood(df,label,trainingmode=1, ResArray=None, SusArray=None):
    N=len(label)
    delta=0.000000000000001
    if (trainingmode==1):
        ResArray, SusArray = getConditionalProbability(df, label, N, MinDatNum=100)
    #print (ResArray)
    #print("Sus")
    #print(SusArray)
    weightdf = pd.DataFrame(columns=label, index=df.index)
    updatedf = df.copy()
    for i, value in enumerate(df.values):
        weightlist = []
        for j, val1 in enumerate(value):
            val1=float(val1)
            if (pd.isnull(val1)):
                PR = 1.0
                PS = 1.0
                for index, val2 in enumerate(value):
                    val2=float(val2)
                    if(index == j):
                        continue
                    if(val2==0 and (SusArray[j][index] !=-1)):
                        PR = PR *  ((1-SusArray[j][index])+delta)
                        PS = PS * ((SusArray[j][index])+delta)
                    elif (val2 == 1 and (ResArray[j][index] != -1)):
                        PR = PR *((ResArray[j][index])+delta)
                        PS = PS * ((1 - ResArray[j][index])+delta)
                        

                #print(PR, PS)
                if (PR > PS):
                    value[j] = 1
                    weightlist.append(round((PR - PS) / (PR+delta), 3))
                else:
                    value[j] = 0
                    weightlist.append(round(((PS - PR) / (PS+delta)), 3))
            else:
                if (val1==0 or val1==1 or val1==-1):
                    weightlist.append(1)
                elif(val1< 0.5):
                    value[j] = 0
                    weightlist.append((0.5-val1))
                else:
                    value[j] = 1
                    weightlist.append(val1-0.5)

        weightdf.loc[i] = weightlist
        updatedf.loc[i] = value
        # i=i+1
    #print('Done' + str(i) + ':' + str(updatedf.shape))
    return  ResArray, SusArray, updatedf, weightdf

'''
df = pd.read_csv('Finalplfam_iddataset_Multilabel_final.csv', index_col=0)
labels=['amoxicillin','ampicillin','aztreonam','cefepime','cefotaxime','cefoxitin','ceftazidime','cefuroxime',
      'ciprofloxacin','gentamicin','piperacillin','tobramycin','trimethoprim','sulfamethoxazole']
selectedf=df[labels]
uddf, weighdf=getLikelihood(selectedf,labels)
uddf.to_csv('Updated_Datset_1.csv')
weighdf.to_csv('Weight_1.csv')
'''


