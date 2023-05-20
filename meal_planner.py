import openai
import os
import json
from datetime import datetime

def create_prompt(condition, blood_glucose, delta_glucose, carbohydrates, tomorrow_business, tomorrow_schedule):
    """Create a string-based prompt suitable for OpenAI API."""
    # Create prompt
    time_now = datetime.now().strftime("%H:%M")
    JSON_FORMAT = """
    {
        "MealPlan": [
            {
                "Meal": "Breakfast",
                "Summary": "Toast with low fat yoghurt, blueberries and honey.",
                "Time": "08:00",
                "Carbohydrates": 40,
                "Ingredients": [
                    "1 slice wholegrain toast",
                    "200 g of low-fat yoghurt",
                    "1 teaspoon of honey",
                    "200 g of blueberries"
                ]
            }
        ]
    }
    """

    prompt_string = f"""Recommend a custom meal plan with times using the information below.

    Context about my day:
    I have {condition}. My blood glucose is {blood_glucose} mmol/L and {delta_glucose}. 
    My typical carbohydrate intake is {carbohydrates}g per day. I have a {tomorrow_business} day tomorrow with {tomorrow_schedule}.

    Ensure the output is JSON and can be loaded by python json.loads() in the following format:
    {JSON_FORMAT}
    """
    return prompt_string


def query_generative_api(prompt_string):
    """Query the OpenAI API to return a meal plan."""
    # Define model.
    MODEL = "text-davinci-003"

    # Query the API.
    response = openai.Completion.create(
    engine=MODEL,
    prompt=prompt_string,
    max_tokens = 800
    )

    # Get a response.
    generated_text = response.choices[0].text
    return generated_text


def create_meal_plan(condition, blood_glucose, delta_glucose, carbohydrates, tomorrow_business, tomorrow_schedule):
    """Create a meal plan for the following day based on a condition e.g. "Type 1 diabetes."""

    # Load the open ai key from system environment variables
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    # Create prompt.
    prompt = create_prompt(
        condition, 
        blood_glucose, 
        delta_glucose, 
        carbohydrates, 
        tomorrow_business, 
        tomorrow_schedule
    )

    # Query the API for a JSON meal plan.
    print("Generating meal plan...")
    meal_plan = query_generative_api(prompt)
    
    try:
        json_plan = json.loads(meal_plan)
    except:
        print(f"Trouble with the JSON file")
        error_prompt = f"""This is not a valid JSON. Refactor it to be valid. 
        Output only a JSON from this:\n\n{meal_plan}"""
        meal_plan = query_generative_api(error_prompt)
        try:
            json_plan = json.loads(meal_plan)
        except:
            print(f"Trouble with the JSON file x2")
            with open('example.json') as file:
                json_plan = json.load(file)
 
    return json_plan
    

if __name__ == "__main__":
    # Create some example parameters,
    condition = "type 1 diabetes"
    blood_glucose = 5.5             # mmol/L
    delta_glucose = "dropping"
    carbohydrates = 300    # grams
    tomorrow_business = "busy"
    tomorrow_schedule = "many meetings in the morning"

    # Create the meal plan.
    meal_plan = create_meal_plan(condition, blood_glucose, delta_glucose, carbohydrates, tomorrow_business, tomorrow_schedule)
    print(json.dumps(meal_plan, indent=2))
    