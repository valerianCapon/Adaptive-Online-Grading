import numpy as np
import scipy.stats as stats
import choix
import random


# true colors value   : [0, 25, 50, 75, 100, 125, 136, 143, 150, 155, 160, 167, 175, 180, 183, 188, 193, 199, 200, 214, 255]
# estimated value are : [65, 49, 48, 70, 87, 83, 79, 134, 157, 157, 157, 157, 157, 175, 167, 190, 189, 220, 243, 241, 247]
# |||| Separation ratio G =  2.2270222263012034
# |||| KR-20 =  0.8322042918454936


# colors = [ ('G0', 0), ('G1', 10), ('G2', 15), ('G3', 20),
#            ('G4', 25), ('G5', 30), ('G6', 35), ('G7', 40),
#              ('G8', 45), ('G9',50), ('G10',60)]

# colors = [ ('G0', 0), ('G1', 31), ('G2', 62), ('G3', 94),
#            ('G7', 128),
#              ('G8', 166), ('G9',200), ('G10',255)]
# list_items = [0, 1, 2, 3, 4, 5, 6, 7]


# colors = [ ('G0', 0), ('G5',63), ('G1', 126), ('G2', 189), ('G3', 255),]
# list_items = [0, 1, 2, 3, 4]


colors = [ ('G0', 0), ('G1', 25), ('G2', 50), ('G3', 75),
           ('G4', 100), ('G5', 125), ('G6', 150), ('G7', 175),
             ('G8', 200), ('G9',225), ('G10',255)]
list_items = [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9 ,10]

random.shuffle(list_items)

# colors = [ ('G0', 0), ('G1', 25), ('G2', 50), ('G3', 75),
#            ('G4', 100), ('G5', 125), ('G6', 136), ('G6', 143), ('G6', 150),
#             ('G6', 155),('G6', 160),('G6', 167),('G6', 175),('G6', 180),
#              ('G6', 183),('G6', 188),('G6', 193),('G6', 199),('G6', 200), ('G7', 214), ('G10',255)]
# list_items = [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9 ,10, 11,12,13,14,15,16,17,18,19,20]


list_of_value_colors = []
for values in colors:
    list_of_value_colors.append(values[1])

avgtrue = np.average(list_of_value_colors)
stdtrue = np.std(list_of_value_colors)

#Create the first test that have to be done so that each color is tested at least one time
assessments = []
i = len(colors)-1

while(i > 0): 
    assessments.append((list_items[i], list_items[i-1]))
    i = i-1

if(len(colors)%2!=0):
    assessments.append((list_items[1], list_items[0]))

#assessments.append((len(list_items)-1,0))

nb_colors = len(colors)
probestimated = np.zeros((nb_colors,nb_colors),dtype=np.float64)
ssr = -1
kr20 = -1
on = 0
secu = 0



