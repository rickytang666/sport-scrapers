from table_tennis import scrape_ittf
from athletics import scrape_athletics
import datetime

date = datetime.date(2023, 7, 15)
top_num = 10

if __name__ == "__main__":
    scrape_athletics(date, 10)