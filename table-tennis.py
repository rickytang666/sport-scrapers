import requests
from bs4 import BeautifulSoup
import datetime

def scrape_ittf(num=10):
    try:
        num = max(1, num) # Ensure num is at least 1
        # dynamically calculate current week number
        today = datetime.date.today()
        week_num = today.isocalendar()[1]
        # if today is before tuesday, minus one
        if today.weekday() < 1:  # 0 is Monday, 1 is Tuesday
            week_num -= 1
        url = f"https://www.ittf.com/wp-content/uploads/2025/08/2025_{week_num}_SEN_MS.html"
        response = requests.get(url)
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

scrape_ittf(20)