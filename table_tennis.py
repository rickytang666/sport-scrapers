import requests
from bs4 import BeautifulSoup
import datetime

'''
Currently only supports men's singles ranking.
'''

def scrape_ittf(date_query=None, num=10):
    try:
        num = max(1, num) # Ensure num is at least 1
        
        # Use today's date if no date is provided
        if date_query is None:
            date_query = datetime.date.today()

        # find the nearest tuesday
        while date_query.weekday() != 1:
            date_query -= datetime.timedelta(days=1)

        # only support years >= 2021

        if date_query.year < 2021:
            print("Year must be 2021 or later :(")
            return

        # dynamically get the week number and month number (2 digits with leading zero)
        year = date_query.year
        week_num = date_query.isocalendar()[1]
        month_num = f"{date_query.month:02d}"
        
        url = f"https://www.ittf.com/wp-content/uploads/{year}/{month_num}/{year}_{week_num}_SEN_MS.html"
        print(url)
        print()
        response = requests.get(url)
        if (response.status_code != 200):
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return
        my_html = BeautifulSoup(response.text, 'html.parser')

        # <tbody> tag
        table = my_html.find('tbody')
        # <tr> tags and with rrow classnames (only select first 10 rows)
        rows = table.find_all('tr', class_='rrow', limit=num)

        # print the header
        print(f"Men's Singles Ranking in Week {week_num} of {year}:")
        print("----------------------------------------------")

        # iterate through each row and print the data
        for row in rows:
            cols = row.find_all('td')
            # Remove <p> with rankup or rankdown class from the rank cell
            for tag in cols[0].find_all('p', class_=['rankup', 'rankdown']):
                tag.decompose()
            rank = cols[0].text.strip()
            name = cols[1].text.strip()
            nationality = cols[2].text.strip()
            points = cols[3].text.strip()
            print(f"{rank} {name} {nationality} {points}")
            print()
    
    except Exception as e:
        print(f"An error occurred: {e}")