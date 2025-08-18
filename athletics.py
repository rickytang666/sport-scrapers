import requests
from bs4 import BeautifulSoup
import datetime
import urllib3

# Suppress SSL warning when using verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
Currently only supports men's 100m ranking (within top 100)
'''

def scrape_athletics(today, num=10):
    if num > 100:
        print("We only support top 100 athletes :(")
        return
    
    try:
        num = max(1, num)  # Ensure num is at least 1

        # date must be >= 2019-1-1
        if today.year < 2019:
            print("Year must be 2019 or later :(")
            return

        # find the nearest tuesday
        while today.weekday() != 1:
            today -= datetime.timedelta(days=1)

        year = today.year
        month_num = f"{today.month:02d}"
        day_num = f"{today.day:02d}"
        
        url = f"https://worldathletics.org/world-rankings/100m/men?regionType=world&page=1&rankDate={year}-{month_num}-{day_num}&limitByCountry=0"

        print(url)
        print()

        response = requests.get(url, verify=False)
        if response.status_code != 200:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return
        my_html = BeautifulSoup(response.text, 'html.parser')

        # find <tbody> tag
        table = my_html.find('tbody')
        # find <tr> tags and limit to the first 'num' rows
        rows = table.find_all('tr', limit=num)

        # print the header
        print(f"Men's 100m Ranking as of {today}:")
        print("----------------------------------------------")

        for row in rows:
            cols = row.find_all('td')
            rank = cols[0].text.strip()
            name = cols[1].text.strip()
            dob = cols[2].text.strip()
            nationality = cols[3].text.strip()
            points = cols[4].text.strip()
            print(f"{rank}  {name}  {dob}  {nationality}  {points}")
    except Exception as e:
        print(f"An error occurred: {e}")