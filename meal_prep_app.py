#!/usr/bin/env python3

'''
Meal plan creation based on user input
- take user input as daily macros
- search a database for meals that sum perfectly
- choices:
    - no. of meals (1-4)
    - diet choice (vego, pescatarian, meat-eater, low-carb, low-fat)

MILESTONES
------------------------------------------------------------------------------------------
- Create classes
- 
------------------------------------------------------------------------------------------
TODO
- create_user_profile function
- deal with weight / height conversions?
'''

import sys

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""


def create_user_profile(get=[]):
    for item in get:
        stop = 0
        while stop == 0:
            if item == ['age', 'weight', 'height']:
                try:
                    ask_item = int(input(item.title() + ': '))
                    user_1.item = ask_item
                    stop = 1
                except ValueError:
                    print('Please input valid ' + item)
            else:
                print('sex')

        
def main():

    ACTIVITY_LEVEL = {}
    WEIGHT_PREFERENCE = {}
    
    DIET_CHOICE = {
        'vegetarian':1,
        'pescetarian':2,
        'meat-eater':3
        }
    
    class Meal:
        name = ''
        ingredients = ''
        method = ''
        protein = 0
        carbohydrates = 0
        fat = 0
        calories = 0

    class User:
        sex = ''
        age = 0
        weight = 0
        height = 0
        activity_level = ''
        weight_preference = ''
        diet_preference = ''
        meal_num = 3
        u_protein = 0
        u_carbohydrates = 0
        u_fat = 0
        u_calories = 0

    user_1 = User()

    # deal with input and usage
    usage = ('\nUSAGE: project.py [DIETARY_PREF] [NO.OF_MEALS]\n\n'
             'DETARY_PREF: vegetarian OR pescetarian OR meat OR lowcarb\n'
             'NO.OF_MEALS: 1-4\n')
    meal_range = [1, 2, 3, 4]
    if len(sys.argv) != 3:
        print(usage)
        print(f'Arg0 = {sys.argv[0]}, argv1 = {sys.argv[1]}')
    elif sys.argv[1] in DIET_CHOICE:
        user_1.diet_preference = sys.argv[1]
        user_1.meal_num = sys.argv[2]
    elif sys.argv[2] in meal_range: #fix this later
        print(sys.argv[2])
    else:
        print(usage)

    print(f'\nYou chose {user_1.meal_num} {user_1.diet_preference} meals...\n'
          'Input your information below to calculate your macronutrients:\n')
    
    stop = 0
    while stop == 0:
        ask_sex = input('Biological sex: ').lower()
        if ask_sex == 'male':
            user_1.sex = 'male'
            stop = 1
        elif ask_sex == 'female':
            user_1.sex = 'female'
            stop = 1
        else:
            print('Invalid sex, please input a biological sex (Male, Female) for calculation purposes.')
            stop = 0

    stop = 0
    while stop == 0:
        try:
            ask_age = int(input('Age in years: '))
            user_1.age = ask_age
            stop = 1
        except ValueError:
            print('Please input valid age')

    stop = 0
    while stop == 0:
        try:
            ask_weight = int(input('Weight in kgs: '))
            user_1.weight = ask_weight
            stop = 1
        except ValueError:
            print('Please input valid weight')
            
    # create user macro profile
    #print('Please input your daily macronutrients below\n')
    #user_1.u_calories = input('Calories: ')
    #user_1.u_protein = input('Protein: ')
    #user_1.u_carbohydrates = input('Carbs: ')
    #user_1.u_fat = input('Fat: ')
        
if __name__ == "__main__":
    main()
