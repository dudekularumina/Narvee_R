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


# import nlp


# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# # -
# driver_path = ChromeDriverManager().install()
# service = ChromeService(driver_path)


# mydb = pymysql.connect(
# #  host="69.216.19.140",
#  host = "localhost",
#   user="root",
#   password="Nadmin123$",
#   database="usitportal"
# )

from datetime import datetime
curr_dt=datetime.now()
timestamp=int(round(curr_dt.timestamp()))

os.environ['DISPLAY'] = ':2'

# options.headless = True

driver= webdriver.Chrome()
driver.get("https://www.Dice.com")
# print(driver)

dirname=os.path.dirname(os.path.abspath(__file__))
print("Directory Name - ", dirname)

today=date.today()
Today=today.strftime("%Y-%m-%d")
yesterday=today-timedelta(days=5)
Yesterday=yesterday.strftime("%Y-%m-%d")

# print(Today)
# print(Yesterday)


# Create the log directory if it doesn't exist
log_directory=os.path.join(dirname, 'logfiles')
os.makedirs(log_directory, exist_ok=True)
#Set Up Logging

log_file=os.path.join(log_directory, 'log-US-VirtualVocations-{d}.log'.format(d=Today))
# This configures the logging system for the root logger.
logging.basicConfig(filename=log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

df=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/test.xlsx'))

startno=0
endno=len(df)

#Date Filter
start_date=Yesterday
end_date=Today

#Job Sites Excel Sheet
df1=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/JobSites1.xlsx'))

#Skills from Job_description
df2=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/listofskills.xlsx'))


from Commonfields import Commonfields

# API_ENDPOINT = "http://narveetech.com/usit/requirements_api?api_key=9010096292ce32bb78bce7fe6cbaedc8&username=lekhana.pmk@gmail.com&password=Lekhana123$"
# API_ENDPOINT1 = "http://192.168.0.194/usit/requirements_api?api_key=9010096292ce32bb78bce7fe6cbaedc8&username=testingteam@narveetech.com&password=Nadmin123$"

def VirtualVocations(Commonfields, df, URL, startnum, endnum, df2, pagestart, pageend):
    dic=Commonfields
    unique_job_ids=set()
    # skill = 'Python'
    for i in range(startnum, endnum):
        for j in range(pagestart, pageend):
            skillname=df.loc[i, 'SkillName'] 
            url=URL.format(a=df.loc[i, 'skill4'], b=j)
            time.sleep(5)
            print('url:', url)
            time.sleep(5)
            driver.get(url)

            time.sleep(5)
            jobelems=driver.find_elements(By.XPATH, '//dhi-search-card')
            print('ResultContent: ', len(jobelems))

            for k in jobelems:

                # driver.implicitly_wait(10)
                role=k.find_element(By.CLASS_NAME, 'card-title-link')
                print("Job Title:", role.text)
                dic['job_title'].append(role.text)
                # link_element=role.find_element(By.CLASS_NAME, 'id')
                id_value = role.get_attribute('id')
                # dic['job_id'].append(id_value)
                print(id_value)
                link="https://www.dice.com/job-detail/" + str(id_value)
                dic['job_link'].append(link)
                print(link)
                company=k.find_element(By.CLASS_NAME, 'ng-star-inserted').text
                dic['vendor'].append(company)
                print(company)
                location=k.find_element(By.CLASS_NAME, 'search-result-location').text
                dic['job_location'].append(location)
                print(location)
                url = driver.current_url
                source = url.split('.')[1]
                # Print the source
                print("Source:", source)
                dic['source'].append(source)

                posted_on=k.find_element(By.CLASS_NAME, 'posted-date').text 
                posted_on_text = posted_on# Example text
                # Extracting the number of hours ago
                hours_ago = posted_on_text.split()[1]
                posted_on_text = posted_on # Example text
                # Extracting the number of hours ago
                if 'moments' in posted_on_text:
                    hours_ago = 1  # Assume it's posted 1 hour ago
                else:
                    hours_ago_text = posted_on_text.split()[1]
                    hours_ago = int(hours_ago_text)
                # hours_ago = int(hours_ago)
                # Subtract the number of hours from the current date and time
                posting_date =datetime.now() - timedelta(hours=hours_ago)
                posting_date=posting_date.strftime("%Y-%m-%d  %H:%M:%S")
                posting_date=str(posting_date)

                # Printing the posting date
                print("Posting Date:", posting_date)
                dic['posted_on'].append(posting_date)
                # print(posted_on)

                

                jobtype=k.find_element(By.CLASS_NAME, 'card-position-type').text
                if jobtype not in 'Full-time':
                    dic['Employment_type'].append(jobtype)
                    print(jobtype)
                    # headers=

                page_response = requests.get(link).text
                # print(page_response)
                soup = BeautifulSoup(page_response, 'html.parser')







                # print(soup)
                skills_section = soup.find('div', class_='Skills_chipContainer__mlLa7')
                # print("Skills Secxtion:", skills_section)
                try:
                 if skills_section:
                    skills_spans=skills_section.find_all('span')
                    job_skills = ', '.join(span.text for span in skills_spans)                    
                    print("Job_Skills:", job_skills)
                except:
                   print("Skills Not Fetched")



                job_description_container = soup.find('div', class_='job-description')
                # print("job_description_container:",job_description_container)

                # Remove square brackets from the string
                try:
                
                 if job_description_container:
                    job_des=[i.text for i in job_description_container]
                    job_description_text = ''.join(job_des)
                    cleaned_job_description_text = job_description_text.strip('[]')



                    print("Job_Description:", cleaned_job_description_text)


                except:
                   print("Description  Not Fetched")
            


                dic['job_description'].append(cleaned_job_description_text)
                dic['job_skills'].append(job_skills)









    dice=pd.DataFrame(dict([(k,pd.Series(dic[k])) for k in dic])) 
    
    return dice
    # print(dice)


virtual_vocations=VirtualVocations(Commonfields(), df, df1.loc[19, 'ContractURL'], startno, endno, df2, 1,2)
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
excel_file_path = os.path.join(output_dir, f'data(dice)-{time}-{Today}.xlsx')

# Write the DataFrame to an Excel file in the created directory
virtual_vocations.to_excel(excel_file_path, index=False)

print(f"Excel file saved at: {excel_file_path}")















# # Create the directory if it doesn't exist
# output_dir = '/Users/admin/Documents/'
# os.makedirs(output_dir, exist_ok=True)

# # Specify the path to the Excel file within the created directory
# excel_file_path = os.path.join(output_dir, 'virtual_vocations.xlsx')

# # Write the DataFrame to an Excel file in the created directory
# virtual_vocations.to_excel(excel_file_path, index=False)




# # print(dataframes)
# data = pd.DataFrame(Commonfields())
# for dice in dataframes:
#     data = pd.concat([data, pd.DataFrame(dice.__dict__)], ignore_index=True)
# data=data.drop_duplicates()





# # print(data)
# data1=data[['job_title','job_id','job_link','vendor','job_location','posted_on','Employment_type','job_description', 'job_skills']]
# print(data1)
# print('Data',data)
# +
# dictionary=Commonfields()










# print(data)

# for d in dataframes:
#     data=pd.concat([data, pd.DataFrame(d.__dict__)], ignore_index=True)
# data=data.drop_duplicates()
# dataframes=[VirtualVocations] #,dice2
# #print('DataFrame', dataframes)
# #data=pd.concat(dataframes,ignore_index=True,sort=False)
# data = pd.DataFrame(Commonfields())




# for dice in dataframes:
#     data = pd.concat([data, pd.DataFrame(dice.__dict__)], ignore_index=True)
# data=data.drop_duplicates()
# print('Data',data)



# data.to_excel('/Users/admin/Documents/data.xlsx', index=False)












# +
# dictionary=Commonfields()

# print(data)

# output_dir=os.path.join(dirname)
# os.makedirs(output_dir, exist_ok=True)

# excel_file_path = os.path.join(output_dir, 'data(dice)-{d}.xslx'.format(d=today))


# data1=data[['job_title','job_id','job_link','vendor','job_location','posted_on','Employment_type',]]
# print(data1)
# Create the directory if it doesn't exist
# output_dir = '/Users/admin/Documents/data(dice)-{d}.xslx'.format(d=today)
# os.makedirs(output_dir, exist_ok=True)

# Specify the path to the Excel file within the created directory
# excel_file_path = os.path.join(output_dir, 'data.xlsx')

# Write the DataFrame to an Excel file in the created directory
# data.to_excel(excel_file_path, index=False)

# data.to_excel('/Users/admin/Documents/data.xlsx', index=False)

# # Write the DataFrame to an Excel file
# # dice.to_excel(excel_file_path, index=False)

# output_dir = os.path.join(dirname, 'jobsscraped')
# os.makedirs(output_dir, exist_ok=True)

# excel_file_path = os.path.join(dirname, 'data(dice)-{d}.xlsx'.format(d=today))
# # print(excel_file_path)

# virtual_vocations.to_excel(excel_file_path, index=False)



# data1=dic[['job_title','vendor','job_location','posted_on','job_description','Employment_type','job_skills','job_source','email','phone','category_skill','source']]

# data1 =data1.fillna('None')




