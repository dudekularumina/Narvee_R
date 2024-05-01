from datetime import datetime, timedelta, date
import dateutil.parser as parser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
# import schedule
import time
import json
import re
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
yesterday=today-timedelta(days=5)
Yesterday=yesterday.strftime("%Y-%m-%d")
print("5 days back Date:", Yesterday)


os.environ['DISPLAY'] = ':2'



driver= webdriver.Chrome()
driver.get("https://edistaffing.com/jobs/")
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

#Date Filter
# start_date=Yesterday
# end_date=Today

#Job Sites Excel Sheet
df1=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/JobSites1.xlsx'))
df1 = df1.reset_index(drop=True)
# Skills from Job_description
df2=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/listofskills.xlsx'))


from Commonfields import Commonfields

# # API_ENDPOINT = "http://narveetech.com/usit/requirements_api?api_key=9010096292ce32bb78bce7fe6cbaedc8&username=lekhana.pmk@gmail.com&password=Lekhana123$"
# # API_ENDPOINT1 = "http://192.168.0.194/usit/requirements_api?api_key=9010096292ce32bb78bce7fe6cbaedc8&username=testingteam@narveetech.com&password=Nadmin123$"

def VirtualVocations(Commonfields, df, URL, startnum, endnum, pagestart, pageend):
    dic=Commonfields
    # print(URL)
# #     unique_job_ids=set()
# # #     # skill = 'Python'
    for i in range(startnum, endnum):
        
        for j in range(pagestart, pageend):
            skillname=df.loc[i, 'SkillName'] 
            url=URL.format(a=df.loc[i, 'skill5'])


            print('url:', url)
            time.sleep(5)
            driver.get(url)

            time.sleep(5)
            jobelems=driver.find_elements(By.CLASS_NAME, 'job')
            print('ResultContent: ', len(jobelems))

            for k in jobelems:


                a_element = k.find_element(By.TAG_NAME, 'a')

                # Retrieve the href attribute
                jd_link = a_element.get_attribute('href')
                dic['job_link'].append(jd_link)



                # Retrieve the text within the <a> tag
                job_role = a_element.text.strip()
                dic['job_title'].append(job_role)

                # Print the extracted information
                # print("Job Description Link:", jd_link)
                # print("Job Role:", job_role)

                # driver.implicitly_wait(10)
                job_id=k.find_element(By.CLASS_NAME, 'jobno')
                print("Job ID:", job_id.text)

                
                print("Link:", jd_link)
                page = requests.get(jd_link).text 
                    #print(f'Page: {page}')
                    
                soup = BeautifulSoup(page, 'html.parser')

                job_location = soup.find('li', class_='left').find('strong').text.strip()
                print("Job Location:", job_location)
                dic['job_location'].append(job_location)



                # Fetch posted date
                posted_date = soup.find('li', class_='right').find('strong').text.strip()
                print("Posted Date:", posted_date)
                dic['posted_on'].append(posted_date)


                job_type = soup.find('li', class_='left').find('strong').text.strip()
                print("Job Type:", job_type)
                dic['Employment_type'].append(job_type)


                job_description = soup.find('div', class_='description').text.strip()
                print("Job Description:", job_description)
                dic['job_description'].append(job_description)



               








    dice=pd.DataFrame(dict([(k,pd.Series(dic[k])) for k in dic])) 
    
    return dice
#     # print(dice)


virtual_vocations=VirtualVocations(Commonfields(), df, df1.loc[22, 'ContractURL'], startno, endno, 1,2)
print(virtual_vocations)





dataframes=[VirtualVocations]

data = pd.DataFrame(Commonfields())

for dice in dataframes:
    data = pd.concat([data, pd.DataFrame(dice.__dict__)], ignore_index=True)
data=data.drop_duplicates()







output_dir = '/Users/admin/Documents/'

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
# import time
time = datetime.now().strftime('%H-%M-%S') 
# Specify the path to the Excel file within the created directory
excel_file_path = os.path.join(output_dir, f'data(EDI_Staffing)-{time}-{Today}.xlsx')

# Write the DataFrame to an Excel file in the created directory
virtual_vocations.to_excel(excel_file_path, index=False)

print(f"Excel file saved at: {excel_file_path}")




