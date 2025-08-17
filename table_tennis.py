import requests
from bs4 import BeautifulSoup
import datetime

def scrape_ittf(num=10):
    try:
        num = max(1, num) # Ensure num is at least 1
        
        today = datetime.date.today()

        # find the nearest tuesday
        while today.weekday() != 1:
            today -= datetime.timedelta(days=1)

        # dynamically get the week number and month number (2 digits with leading zero)
        week_num = today.isocalendar()[1]
        month_num = f"{today.month:02d}"
        
        url = f"https://www.ittf.com/wp-content/uploads/2025/{month_num}/2025_{week_num}_SEN_MS.html"
        print(url)
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
        print(f"Men's Singles Ranking in Week {week_num} of 2025:")
        print("----------------------------------------------")

        # iterate through each row and print the data
        for row in rows:
            # go through <td> one by one
            cols = row.find_all('td')
            # print the text in each <td>
            for col in cols:
                print(col.text.strip(), end=' | ')
            print()
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")