from .models import *




def generate_assessments(color_set_assessmnt:ColorSetAssessment):
    color_set_assessmnt.nb_of_assmnt_max = get_nb_max_of_assment(color_set_assessmnt)
    list_of_colors = color_set_assessmnt.color_set.colors.all()
    print(list_of_colors) #TODO: à supr

    match color_set_assessmnt.type:
        #Rubric type of assessments
        case "r":
            for set_nb, color in range(0,color_set_assessmnt.nb_of_assmnt_max), list_of_colors:
                # ColorRubricAssessment.objects.create(
                #     name=color_set_assessmnt.name + 
                # )
                pass


def get_nb_max_of_assment(color_set_assessmnt:ColorSetAssessment) -> int:
    nb_of_assment = color_set_assessmnt.nb_of_assmnt_max
    match color_set_assessmnt.type:
        case "r":
            nb_of_assment = color_set_assessmnt.color_set.colors.count()

        #TODO: Set nb_max_of_assessments
        case "t":
            pass
        case "a":
            pass

    return nb_of_assment