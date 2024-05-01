from datetime import datetime, timedelta, date
import dateutil.parser as parser
from bs4 import BeautifulSoup
import pandas as pd
import requests
# import schedule
import time
import logging
import os
import spacy
# import pymysql
from hashlib import md5
# nlp = spacy.load('en_core_web_sm')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# # options = webdriver.ChromeOptions()
# # options.add_argument('--no-sandbox')
# # # -
# # driver_path = ChromeDriverManager().install()
# # service = ChromeService(driver_path)


# # mydb = pymysql.connect(
# # #  host="69.216.19.140",
# #  host = "localhost",
# #   user="root",
# #   password="Nadmin123$",
# #   database="usitportal"
# # )


# # options.headless = True


from datetime import datetime
curr_dt=datetime.now()
timestamp=int(round(curr_dt.timestamp()))
print("Time Stamp:", timestamp)


today=date.today()
Today=today.strftime("%Y-%m-%d")
print("Today Date:", Today)

os.environ['DISPLAY'] = ':2'


driver= webdriver.Chrome()
driver.get("https://www.randstadusa.com/jobs/q-recruiter/district-of-columbia/washington/mi-25/?gad_source=1&gclid=CjwKCAjwxLKxBhA7EiwAXO0R0N2YNlP8f2gzeOJSwb4oeWvbpWaiveUqqlLeD3vwm3lPnX_eHcjh3BoCtGwQAvD_BwE")
# print(driver)

dirname=os.path.dirname(os.path.abspath(__file__))
print("Directory Name - ", dirname)

# Create the log directory if it doesn't exist
log_directory=os.path.join(dirname, 'logfiles')
os.makedirs(log_directory, exist_ok=True)
#Set Up Logging

log_file=os.path.join(log_directory, 'log-US-VirtualVocations-{d}.log'.format(d=Today))
# This configures the logging system for the root logger.
logging.basicConfig(filename=log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

df=pd.read_excel(os.path.join(dirname,'c:/Users/admin/Documents/IT_skill_category_HOT.xlsx'))

startno=0
endno=len(df)

df1=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/JobSites1.xlsx'))
df1 = df1.reset_index(drop=True)
from jobfields import jobfields


def VirtualVocations(jobfields, df, URL, startnum, endnum, pagestart, pageend):
    data=jobfields
    # print(URL)
# #     unique_job_ids=set()
# # #     # skill = 'Python'
    for i in range(startnum, endnum):
        
        for j in range(pagestart, pageend):
            skillname=df.loc[i, 'SkillName'] 
            url=URL.format(a=df.loc[i, 'skill6'])
            # print('url:', url)
            time.sleep(5)
            driver.get(url)
            time.sleep(5)

            #cards_element = driver.find_element(By.CLASS_NAME, 'cards')

            print(url)
# Find all job card elements within the parent element cards__item 
            job_cards = driver.find_elements(By.CLASS_NAME, 'cards__item')
            # print('ResultContent: ', len(job_cards))
            
            for card in job_cards:
                a_element = card.find_element(By.TAG_NAME, 'a')

                # Retrieve the href attribute
                jd_link = a_element.get_attribute('href')
                # print(type(jd_link))
                # print("Job Link:", jd_link)
                data['job_link'].append(jd_link)



                # Retrieve the text within the <a> tag
                job_role = a_element.text.strip()
                data['job_role'].append(job_role)


                job_details_list = card.find_element(By.CLASS_NAME, 'cards__meta')

                # Extract job details from <li> elements
                job_details = job_details_list.find_elements(By.TAG_NAME, 'li')

                # Extracting job location, job type, and hourly rate from <li> elements
                job_location = job_details[0].text
                data['job_location'].append(job_location)
                job_type = job_details[1].text
                data['employment_type'].append(job_type)
                hourly_rate = job_details[2].text
                data['hourly_rate'].append(hourly_rate)

                time_info_div = card.find_element(By.CLASS_NAME, 'cards__time-info')

                # Extract posted date from the <span> element
                posted_date_element = time_info_div.find_element(By.CLASS_NAME, 'cards__date')
                posted_date = posted_date_element.text.strip()

                from datetime import datetime

                # Define the function to convert the posted date to the desired format
                def convert_posted_date(posted_date):
                    # Parse the posted date string
                    parsed_date = datetime.strptime(posted_date, "posted %B %d, %Y")
                    # Format the parsed date to the desired format
                    formatted_date = parsed_date.strftime("%Y-%m-%d")
                    return formatted_date

                # Call the function to convert the posted date
                formatted_posted_date = convert_posted_date(posted_date)
                # print("Formatted Posted Date:", formatted_posted_date)
                data['job_posted_on'].append(formatted_posted_date)
                

                # # Print job details
                # print("Job Role:", job_role)
                # # print("Job Posted Date:", posted_date)
                # print("Job Location:", job_location)

                # print("Job Type:", job_type)
                # print("Hourly Rate :", hourly_rate)
                # print("Job URL:", jd_link)


                page = requests.get(jd_link).text 
                    
                soup = BeautifulSoup(page, 'html.parser')

                job_summary_div = soup.find('div', class_='body-copy').find('div', class_='content')
                job_summary = job_summary_div.get_text(separator='\n',strip=True)
                # print("Job Summary:", job_summary)
                data['job_description'].append(job_summary)

            # # jobelems=driver.find_elements(By.CLASS_NAME, 'cards__list cards__list--format-grid')
            # # print('ResultContent: ', len(jobelems))






    dice=pd.DataFrame(dict([(k,pd.Series(data[k])) for k in data])) 
    
    return dice


virtual_vocations=VirtualVocations(jobfields(), df, df1.loc[23, 'ContractURL'], startno, endno, 1,2)
print(virtual_vocations)



dataframes=[VirtualVocations]

data = pd.DataFrame(jobfields())

for dice in dataframes:
    data = pd.concat([data, pd.DataFrame(dice.__dict__)], ignore_index=True)
data=data.drop_duplicates()







output_dir = '/Users/admin/Documents/'

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
# import time
time = datetime.now().strftime('%H-%M-%S') 
# Specify the path to the Excel file within the created directory
excel_file_path = os.path.join(output_dir, f'data(Randstand_USA)-{time}-{Today}.xlsx')

# Write the DataFrame to an Excel file in the created directory
virtual_vocations.to_excel(excel_file_path, index=False)

print(f"Excel file saved at: {excel_file_path}")


