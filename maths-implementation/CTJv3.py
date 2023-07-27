import numpy as np
import random
from itertools import chain
###############################         FUNCTIONS       ############################################


def assign_id_to_colors(colors):
    colors_with_id = []
    i = 0
    for color in colors :
            colors_with_id.append( (i, color[0], color[1]) )
            i += 1
    return colors_with_id

def is_assessed(color_A,color_B,color_C, assessments) :
    for assessment in assessments:
        colors_assessed = []
        colors_assessed.append(assessment[0][0])
        colors_assessed.append(assessment[1][0][0])
        colors_assessed.append(assessment[2][0])
        if color_A in colors_assessed and color_B in colors_assessed and color_C in colors_assessed:
            return True
    return False

def get_color(color_id, colors):
    for color in colors:
        if color[0] == color_id :
            return color

def assessment_result(colors_to_asses, colors_values, colors):
    #Sorting the colors in an ascending order
    if colors_values[colors_to_asses[0]] > colors_values[colors_to_asses[1]] :
        colors_to_asses[0], colors_to_asses[1] = colors_to_asses[1], colors_to_asses[0]

    if colors_values[colors_to_asses[0]] > colors_values[colors_to_asses[2]] :
        colors_to_asses[0], colors_to_asses[2] = colors_to_asses[2], colors_to_asses[0]

    if colors_values[colors_to_asses[1]] > colors_values[colors_to_asses[2]] :
        colors_to_asses[2], colors_to_asses[1] = colors_to_asses[1], colors_to_asses[2]



    
    short = colors_values[colors_to_asses[1]] - colors_values[colors_to_asses[0]]
    long = colors_values[colors_to_asses[2]] - colors_values[colors_to_asses[0]]
    if long == 0:
        dist = 5
    else :
        dist = round(short*10/long)
    darkest = get_color(colors_to_asses[0],colors)
    mid = (get_color(colors_to_asses[1],colors),dist)
    lightest =  get_color(colors_to_asses[2],colors)
    return (darkest, mid, lightest)


###############################         INITIALIZATION       ############################################

# DATA
# colors = [ (0, 'G0', 0), (4, 'G6', 75), (2, 'G5', 125),(3, 'G2', 189), (1, 'G10', 255), ]

colors = [ (7,'G0', 0), (9,'G1', 25), (5,'G2', 50), (10,'G3', 75),
           (8,'G4', 100), (2,'G5', 125), (6,'G6', 150), (0,'G7', 175),
             (4,'G8', 200), (1,'G9',225), (3,'G10',255)]

nb_colors = len(colors)
random.shuffle(colors) #We are not supposed to have colors sorted nicely in a increasing way

#exemple of an assessemnt :   (darkest, (middle,dist1), lightest)
assessments = []

# ESTIMATE VALUE COMPUTING : 
true_values = [0]*nb_colors

for i in range(0,nb_colors):
    true_values[colors[i][0]] =  colors[i][2]


# SCALE SERIAL RELIABILITY COMPUTING :
SSR = -1   #init at -1 to be sure to go through the main loop


# SETTING UP THE MATRICES AND 2 FIXED POINTS
#Here we don't really care which colors we use as fixed points
#But it makes more sense to always have to pick the min and max values
A = np.zeros(shape=(2, nb_colors))
b = np.zeros( shape=(2, 1))
row_nb = 0
for color in colors[:2]:
    A[row_nb][color[0]] = 1
    b[row_nb] = color[2]
    row_nb += 1
    

print("A = \n",A)
print("b = \n",b)



"""                             START OF THE ALGORITHME                                     """
# ASSESS ALL COLORS ONE TIME
for i in range(0,nb_colors-3,3):
    colors_to_asses = [i, i+1, i+2]
    new_assessment = assessment_result(colors_to_asses, true_values, colors)
    assessments.append(new_assessment)
    print("\nassessment ADDED IS ==> ",new_assessment)

if nb_colors%3 != 0:
    colors_to_asses = [nb_colors-1,nb_colors-2, nb_colors-3]
    new_assessment = assessment_result(colors_to_asses, true_values, colors)
    assessments.append(new_assessment)
    print("\nassessment ADDED IS ==> ",new_assessment)

# SETTING UP THE MATRICES
index_assessments = 0
for assessment in assessments:
    d1 = assessment[1][1]
    d2 = 10 - d1
    alpha = d1/d2
    worst = assessment[0][0]
    best = assessment[2][0]
    mid = assessment[1][0][0]

    new_row = [0]*nb_colors
    new_row[worst] = 1
    new_row[mid] = -(alpha + 1)
    new_row[best] = alpha

    A = np.vstack([A, new_row])
    b = np.vstack([b, [0]])
    index_assessments += 1

print("SETTING UP THE MATRICES")
print("A = \n",A)
print("b = \n",b)


