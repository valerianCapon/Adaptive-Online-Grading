import numpy as np
from itertools import chain
import scipy as scp

def leastsq(A:np.array, b:np.array):
    inv = np.linalg.pinv(np.dot(A.T, b))
    cross = np.dot(inv, A.T)
    beta = np.dot(cross, b)
    return beta



A = np.array( [ 
 [0,0,1,0,0],
 [0,0,0,0,1],
 [0,1,-2,0,1],
 [1,2.33333333, 0,-3.33333333, 0],
 [0,2.33333333, 1,-3.33333333, 0],
 [1,0.       
 [0,2.33333333, 0,-3.33333333, 1],
 [1,0,0,0.66666667, -1.66666667],
 ])
b = np.array( 
 [[125],
 [75],
 [0],
 [0],
 [0],
 [0],
 [0],
 [0],
 ])

#/////////////////:
# inv = np.linalg.pinv(np.dot(A.T, A))
# print("inv =\n",inv)
# cross = np.dot(inv, A.T)
# beta = np.dot(cross, b)
#///////////////



# estimated_values = beta
# print("ajkzehiazhe =",estimated_values)
# estimated_values = scp.linalg.lstsq(A,b)[0]
estimated_values = np.linalg.lstsq(A,b,rcond=1e-12)[0]


#converting in a list
estimated_values = list(chain.from_iterable(estimated_values)) 
nb_colors = len(estimated_values)
for i in range(0,nb_colors):
    if estimated_values[i] < 0 :
        estimated_values[i] = 0
    elif estimated_values[i] > 255 :
        estimated_values[i] = 255
    else :
        estimated_values[i] = round(estimated_values[i])


true_values = [0,255, 125, 189,75]

""" Here we use the true values but since we aren't supposed to know about them 
we should use the RMSE computed from the judge's previous judgements of before this CTJ assessement"""
estimated_STD = np.std(estimated_values)
MSE = np.square(np.subtract(true_values, estimated_values)).mean()
true_STD_squared = estimated_STD**2 - MSE
SSR = true_STD_squared / estimated_STD**2
print("| SSR = [ ",SSR," ] |\n")   



print(estimated_values)
print(true_values)
# print(np.linalg.lstsq(A,b,rcond=None))