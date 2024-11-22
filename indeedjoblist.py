import requests
from bs4 import BeautifulSoup as bs
import csv


relative_url = 'https://ng.indeed.com/jobs?q={}&l={}'


def get_url(title,location):
    ''' Returns the absolute path '''    
    absolute_url = relative_url.format(title,location)
    return absolute_url

def jobdetails(card):
    '''Returns a tuple holding major job details'''
    new_text = ''
    job_tag = card.find('h2',attrs={'class':'jobTitle'})
    job = job_tag.find_all('span')
    if len(job) > 1:
        new_text = job[0].text.strip(',')
        job_title = job[1].get('title')
    else:
        job_title = job[0].get('title')

    #get company name
    company = card.find('span',attrs={'class':'companyName'}).text.strip()

    #get company location
    location = card.find('div',attrs={'class':'companyLocation'}).text.strip() 
    try:
        #get company salary
        salary = card.find('div',attrs={'class':'salary-snippet'}).text
        #get Urgently Hiring
        urgent = card.find('div',attrs={'class':'urgentlyHiring'}).text
    except AttributeError:
        urgent = ''
        salary = ''

    #get job snippet
    jobSnippet = card.find('div',attrs={'class':'job-snippet'}).text.strip()

    #get date posted
    date_posted = card.find('span',attrs={'class':'date'}).text.strip()

    if new_text != '' or urgent != '' or salary != '':
        records = (job_title,company,location,jobSnippet,date_posted,salary,new_text,urgent)
    else:
        records = (job_title,company,location,jobSnippet,date_posted)
    return records



def main(title,location):
    '''Runs the main program'''
    records = []

    url = get_url(title,location)
    while True:
        responses = requests.get(url)
        response = responses.text
        soup = bs(response,'html.parser')

        #get card 
        cards = soup.find_all('div','job_seen_beacon')
        for card in cards:
            record = jobdetails(card)
            records.append(record)

        try:
            url = 'https://ng.indeed.com/' + soup.find('a',{'aria-label':'Next'}).get('href')
        except AttributeError:
            break
    
    return records

if __name__ == '__main__':
    title = input('Enter job title: ')
    location = input('Enter location: ')
    record_list = main(title,location)

    try:
        with open('jobtrack.csv', mode='w',newline='', encoding='utf-8') as joborder:
            jobfile = csv.writer(joborder)
            jobfile.writerow(['Job Title','Company','Location','Job Description','Date Posted','Salary','New Job','Urgent']) 
            jobfile.writerows(record_list)
    except PermissionError:
        print('Please kindly close the csv file')