nb_loop = 0
while SSR <= 0.9 and nb_loop < nb_colors*2:
    print("\n============================> LOOP [ ",nb_loop," ] <============================")

    #------------------------------ Computing of estimated value -----------------------------
    
    #Updating the matrices with the new assessments
    for assessment in assessments[index_assessments:]:
        d1 = assessment[1][1]
        d2 = 10 - d1
        alpha = d1/d2
        worst = assessment[0][0]
        best = assessment[2][0]
        mid = assessment[1][0][0]

        new_row = [0]*nb_colors
        new_row[worst] = 1
        new_row[mid] = -(alpha + 1)
        new_row[best] = alpha

        A = np.vstack([A, new_row])
        b = np.vstack([b, [0]])
        index_assessments +=1
        print("A = \n",A)
        print("b = \n",b)

    
    estimated_values = np.linalg.lstsq(A,b,rcond=1e-17)[0]
    #converting in a list
    estimated_values = list(chain.from_iterable(estimated_values)) 

    for i in range(0,nb_colors):
        if estimated_values[i] < 0 :
            estimated_values[i] = 0
        elif estimated_values[i] > 255 :
            estimated_values[i] = 255
        else :
            estimated_values[i] = round(estimated_values[i])


    print("<============ RESULT ==============>")
    print(estimated_values)
    print(true_values)

    #---------------------------------------SSR COMPUTING---------------------------------------
    """ Here we use the true values but since we aren't supposed to know about them 
    we should use the RMSE computed from the judge's previous judgements of before this CTJ assessement"""
    estimated_STD = np.std(estimated_values)
    MSE = np.square(np.subtract(true_values, estimated_values)).mean()
    true_STD_squared = estimated_STD**2 - MSE
    SSR = true_STD_squared / estimated_STD**2

    print("| SSR = [ ",SSR," ] |\n")    


    #----------------------------------------- ADDING TEST -------------------------------------
    
    #ééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééé
    # #Generate an assessment that are supposed to have great distance within
    # #Prevent infinite loop
    # secu = 0
    # colors_to_asses = [random.randrange(0,nb_colors,1) for _ in range(0,3) ]
    # same = colors_to_asses[0] == colors_to_asses[1]
    # same = same or colors_to_asses[0] == colors_to_asses[2]
    # same = same or colors_to_asses[1] == colors_to_asses[2]
    # limit_broken = secu > (nb_colors*10) 
    # if not same :
    #     new_assessment = assessment_result(colors_to_asses, estimated_values, colors)
    #     distance_check = new_assessment[1][1] < 4 or new_assessment[1][1] > 6 

    # while same or (not distance_check and not limit_broken):
    #     colors_to_asses = [random.randrange(0,nb_colors,1) for _ in range(0,3) ]
    #     same = colors_to_asses[0] == colors_to_asses[1]
    #     same = same or colors_to_asses[0] == colors_to_asses[2]
    #     same = same or colors_to_asses[1] == colors_to_asses[2]
    #     limit_broken = secu > (nb_colors*10) 
    #     if not same :
    #         new_assessment = assessment_result(colors_to_asses, estimated_values, colors)
    #         distance_check = new_assessment[1][1] < 4 or new_assessment[1][1] > 6
            
    #     secu += 1
    
    #ééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééé


    #***************************************************************************************
    #Generate an assessment from the 3 least assessed colors
    least_three_assessed = [(None,9999),(None,9999),(None,9999)]
    dim_A = A.shape
    print(dim_A)
    for color in range(0,dim_A[1]):
        nb_assessed = 0
        for assessment in range(2,dim_A[0]):
            if A[assessment][color] != 0 :
                nb_assessed += 1
        for i in range(0,3) :
            if nb_assessed < least_three_assessed[i][1]:
                least_three_assessed[i] = (color, nb_assessed)
                break
    #***************************************************************************************

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # #Generate an already not done assessment randomly
    # color_A = random.randrange(0,nb_colors,1)
    # color_B = random.randrange(0,nb_colors,1)
    # color_C = random.randrange(0,nb_colors,1)
    # same = color_A == color_B or color_A == color_C or color_B == color_C
    # #Prevent infinite loop
    # secu = 0
    # limit_broken = secu > (nb_colors*10) 
    # already_done = is_assessed(color_A,color_B,color_C, assessments)
    # while same or (already_done and not limit_broken):
    #     color_A = random.randrange(0,nb_colors,1)
    #     color_B = random.randrange(0,nb_colors,1)
    #     color_C = random.randrange(0,nb_colors,1)
    #     same = color_A == color_B or color_A == color_C or color_B == color_C
    #     limit_broken = secu > (nb_colors*10) 
    #     already_done = is_assessed(color_A,color_B,color_C, assessments)
    #     secu += 1
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #Computing a simulated assessment result
    colors_to_asses = []

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # For the randomized assessment generation
    # colors_to_asses.append(get_color(color_A, colors))
    # colors_to_asses.append(get_color(color_B, colors))
    # colors_to_asses.append(get_color(color_C, colors))
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #***************************************************************************************
    #For the 3 least assessed colors assessment generation
    for color in least_three_assessed :
        colors_to_asses.append(color[0])
 
    #***************************************************************************************


    print("COLOR TO ASSES ARE =",colors_to_asses)
    new_assessment = assessment_result(colors_to_asses, true_values, colors)
    assessments.append(new_assessment)
    print("\nassessment ADDED IS ==> ",new_assessment)

    nb_loop += 1

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(" [ ",len(assessments)," ] ASSESSMENTS HAVE BEEN DONE")
# pprint(assessments)