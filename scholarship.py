'''Generates a csv file of latest scholarships from opportunitiespedia'''
import requests
from bs4 import BeautifulSoup as bs
import csv

def scholarship_detail(card):
    #title
    scholarships = card.find('a')
    scholarship_title = scholarships.get('title')

    #scholarship Page Link
    scholarship_link = scholarships.get('href')

    #get date 
    date_span = card.find('span',attrs={'class':'td-post-date'})
    dates = date_span.find('time').text

    try:
        summary = card.find('div',attrs={'class':'td-excerpt'})
        summary_text = summary.text.strip()
    except AttributeError:
        summary_text = ''

    result = (scholarship_title,dates,summary_text,scholarship_link)
    return result


def main(url): 
    scholarships = []
    while True:
        responses = requests.get(url)
        response = responses.text
        soup = bs(response,'html.parser')

        cards = soup.find_all('div','item-details')

        for card in cards:
            record = scholarship_detail(card)
            scholarships.append(record)
            
        pagination = soup.find('span',attrs={'class':'pages'}).text
        page_list = pagination.split()
        current_page = int(page_list[1])
        next_page = int(current_page) + 1
        last_page = 9

        if next_page > 1 and current_page < last_page :
            relative_url ="https://opportunitiespedia.com/category/scholarships/page/{}/"
            url = relative_url.format(next_page)
        else:
            return scholarships


if __name__ == '__main__':
    url = 'https://opportunitiespedia.com/category/scholarships/'
    a = main(url)
    try:
        with open('scholarship.csv', mode='w',newline='', encoding='utf-8') as scholarships:
            scholarship_file = csv.writer(scholarships)
            scholarship_file.writerow(['Title','Date','Summary','Scholarship Page Link']) 
            scholarship_file.writerows(a)
    except PermissionError:
        print('Please kindly close the csv file')