while(kr20 < 0.98 and on < 30 and secu < 5 ):
    print("BOUCLE ON =",on," COOOOOOOOOOOOOOOOOOOOOOOOOOOOMMMMMMMMMMMMMMMMMMMMMEEEEEEENCE")
    colorestimated = []
    # sterror = [0]*nb_colors
    # infoquality = [0]*nb_colors

    #------------------------------ Computing of estimated value -----------------------------
    params = choix.ilsr_pairwise(nb_colors, assessments, alpha=0.1)

    paramZ = stats.zscore(params)
    for x in paramZ:
        val = round( x*stdtrue +avgtrue  )
        if val < 0:
            colorestimated.append(0)
        elif val > 255:
            colorestimated.append(255)
        else:
            colorestimated.append(val)
    
    
    #---------------------------------------KR20-----------------------------------------------
    
    observedSD = np.std(colorestimated)
    rmse = np.sqrt(np.square(np.subtract(list_of_value_colors, colorestimated)).mean())
    trueSDsquared = observedSD**2 - rmse**2

    print("observedSD =",observedSD)
    print("RMSE =",rmse)
    print("TRUESDSQUARED =",trueSDsquared)
    G = np.sqrt(trueSDsquared) / rmse

    kr20 = trueSDsquared / observedSD**2
    
    #between 8 to 23 loops
    

    # #compute the probabilities of every duel
    # for i in range(0,(nb_colors)):
    #     for k in range(i+1,nb_colors):
    #         probestimated[i][k],probestimated[k][i] = choix.probabilities([i, k],params)
    #         # if k == 10:
    #         #     print("",i,"vs",k,"donne =",probestimated[i][k])

    # #print("tableau des proba :",probestimated)
    
    # #standards errors computing
    # for i in range(0,(nb_colors)):
    #     for k in range(0,nb_colors):
    #         infoquality[i] = infoquality[i] + probestimated[i][k]*(1-probestimated[k][i])

    # # print("Info quality :", infoquality)

    # for i in range(0,(nb_colors-1)):
    #     sterror[i] = 1 / np.sqrt(infoquality[i])

 
    # ssr = (np.std(params)**2 - np.sqrt(np.mean([i**2 for i in sterror]))) / np.std(params)**2
    #--------------------------------------PRINT RESULTS----------------------------------------------


    print("___ ___ __ ___ ___ ___ ___ ___ ___ ____  ___ _")
    print("true colors value   :",list_of_value_colors)
    print("estimated value are :",colorestimated)
    
    print("|||| Separation ratio G = ",G)
    print("|||| KR-20 = ",kr20)
    # print("|||| SSR =",ssr)
    print("_____________________________________________________________________")

    #SSR = 0.06766327257591977
    #SSR = 0.18141342821110398

    #----------------------------------------- ADDING TEST ---------------------------------------------------
    
    for i in range(0,nb_colors):
        for k in range(0,i):
            if i != k:
                proba = choix.probabilities([i, k],params)
                # print("assigning ",i,"vs",k," = ",proba[0] )
                probestimated[i][k] = round(proba[0],2)

                # print("\n",i,"vs",k,"=",probestimated[i][k])
                # print("au cas ou : ",proba[0])
                # print("avec la function :",choix.probabilities([i, k],params))
            else:
                # print("\nles indices identiques sont",i," et ",k)
                probestimated[i][k] = -1

    print("\nprobaestimated =\n",probestimated)
    highQualityAssessments = []
    insane_test = (nb_colors-1,0)
    for r in range(0,nb_colors):
        for c in range(r+1,nb_colors):
            # print("\nexaminating prob of ",r,"vs",c)
            # print("with proba of :",probestimated[r][c])
            # print("checking ",c,"vs",r," = ",probestimated[c][r] )
            if r != c and probestimated[c][r] >= 0.4 and probestimated[c][r] <= 0.6:
                highQualityAssessments.append((c,r))
                print("ajout de ", (c,r))
            if r != c and abs(0.5 - probestimated[c][r]) < abs(0.5 - probestimated[insane_test[0],insane_test[1]]):
                insane_test = (c,r)


    print("azeaz :",not highQualityAssessments, " car : ",highQualityAssessments)
    if (not highQualityAssessments) or on < 0:
        
        listofwinners = []
        # secu = 1000
        for test in assessments:                                    
            listofwinners.append(test[0])

        print("no great test to do  : ",highQualityAssessments)


        itemA = 0
        itemB = 0
        while (itemA == itemB) and ((itemB, itemA) in assessments) or ((itemA, itemB) in assessments) :
            itemA = listofwinners[random.randrange(0,len(listofwinners),1)]
            itemB = listofwinners[random.randrange(0,len(listofwinners),1)]
        
        if(itemA > itemB):
            if ((itemA, itemB) not in assessments):
                print("random test added :",(itemA, itemB))
                assessments.append((itemA,itemB))
                i+=1
            else:
                secu+=1
                print("test cancel :",(itemA, itemB))
            
        elif(itemA < itemB):
            if ((itemB, itemA) not in assessments):
                print("random test added :",(itemB, itemA))
                assessments.append((itemB,itemA))
                i+=1
            else:
                secu+=1
                print("test cancel :",(itemB, itemA))
        else:
            print("test cancel :",(itemB, itemA))
            # secu+=1
    else:
        k = 0
        secu2 = 0
        while (k < 1 and secu2 < 4):
            if len(highQualityAssessments) == 0 : 
                secu2 = 5
            else:
                best_test = highQualityAssessments[0]
                for test in highQualityAssessments:
                    if test[0]-test[1] > best_test[0]-best_test[1]:
                            best_test = test
                test_to_add = insane_test
                # test_to_add = best_test
                # test_to_add = highQualityAssessments[random.randrange(0,len(highQualityAssessments))]
                if test_to_add[1] > test_to_add[0]:
                    test_to_add = (test_to_add[1],test_to_add[0])
                
                if test_to_add not in assessments or True:
                    assessments.append(test_to_add)
                    
                    print("\n----------\n",assessments),
                    print("\n****************\n",highQualityAssessments)

                    print(highQualityAssessments.remove(assessments[-1]))
                    
                    print("\nTRUE test added :",assessments[-1])
                    print("great test possible =", highQualityAssessments)
                    k +=1
                else:
                    print("no great test to do  : ",highQualityAssessments, "\n test done are :",assessments)
                    itemA = random.randrange(0,nb_colors,1)
                    itemB = random.randrange(0,nb_colors,1)
                    if(itemA > itemB):
                        if ((itemA, itemB) not in assessments):
                            print("random test added :",(itemA, itemB))
                            assessments.append((itemA,itemB))
                            i+=1
                        else:
                            secu2+=1
                            print("test cancel :",(itemA, itemB))
                        
                    elif(itemA < itemB):
                        if ((itemB, itemA) not in assessments):
                            print("random test added :",(itemB, itemA))
                            assessments.append((itemB,itemA))
                            i+=1
                        else:
                            secu2+=1
                            print("test cancel :",(itemB, itemA))
                    else:
                        print("test cancel :",(itemB, itemA))
                        secu2+=1



    # print("------------")
    # print(probestimated)
    # i = 0
    # secu = 0
    # while(i < 1 and secu !=5):
    #     for prob in probestimated:


    #     itemA = random.randrange(0,nb_colors,1)
    #     itemB = random.randrange(0,nb_colors,1)
    #     if(itemA > itemB):
    #         if ((itemA, itemB) not in assessments):
    #             print("test added :",(itemA, itemB))
    #             assessments.append((itemA,itemB))
    #             i+=1
    #         else:
    #             secu+=1
    #             print("test cancel :",(itemA, itemB))
            
    #     elif(itemA < itemB):
    #         if ((itemB, itemA) not in assessments):
    #             print("test added :",(itemB, itemA))
    #             assessments.append((itemB,itemA))
    #             i+=1
    #         else:
    #             secu+=1
    #             print("test cancel :",(itemB, itemA))
    #     else:
    #         print("test cancel :",(itemB, itemA))
    #         secu+=1
    #----------------------------------------- ADDING TEST ---------------------------------------------------

    on = on+1

print("secu = ",secu)
print("LIST OF ITEMS = ",list_items)