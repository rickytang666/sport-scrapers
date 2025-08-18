from table_tennis import scrape_ittf
import datetime

date = datetime.date(2021, 7, 15)
top_num = 10

if __name__ == "__main__":
    scrape_ittf(date, top_num)