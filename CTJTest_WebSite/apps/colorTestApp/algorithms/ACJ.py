import numpy as np
import scipy.stats as stats
import random
from itertools import chain

#https://github.com/lucasmaystre/choix
import choix




""" Compute an iteration of the acj algorithme 
    colors : [("black",3), ("white",255), ("grey150", 147)... ]
    comparisons : [("white", "black"), ("grey1", "black")... ] #In each tuple the 1st color is the winner
    SSR_max : float 
    #The closer the SSR max is to 1 the better will be the accuracy but it will increase the number
    #of assessment to do.  Below 0.9 the accuracy is really bad.


    return in a dico multiple parameters :
 - "finished" : True/False   #A boolean value indicating if SSR value is high enough 
 - "SSR" : float or None #The Scale Separation Reliability 
 - "new_comparison" : ("white", "grey50") or None  #the new generated comparison to realize 
 - "estimated_colors" : [("black",3), ("white",255), ("grey150", 147)... ] or None  #The estimated values of the colors
 """
def acj_iteration(colors, comparisons, SSR_max=0.95):
    result = {
                "finished": None,
                "SSR": None,
                "new_comparison": None,
                "estimated_colors": None,
            }
    
    nb_colors = len(colors)

    #The color set may have been created with a certain order in  mind
    #So we are erasing any possibility of this order to influence the algorithm's performance
    #But it can be proven that having a certain order can lead to a better convergence  
    random.shuffle(colors)   

    #We need to first have every color appear at least one time in the comparisons
    #Checking if the initials assessments have already been done 
    if len(comparisons) < (nb_colors//2 + nb_colors%2) :
        colors_compared = list(chain.from_iterable(comparisons))
        print("color_compared = ",colors_compared)#TODO:supr
        
        colors_not_compared = []
        for color in colors:
            if color[0] not in colors_compared:
                colors_not_compared.append(color)
        print("color NOT compared = ",colors_not_compared)#TODO:supr

        if len(colors_not_compared) == 1 :
            color_B = random.choice([color for color in colors if color!=colors_not_compared[0]])
            result["new_comparison"] = (colors_not_compared[0][0], color_B[0])
        else:
            result["new_comparison"] = (colors_not_compared[0][0], colors_not_compared[1][0])
    
    
    else:
        print("toutes les couleurs ont était comparées")#TODO:supr

        ###############################         INITIALIZATION       #####################################
    
        #assigning IDs to the colors for the the choix library 
        for i in range(0,nb_colors):
            colors[i] = (i, colors[i][0], colors[i][1])
        
        #Converting the comparisons with color names to color ids
        for i in range(0,len(comparisons)):
            
            for color in colors:
                if color[1] == comparisons[i][0]:
                    color_A = color[0]    
                if color[1] == comparisons[i][1]:
                    color_B = color[0]
            
            #Color A must be first cauz it means it is the one who won the comparison
            comparisons[i] = (color_A, color_B)

        # ESTIMATE VALUE COMPUTING :    
        true_values = [0]*nb_colors
        for i in range(0,nb_colors):
            true_values[colors[i][0]] = colors[i][2]

        estimated_values = []

        true_mean = np.average(true_values)
        true_std = np.std(true_values)

        parameters = None
        Z_parameters = None


        # SCALE SERIAL RELIABILITY COMPUTING :
        SSR = -1   #init at -1 to be sure to go through the main loop

        ###############################         START        ############################################
        
        #------------------------------ Computing of estimated value -----------------------------
        #Computing the maximum-likelihood given the paired comparaisons
        parameters = choix.ilsr_pairwise(nb_colors, comparisons, alpha=0.1)
        
        Z_parameters = stats.zscore(parameters)
        for x in Z_parameters: 
            val = round( x * true_std + true_mean  )
            if val < 0:
                estimated_values.append(0)
            elif val > 255:
                estimated_values.append(255)
            else:
                estimated_values.append(val)
        
        estimated_colors = []
        for i in range(0,nb_colors):
            for color in colors:
                if color[0] == i:
                    estimated_colors.append((color[1],estimated_values[i]))

        result["estimated_colors"] = estimated_colors
        print("True values are      :",true_values) #TODO:supr
        print("Estimated values are :",estimated_values) #TODO:supr

        #---------------------------------------SSR COMPUTING---------------------------------------
        """ Here we use the true values but since we aren't supposed to know about them 
        we should use the RMSE computed from the judge's previous judgements of before this CTJ assessement
        in a more realistic environement"""
        estimated_STD = np.std(estimated_values)
        MSE = np.square(np.subtract(true_values, estimated_values)).mean()
        true_STD_squared = estimated_STD**2 - MSE
        SSR = true_STD_squared / estimated_STD**2

        result["SSR"] = SSR
        
        if SSR > SSR_max :
            result["finished"] = True
        
        print("| SSR = [ ",SSR," ] |\n")#TODO:supr
        

        #----------------------------------------- NEW COMPARISON ---------------------------------------
        """ 
        There is probably a lot of room for improvement left here when it comes to how to pick a new comparison
        What have already been tried without much sucess
        pairing randomly among winners
        pairing randomly among least compared colors

        The best performances was when assessing the most far apart values
        but this isn't a realistic solution since we aren't supposed to know the true values
        And using the estimated ones isn't effective

        It has been decided to select the comparison that is estimated to be the closest to a 50/50
        """
        
        #By default we pick a random colors to assess
        id_A = random.randrange(0,nb_colors)
        #This generate another random color id that isn't A 
        id_B = random.choice(list(range(0,id_A))+list(range(id_A+1,nb_colors)))
        
        comparison = (id_A, id_B)

        #The closer to 50% the better the info given by the assessment is
        info_of_comparison = choix.probabilities([id_A, id_B],parameters)
        info_of_comparison = abs( 0.5 - round(info_of_comparison[0],2))
        for i in range(0,nb_colors):
            for k in range(0,i):
                if i != k:
                        info = choix.probabilities([i, k],parameters)
                        info = abs(0.5 - round(info[0],2))        
                        if info < info_of_comparison:
                            comparison = (i, k)  # i > k
                            info_of_comparison = info
        
        #Converting the IDs back to color names
        for color in colors:
            if color[0] == comparison[0]:
                color_A = color[1]
            if color[0] == comparison[1]:
                color_B = color[1]
        
        result["new_comparison"] = (color_A, color_B)




    return result
