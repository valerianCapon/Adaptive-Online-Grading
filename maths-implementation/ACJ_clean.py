import numpy as np
import scipy.stats as stats
import random
"""
    Using the "choix" library https://github.com/lucasmaystre/choix that implement in order to 
    be use for pairwise comparisons
"""
import choix

###############################         FUNCTIONS       ############################################

def assessment_result(itemA:int, itemB:int, colors):
    result = None
    valueA = None
    valueB = None

    for color in colors:
        if color[0] == itemA:
            valueA = color[2]
        if color[0] == itemB:
            valueB = color[2]
    
    if valueA > valueB :
        result = (itemA, itemB)
    elif valueB > valueA :
        result = (itemB, itemA)
    return result 

def assign_id_to_colors(colors):
    colors_with_id = []
    i = 0
    for color in colors :
            colors_with_id.append( (i, color[0], color[1]) )
            i += 1
    return colors_with_id

###############################         INITIALIZATION       ############################################

# DATA :
"""  ( id_item, color_name, color_value )                     """
# colors = [ (7,'G0', 0), (9,'G1', 25), (5,'G2', 50), (10,'G3', 75),
#            (8,'G4', 100), (2,'G5', 125), (6,'G6', 150), (0,'G7', 175),
#              (4,'G8', 200), (1,'G9',225), (3,'G10',255)]


# colors = [ (2, 'G0', 0), (0, 'G5',63), (4, 'G1', 126), (1,'G2', 189), (3,'G3', 255),]


# colors = [ ('G0', 0), ('G1', 31), ('G2', 62), ('G3', 94),
#            ('G7', 128),
#              ('G8', 166), ('G9',200), ('G10',255)]

colors = [('black', 0), ('g1', 160), ('g2', 106), ('white', 255)]

nb_colors = len(colors)
random.shuffle(colors) #We are not supposed to have colors sorted nicely in a increasing way

colors = assign_id_to_colors(colors)

# ESTIMATE VALUE COMPUTING : 
true_values = [0]*nb_colors
for i in range(0,nb_colors):
    true_values[colors[i][0]] = colors[i][2]


print("true values are ",true_values)
estimated_values = []
estimated_proba = np.zeros((nb_colors,nb_colors),dtype=np.float64)

true_mean = np.average(true_values)
true_std = np.std(true_values)

parameters = None
Z_parameters = None

# SCALE SERIAL RELIABILITY COMPUTING :
SSR = -1   #init at -1 to be sure to go through the main loop



# ASSESSMENTS :
assessments = []



###############################         START        ############################################

"""    Emulating the first nb_colors/2 assessment to do, to have at least each """
i = 0
while i < nb_colors-1:
    assessment_done = assessment_result(colors[i+1][0], colors[i][0], colors)
    assessments.append(assessment_done)
    i += 2
if ( nb_colors%2 ) != 0 :  #If there is a odd number of colors
    assessment_done = assessment_result(colors[-1][0], colors[-2][0], colors) #Last versus Last but one
    assessments.append(assessment_done)



"""                             START OF THE ALGORITHME                                     """

nb_loop = 0
while SSR < 0.9 and nb_loop < 30:
    print("\n============================> LOOP [ ",nb_loop," ] <============================")
    
    #------------------------------ Computing of estimated value -----------------------------
    estimated_values = [] #Reseting to zero the list of estimated value
    #Computing the maximum-likelihood given the paired comparaisons
    parameters = choix.ilsr_pairwise(nb_colors, assessments, alpha=0.1)
    
    Z_parameters = stats.zscore(parameters)

    for x in Z_parameters: 
        val = round( x * true_std + true_mean  )
        if val < 0:
            estimated_values.append(0)
        elif val > 255:
            estimated_values.append(255)
        else:
            estimated_values.append(val)
    
    print("True values are      :",true_values)
    print("Estimated values are :",estimated_values)



    #---------------------------------------SSR COMPUTING---------------------------------------
    """ Here we use the true values but since we aren't supposed to know about them 
    we should use the RMSE computed from the judge's previous judgements of before this CTJ assessement"""
    estimated_STD = np.std(estimated_values)
    MSE = np.square(np.subtract(true_values, estimated_values)).mean()
    true_STD_squared = estimated_STD**2 - MSE
    SSR = true_STD_squared / estimated_STD**2

    print("| SSR = [ ",SSR," ] |\n")     

    #----------------------------------------- ADDING assessment ---------------------------------------------------
    itemA = 0
    itemB = 0
    #By default we pick a random assessment
    while itemA == itemB:
        itemA = random.randrange(0,nb_colors,1)
        itemB = random.randrange(0,nb_colors,1)
    quality_assessment = (itemA, itemB)

    #The closer to 50% the better the info given by the assessment is
    info_of_quality_assessment = choix.probabilities([itemA, itemB],parameters)
    info_of_quality_assessment = abs( 0.5 - round(info_of_quality_assessment[0],2))

    for i in range(0,nb_colors):
        for k in range(0,i):
            if i != k:
                info = choix.probabilities([i, k],parameters)
                info = abs(0.5 - round(info[0],2))        
                if info < info_of_quality_assessment:
                    quality_assessment = (i, k)  # i > k
                    info_of_quality_assessment = info

    
    quality_assessment = assessment_result(quality_assessment[0],quality_assessment[1], colors)
    assessments.append( quality_assessment )
    

    print("\nassessment ADDED IS ==> ",quality_assessment)
    #-----------------------------------------------------
    valueW = None
    valueL = None
    for color in colors:
        if color[0] == quality_assessment[0]:
            valueW = color[2]
        if color[0] == quality_assessment[1]:
            valueL = color[2]
    print("VALUE OF assessment IS ==> ",(valueW, valueL))
    #--------------------------------------------------------------------------------
    nb_loop += 1

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(" [ ",len(assessments)," ] ASSESSMENTS HAVE BEEN DONE")