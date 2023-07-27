import numpy as np
import scipy.stats as stats
import choix
import random
###############################         FUNCTIONS       ############################################

def testResult(itemA:int, itemB:int, colors):
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

###############################         INITIALIZATION       ############################################

# DATA :
"""  ( id_item, color_name, color_value )                     """
# colors = [ (7,'G0', 0), (9,'G1', 25), (5,'G2', 50), (10,'G3', 75),
#            (8,'G4', 100), (2,'G5', 125), (6,'G6', 150), (0,'G7', 175),
#              (4,'G8', 200), (1,'G9',225), (3,'G10',255)]


# colors = [ (2, 'G0', 0), (0, 'G5',63), (4, 'G1', 126), (1,'G2', 189), (3,'G3', 255),]
# list_items = [0, 1, 2, 3, 4]

colors = [ (1,'G0', 0), (2,'G5', 125),(3,'G2', 189), (0, 'G10', 255)]


nb_colors = len(colors)
random.shuffle(colors) #We are not supposed to have colors sorted nicely in a increasing way


# ESTIMATE VALUE COMPUTING : 
true_values = [0]*nb_colors
for i in range(0,nb_colors):
    true_values[colors[i][0]] = colors[i][2]



#exemple of an assessemnt :   (darkest, middle, lightest)
data = [  ((1,'G0', 0), ((2,'G5', 125),6), (0, 'G10', 255) ), 
        ((2,'G5', 125), ((3,'G2', 189),5),    (0, 'G10', 255)) ]

#First loop

d1 = data[0][1][1]
d2 = 10 - d1
alpha = d1 / d2
worst = data[0][0][0]
best = data[0][2][0]
mid = data[0][1][0][0]

#generate a row to add
new_row = [0]*nb_colors
b = [0]

new_row[worst] = 1
new_row[mid] = -(alpha + 1)
new_row[best] = alpha


A = np.array(new_row)
b = np.array(b)
print("A = ",A)
print("b = ",b)
for assessment in data[1:]:
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
    print("A = ",A)
    print("B =",b)

#Adding the 0 and 255 fixed points
A = np.vstack([A, [0,0,1,0]])
b = np.vstack([b, [125]])

A = np.vstack([A, [0,0,0,1]])
b = np.vstack([b, [189]])

# b[0] = 255
# b[1] = 1
# print("B =",b)
print("<============ RESULT ==============>")
# print(np.linalg.solve(A,b))
print(np.linalg.lstsq(A,b,rcond=None)[0])
# np.linalg.lstsq(np.vstack([]))

#TODO: 0 et 255 limit to add 

# print("RESULATAT  B = ",(-alpha*255) / -(alpha +1)) 