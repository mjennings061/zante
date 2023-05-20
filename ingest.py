import requests
import pandas as pd
from datetime import datetime, timedelta

def glucose_function():   
    # Functions
    def mgdl_to_mmoll(mgdl_value):
        mmoll_value = mgdl_value / 18.018
        mmoll_value_rounded = round(mmoll_value,1)
        return mmoll_value_rounded

    def format_date_time(date_string):
        # Convert dateString to datetime object
        date_obj = datetime.fromisoformat(date_string[:-1])

        # Format the date and time as per UK format
        formatted_date_time = date_obj.strftime("%d/%m/%Y %H:%M:%S")
        return formatted_date_time

    def minutes_since_last_data(date_string):
        last_data = datetime.fromisoformat(date_string[:-1])
        # Get the current datetime
        current_date = datetime.now()
        # Calculate the time difference in minutes
        time_diff = (current_date - last_data).total_seconds()/ 60
        result = round(time_diff)
        return result 
    #     print("current_date", current_date)
    #     print("last_data", last_data)
    #     print("diff", time_diff)
    #     print("result", result)

    # Source Glucode Values URL
    glucose_url = "https://markbt1d.azurewebsites.net/api/v1/entries.json?count=5&token=1d348fd125ae28c0"

    # Send GET request to the API
    response = requests.get(glucose_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()

        # Check if the 'entries' array is present in the response
        if len(data) > 0:
            # Extract the item from the first entry in the array
            latest_value = data[0]
            # Print the extracted item
            # print(latest_value)
        else:
            print("No entries found in the response.")
    else:
        print("Error: Failed to retrieve data from the API.")

    # Extract Latest Values
    dateString = latest_value['dateString']
    dateString_readable = format_date_time(dateString)
    time_since_reading = minutes_since_last_data(dateString)
    direction_value = latest_value['direction']
    glucose_value_mgdl = latest_value['sgv']
    glucose_value_mmol = mgdl_to_mmoll(glucose_value_mgdl)
    glucose_delta_mgdl = latest_value['delta']
    glucose_delta_mmol = mgdl_to_mmoll(glucose_delta_mgdl)

    # Print the latest values
    print("Date & Time:", dateString_readable)
    print("Time since last reading (seconds):", time_since_reading)
    print("Direction:", direction_value)
    print("Value mmol/L:", glucose_value_mmol)
    print("Delta mmol/L:", glucose_delta_mmol)
    output = [direction_value, glucose_value_mmol]
    return output


def average_carb_function():
    # treatments
    carb_url = "https://markbt1d.azurewebsites.net/api/v1/treatments?count=200&find[carbs][$gte]=1&find[created_at][$gte]=2023-05-13&token=hack-1d348fd125ae28c0"
    #&find[created_at][$lte]=2023-05-20

    # Send GET request to the API
    response = requests.get(carb_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()
        #print("data", data)

        # Check if the 'entries' array is present in the response
        if len(data) > 0:
            df = pd.DataFrame(data)

            # Convert the 'date' column to datetime format
            df['date'] = pd.to_datetime(df['date'], unit='ms')

            # Calculate the date for 5 days ago
            five_days_ago = datetime.now() - timedelta(days=5)

            # Filter the DataFrame for the previous 5 days (excluding the current day)
            filtered_df = df[(df['date'] >= five_days_ago) & (df['date'].dt.date != datetime.now().date())]

            # Calculate the average of the desired column
            total_carb_value = filtered_df['carbs'].sum()
            average_carb_value = total_carb_value / 5 
            print("Average carb value:", average_carb_value)
            return average_carb_value

        else:
            print("No entries found in the response.")
            return 1
    else:
        print("Error: Failed to retrieve data from the API.")
        return 1