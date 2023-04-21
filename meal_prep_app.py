#!/usr/bin/env python3

""" MACRO TETRIS
functionally similar: https://macromatch.net
Spoonacular API docs: https://spoonacular.com/food-api/docs

Meal plan creation based on user input
- take user input as daily macros
- search a database for meals that sum perfectly
- choices:
    - no. of meals (1-4)
    - diet choice (vego, pescatarian, meat-eater, low-carb, low-fat)

MILESTONES
------------------------------------------------------------------------------------------
x implement macro calculator
- search database to fill in those macros
- provide user with realistic meals to satisfy their macro needs
------------------------------------------------------------------------------------------
TODO
- create_user_profile from txt file? Use this as input? good practice?
- deal with weight / height conversions?
- create full CLI
    - https://towardsdatascience.com/how-to-write-user-friendly-command-line-interfaces-in-python-cc3a6444af8e
- add caveat to weight gain cals to increase gradually
- add exceptions to the standard macro formula
- add more customisation to recipe search, such as intolerances and cuisine preferences
- fix kcal / cal conversion
"""

import sys
import requests
import json
import random

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""


def jprint(obj):
    # create formatted string of python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def find_recipes(user):
    # pull values from user
    carb_per_meal = round(int(user.u_carbohydrates) / int(user.meal_num))
    prot_per_meal = round(int(user.u_protein) / int(user.meal_num))
    fat_per_meal = round(int(user.u_fat) / int(user.meal_num))
    cal_per_meal = round(int(user.u_calories) / int(user.meal_num))
    u_diet = ""  # change to user.diet_preference later

    api_key = "3988bf04a7524e5695cad2fd7ab2bb30"
    nutr = "addRecipeNutrition=true"
    diet = f"diet={u_diet}"

    # define acceptable bounds for each macronutrient
    # carbs
    max_carb = f"maxCarbs={carb_per_meal + 50}"
    min_carb = f"minCarbs={round(carb_per_meal / 2)}"

    # protein
    max_prot = f"maxProtein={prot_per_meal + 50}"
    min_prot = f"minProtein={round(prot_per_meal / 2)}"

    # fat
    max_fat = f"maxFat={fat_per_meal + 10}"
    min_fat = f"minFat={round(fat_per_meal / 2)}"

    # calories
    max_cal = f"maxCalories={cal_per_meal + 50}"
    min_cal = f"minCalories={round(cal_per_meal / 2)}"

    # get request from API
    req = requests.get(
        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}"
        f"&{diet}&{max_carb}&{min_carb}&{max_prot}&{min_prot}&{max_fat}&{min_fat}&{max_cal}&{min_cal}"
    )
    json = req.json()

    # print macros needed per meal, probably shouldnt be in this function
    print(f"Carbs per meal: {carb_per_meal}")
    print(f"Protein per meal: {prot_per_meal}")
    print(f"Fat per meal: {fat_per_meal}")
    print(f"Calories per meal: {cal_per_meal}\n")

    # print raw json object
    # jprint(json)

    meal_1 = Meal()
    meal_2 = Meal()
    meal_3 = Meal()
    meal_4 = Meal()

    user_meals = [meal_1, meal_2, meal_3, meal_4]

    meals = json["results"]

    # starting points for macro tetris
    starting_point = random.choice(meals)
    r_meal_1 = random.choice(meals)
    r_meal_2 = random.choice(meals)
    r_meal_3 = random.choice(meals)
    macros = starting_point["nutrition"]["nutrients"]

    # set user meal 4 to random starting point
    meal_4.name = starting_point["title"]
    for j in range(len(macros)):
        if macros[j]["name"] == "Calories":
            meal_4.calories = macros[j]["amount"]
        elif macros[j]["name"] == "Fat":
            meal_4.fat = macros[j]["amount"]
        elif macros[j]["name"] == "Carbohydrates":
            meal_4.carbohydrates = macros[j]["amount"]
        elif macros[j]["name"] == "Protein":
            meal_4.protein = macros[j]["amount"]

    # user's baseline macro data
    starting_macros = {
        "Protein": user.u_protein,
        "Fat": user.u_fat,
        "Carbohydrates": user.u_carbohydrates,
        "Calories": user.u_calories,
    }

    # checks that each macro user is above 10g
    for k, v in starting_macros.items():
        if v > 10:
            # subtract random choice meal from starting macros, setting starting macros to the difference
            for j in range(len(macros)):
                if k == macros[j]["name"]:
                    starting_macros[k] = v - macros[j]["amount"]

    print("Starting Macros after subtractions: ", starting_macros)
    print(f"Starting meal: {starting_point['title']}")

    # create list of recipe names being used
    recipes_in_use = []
    for i in range(len(user_meals)):
        if user_meals[i].name != "null":
            recipes_in_use.append(user_meals[i].name)

    # the loop that gave me hell
    # imports data (title, p, f, c, c) from api JSON obj into Meal() class
    for i in range(len(user_meals) - 1):
        if meals[i]["title"] not in recipes_in_use:
            user_meals[i].name = meals[i]["title"]
            recipes_in_use.append(user_meals[i].name)
            macros = meals[i]["nutrition"]["nutrients"]
            for j in range(len(macros)):
                if macros[j]["name"] == "Protein":
                    user_meals[i].protein = macros[j]["amount"]
                elif macros[j]["name"] == "Fat":
                    user_meals[i].fat = macros[j]["amount"]
                elif macros[j]["name"] == "Carbohydrates":
                    user_meals[i].carbohydrates = macros[j]["amount"]
                elif macros[j]["name"] == "Calories":
                    user_meals[i].calories = macros[j]["amount"]

    print(recipes_in_use)
    print(
        f"\nMeal 1: {meal_1.name}"
        f"\nProtein: {meal_1.protein}"
        f"\nFat: {meal_1.fat}"
        f"\nCarbs: {meal_1.carbohydrates}"
        f"\nCalories: {meal_1.calories}\n"
        f"\nMeal 2: {meal_2.name}"
        f"\nProtein: {meal_2.protein}"
        f"\nFat: {meal_2.fat}"
        f"\nCarbs: {meal_2.carbohydrates}"
        f"\nCalories: {meal_2.calories}\n"
        f"\nMeal 3: {meal_3.name}"
        f"\nProtein: {meal_3.protein}"
        f"\nFat: {meal_3.fat}"
        f"\nCarbs: {meal_3.carbohydrates}"
        f"\nCalories: {meal_3.calories}\n"
        f"\nMeal 4: {meal_4.name}"
        f"\nProtein: {meal_4.protein}"
        f"\nFat: {meal_4.fat}"
        f"\nCarbs: {meal_4.carbohydrates}"
        f"\nCalories: {meal_4.calories}\n"
    )


