import requests
import json
import csv
from datetime import datetime
from collections import defaultdict

def Covid_stats():
    # CDC API info
    DATASET_ID = "pwn4-m3yp"
    BASE_URL = f"https://data.cdc.gov/resource/{DATASET_ID}.json"
    
    # list to store results for the final summary of all the states
    all_state_data = []

    # map month numbers to names for display
    month_map = {
        1: "January", 
        2: "February", 
        3: "March", 
        4: "April",
        5: "May", 
        6: "June", 
        7: "July", 
        8: "August",
        9: "September", 
        10: "October", 
        11: "November", 
        12: "December"
    }

    # read states and populations from states CSV file
    try:
        with open('states.csv', 'r') as statesfile:
            reader = csv.reader(statesfile)
            states_list = list(reader)
    except FileNotFoundError:
        print("Error: file not found.")
        return

    # for loop to go through each state and get the abbreviation and population
    for row in states_list:
        if not row: continue
        state_abbrev = row[0].strip()
        population = int(row[1].strip())

        # API info for the specific state and date range
        api_info = {
            "$where": f"state='{state_abbrev}' AND end_date >= '2020-01-01' AND end_date <= '2023-12-31'",
            "$order": "end_date ASC",
            "$limit": 5000  # makes sure we get all weeks
        }

        try:
            # get data from the CDC API
            response = requests.get(BASE_URL, params=api_info)
            response.raise_for_status()
            data = response.json()

            # save the raw JSON data to a state specific JSON and makes it more readable (long format)
            with open(f"{state_abbrev}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

            if not data:
                print(f"No data found for {state_abbrev}")
                continue

            # process statistics
            total_cases = 0
            count_weeks = 0
            max_weekly_val = -1
            max_weekly_date = ""
            
            # dictionary to group cases by (Year, Month)
            monthly_totals = defaultdict(int)

            for entry in data:
                # new_cases is the field name for the 7 day sum in this dataset
                cases = int(float(entry.get('new_cases', 0)))
                # extract date
                date_str = entry.get('end_date', '').split('T')[0]
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                
                total_cases += cases
                count_weeks += 1

                # track highest single week
                if cases > max_weekly_val:
                    max_weekly_val = cases
                    max_weekly_date = date_str

                # group into monthly sums
                monthly_totals[(dt.year, dt.month)] += cases

            # calculate averages and peak month
            avg_weekly = total_cases / count_weeks if count_weeks > 0 else 0
            
            # find the peak month
            peak_month_key = max(monthly_totals, key=monthly_totals.get)
            peak_month_cases = monthly_totals[peak_month_key]
            peak_month_name = f"{month_map[peak_month_key[1]]} {peak_month_key[0]}"
            peak_month_percent = (peak_month_cases / population) * 100

            # store result for summary
            state_result = {
                'name': state_abbrev,
                'avg': avg_weekly,
                'max_date': max_weekly_date,
                'max_cases': max_weekly_val,
                'peak_month': peak_month_name,
                'peak_cases': peak_month_cases,
                'peak_percent': peak_month_percent,
                'pop': population
            }
            all_state_data.append(state_result)

            # print individual state output
            print(f"State name: {state_result['name']}")
            print(f"Average number of new weekly cases for the entire state dataset: {state_result['avg']:.2f}")
            print(f"Date with the highest new number of covid cases: {state_result['max_date']} ({state_result['max_cases']})")
            print(f"Month and Year, with the highest new number of covid cases: {state_result['peak_month']} ({state_result['peak_cases']})")
            print(f"Month and Year, with highest new number, percentage of population: {state_result['peak_percent']:.2f}% (Population: {state_result['pop']})")
            print("-" * 60)

        except Exception as e:
            print(f"Error processing {state_abbrev}: {e}")

    # final summary across all states and rounds peak percent to 2 decimal places
    if all_state_data:
        highest = max(all_state_data, key=lambda x: x['peak_percent'])
        lowest = min(all_state_data, key=lambda x: x['peak_percent'])

        print("******************** SUMMARY ACROSS ALL STATES ********************")
        print("State with HIGHEST percentage of population during its highest month:")
        print(f"{highest['name']} - {highest['peak_percent']:.2f}% in {highest['peak_month']} "
              f"({highest['peak_cases']} cases; Population: {highest['pop']})")
        
        print("State with LOWEST percentage of population during its highest month:")
        print(f"{lowest['name']} - {lowest['peak_percent']:.2f}% in {lowest['peak_month']} "
              f"({lowest['peak_cases']} cases; Population: {lowest['pop']})")

# run function to get covid stats
Covid_stats()