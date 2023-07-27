import numpy as np
import scipy.stats as stats
import choix
import itertools
import random
## Generating random test data
set_of_color = { ('G1', 50), ('G2', 100), ('G3', 148), ('G4', 189), ('G5',240)}
list_of_judges = ['A','B','C','D','E']
nb_of_judge = 5


# ##==============================  Rubric ==============================
"""
    Method : just doing the average of the rubric assessments and
      it's supposed to give us an aproximation of the real color's value
"""
#generate using https://www.random.org/gaussian-distributions/
#Set at generate 5 number and a 20 standard deviation
rubric_assessments = {
    'G1': [55, 67, 53, 20, 31],
    'G2': [95, 82, 100, 98, 80],
    'G3': [150, 136, 123, 140, 155],
    'G4': [164, 171, 200, 183, 200],
    'G5': [249, 224, 238, 221, 236],
}

def simple_average(list:list):
    return sum(list)/len(list)

for key,value in rubric_assessments.items():
    rubric_assessments[key] = simple_average(value)
#print(rubric_assessments)


##==============================  ACJ ==============================