def calc_ree_tdee(person):
    weight = person.weight
    height = person.height
    age = person.age
    sex = person.sex
    activity_level = person.activity_level
    ree = 0
    # ree formulas for each sex
    if sex == 1:  # 1 = male
        ree = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex == 2:  # 2 = female
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
    weight_goal = person.weight_goal  # 1=loss, 2=maintain, 3=gain
    if weight_goal == 1:
        # reduce cal by 20%
        calories = calories - (calories * 0.20)
    elif weight_goal == 3:
        # increase cal by 20%
        calories = calories + (calories * 0.20)
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
                user.attr = int(input(f"{attr.title()}: "))
                i = 1
            except ValueError:
                print("\nERROR: INVALID INPUT")
    # build tdee / ree and macros breakdown for user


def main():
    DIET_CHOICE = {"vegetarian": 1, "pescetarian": 2, "meat-eater": 3}

    global Meal

    class Meal:
        name = "null"
        ingredients = "null"
        method = "null"
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

    # define instance of user() class based on my information
    user_1 = User()
    setattr(User, "sex", 1)
    setattr(User, "age", 25)
    setattr(User, "weight", 75)
    setattr(User, "height", 183)
    setattr(User, "activity_level", 3)
    setattr(User, "weight_goal", 3)

    # deal with input and usage
    usage = (
        "\nUSAGE: project.py [DIETARY_PREF] [NO.OF_MEALS]\n\n"
        "DETARY_PREF: vegetarian OR pescetarian OR meat OR lowcarb\n"
        "NO.OF_MEALS: 1-4\n"
    )
    meal_range = [1, 2, 3, 4]
    if len(sys.argv) != 3:
        print(usage)
        print(f"Arg0 = {sys.argv[0]}, argv1 = {sys.argv[1]}")
    elif sys.argv[1] in DIET_CHOICE:
        user_1.diet_preference = sys.argv[1]
        user_1.meal_num = sys.argv[2]
    elif sys.argv[2] in meal_range:  # fix this later
        print(sys.argv[2])
    else:
        print(usage)

    print(f"\nYou chose {user_1.meal_num} {user_1.diet_preference} meals...\n")

    global instruction
    instruction = """
    INPUT INSTRUCTION:
    ----------------------------------------------------
    All input must be numerical... please provide the following.\n
    Sex:
       1 = male
       2 = female
    Age (in years)
    Weight (in kg's)
    Height (in cm's)
    Activity_Level:
       1 = Sedentary (light daily activity like walking)
       2 = Light
       3 = Moderate
       4 = Very Active
    Weight_Goal:
       1 = Weight loss
       2 = Weight maintenance
       3 = Weight gain
    """

    # print(instruction)

    # NEGATED: only for getting input from user, currently using pre-built profile.
    # give function all relevant class attributes to retrieve input for
    # needed_attr = ["sex", "age", "weight", "height", "activity_level", "weight_goal"]
    # build_user(needed_attr, user_1)
    calc_ree_tdee(user_1)
    calc_macros(user_1)

    macro_summary = (
        "YOUR DAILY INTAKE SUMMARY\n"
        "--------------------------\n"
        f"Total calories: {user_1.u_calories}\n"
        f"Protein: {user_1.u_protein}\n"
        f"Carbohydrates: {user_1.u_carbohydrates}\n"
        f"Fat: {user_1.u_fat}\n"
    )
    print(macro_summary)
    find_recipes(user_1)


if __name__ == "__main__":
    main()
