# Make sure you guys installed below libraries if not use below command to insatll
# pip install beautifulsoup4
# pip install requests

from bs4 import BeautifulSoup
import requests
from datetime import date
from datetime import datetime
import smtplib

print("Sending Covid Stats...")

# Getting website details via request
html_text = requests.get('https://www.worldometers.info/coronavirus/').text

soup = BeautifulSoup(html_text, 'lxml')

# Total covid cases all over the world
case = soup.find_all('div', class_='maincounter-number')

# access details from worlometer covid-stats table
corona_stats = soup.find('table', id='main_table_countries_today')
all_country = corona_stats.find_all('tr')

# list to append India's Covid details
lst = []

# Finding Details
for rows in all_country:
    data = rows.find_all('td')
    row = [i.text for i in data]
    for i in row:
        # gathering india corona details in lst
        if 'India' in row:
            for j in row:
                data = (j)
                if(data != ''):
                    lst.append(data)
                else:
                    lst.append('0')
            break
# List contains all these informations
# [Country,TotalCases, NewCases, TotalDeaths, NewDeaths,
# TotalRecovered, NewRecovered, ActiveCases, Serious, Critical, Tot Cases/1M pop,
# Deaths/1M pop, TotalTests, Tests/1M pop, Population, 1 Case every X ppl, 1 Deathevery X ppl,
# 1 Testevery X ppl, New Cases/1M pop, New Deaths/1M pop, Active Cases/1M pop]

# Information that i need in the list
# ['Rank', 'Country', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
#              'TotalRecovered', 'ActiveCases', 'TotalTests', 'Population']

# deleting unwanted details in lst
del lst[16:19]
del lst[7]
del lst[14]
del lst[8:11]
del lst[9]

field_names = ['Rank', 'Country', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
               'TotalRecovered', 'ActiveCases', 'TotalTests', 'Population']

msg = []
for row in zip(field_names, lst):
    msg.append(' - '.join(row))

# message to be sent
subject = "India's Covid Stats"

# Current Date
today = date.today()
Current_day = today.strftime("%B %d, %Y")

# Current Time
time = datetime.now()
Current_time = time.strftime("%H:%M %p")

# India Covid Stats
Total_case = msg[2]
New_cases = msg[3]
Total_Death = msg[4]
Total_Recovered = msg[6]
Active_Cases = msg[7]
Total_Tests = msg[8]

# For Sending mail we are using SMPT librarie

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
# sender mail id
sender = ""

# sender's mail id's password
password = ""
s.login(sender, password)

# Messaging  Format
message = f'Subject:{subject}\n\n{subject}\n\n{Current_day,Current_time}\n\n{Total_case}\n\n{New_cases}\n\n{Total_Recovered}\n\n{Total_Death}\n\n{Active_Cases}\n\n{Total_Tests}'
# sending the mail

# receiver mail id
receiver = ""
s.sendmail(sender, receiver, message)

# terminating the session after sending mail
s.quit()

# After Sent the mail
print("Sent")
