import functools
from flask import Flask, render_template, jsonify
import json
import meal_planner
from ingest import average_carb_function, glucose_function

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def meal_plan_api():
    # Format constants for generative API
    condition = "type 1 diabetes"
    blood_glucose = 5.5             # mmol/L
    delta_glucose = "dropping"
    carbohydrates = 300    # grams
    tomorrow_business = "busy"
    tomorrow_schedule = "many meetings in the morning"

    # Fetch input data from API.
    carbohydrates = average_carb_function()
    glucose = glucose_function()

    # Format data for Gen API.
    delta_glucose = glucose[0]
    blood_glucose = glucose[1]

    # Run generative API.
    meal_plan = meal_planner.create_meal_plan(
        condition, 
        blood_glucose, 
        delta_glucose,
        carbohydrates, 
        tomorrow_business, 
        tomorrow_schedule
    )
    print(json.dumps(meal_plan, indent=2))
    return jsonify(meal_plan)


@app.route('/')
def index():
    return render_template('index.html')