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
- create full CLI
    - https://towardsdatascience.com/how-to-write-user-friendly-command-line-interfaces-in-python-cc3a6444af8e
- add caveat to weight gain cals to increase gradually
- add exceptions to the standard macro formula
'''

import sys

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""


def calc_ree_tdee(person):
    weight = person.weight
    height = person.height
    age = person.age
    sex = person.sex
    activity_level = person.activity_level
    ree = 0
    # ree formulas for each sex
    if sex == 1: # 1 = male
        ree = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex == 2: # 2 = female
        ree = 10 * weight + 6.25 * height - 5 * age - 161

    # tdee formulas for each activity level
    if activity_level == 1:
        tdee = ree * 1.2
    elif activity_level == 2:
        tdee = ree * 1.375
    elif activity_level == 3:
        tdee = ree * 1.55
    elif activity_level == 4:
        tdee = ree * 1.725
    else:
        tdee = 0
    # set class attributes based on calculation outcome
    person.ree = ree
    person.tdee = tdee


def calc_macros(person):
    calories = person.tdee
    weight_lbs = person.weight * 2.205
    weight_goal = person.weight_goal # 1=loss, 2=maintain, 3=gain
    if weight_goal == 1:
        # reduce cal by 20%
        calories = calories - (calories * .20)
    elif weight_goal == 3:
        # increase cal by 20%
        calories = calories + (calories * .20)
    # else do nothing, calories are already maintenance level
    person.u_calories = round(calories)
    protein = round(weight_lbs * 0.825)
    fat = calories * 0.25
    fat = round(fat / 9)
    carbs = calories - protein - fat
    carbs = round(carbs / 4)

    # set the user atributes based off calculations
    person.u_protein = protein
    person.u_fat = fat
    person.u_carbohydrates = carbs


def build_user(get, user):
    # pass in a list of attributes you want to gather input for
    for attr in get:
        i = 0
        while i == 0:
            try:
                user.attr = int(input(f'{attr.title()}: '))
                i = 1
            except ValueError:
                print('\nERROR: INVALID INPUT')
                print(instruction)


def main():

    class Meal:
        name = ''
        ingredients = ''
        method = ''
        protein = 0
        carbohydrates = 0
        fat = 0
        calories = 0

    class User:
        sex = 0
        age = 0
        weight = 0
        height = 0
        activity_level = 0
        weight_goal = 0
        ree = 0
        tdee = 0
        diet_preference = 0
        meal_num = 3
        u_protein = 0
        u_carbohydrates = 0
        u_fat = 0
        u_calories = 0

    # create object from user class
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
    
    global instruction
    instruction = ('''
    INPUT INSTRUCTION:
    ----------------------------------------------------
    All input must be numerical...\n
    Sex:
       1 = male
       2 = female
    Activity_Level:
       1 = Sedentary (light daily activity like walking)
       2 = Light
       3 = Moderate
       4 = Very Active
    Weight_Goal:
       1 = Weight loss
       2 = Weight maintenance
       3 = Weight gain
    ''')

    print(instruction)
    # give function all relevant class attributes to retrieve input for
    needed_attr = ['sex', 'age', 'weight', 'height', 'activity_level', 'weight_goal']
    build_user(needed_attr, user_1)
    calc_ree_tdee(user_1)
    calc_macros(user_1)

    summary = (
        '\nYOUR DAILY INTAKE SUMMARY\n'
        '--------------------------\n'
        f'Total calories: {user_1.u_calories}\n'
        f'Protein: {user_1.u_protein}\n'
        f'Carbohydrates: {user_1.u_carbohydrates}\n'
        f'Fat: {user_1.u_fat}\n')
    print(summary)
        
if __name__ == "__main__":
    main()
