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
import pymysql
from hashlib import md5
nlp = spacy.load('en_core_web_sm')
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

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
# -
driver_path = ChromeDriverManager().install()
service = ChromeService(driver_path)
# mydb = pymysql.connect(
# #  host="69.216.19.140",
#  host = "localhost",
#   user="root",
#   password="Nadmin123$",
#   database="usitportal"
# )


from datetime import datetime
curr_dt = datetime.now()
timestamp = int(round(curr_dt.timestamp()))



# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':2'  # Replace ':2' with the desired display number# Set the DISPLAY environment va
#from pyvirtualdisplay import Display
#display = Display(visible=0,size=(800,800))
#display.start()

options.headless = True
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# chromedriver url link
#driver=webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
#driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.indeed.com")


#dirname = os.path.dirname('__file__')
dirname = os.path.dirname(os.path.abspath(__file__))
#dirname = os.getcwd()

print("Directory name - ", dirname)
# +
today = date.today()
Today=today.strftime("%Y-%m-%d")
yesterday = today - timedelta(days = 5)
#Yesterday="01 Jan 2023"
Yesterday = yesterday.strftime("%Y-%m-%d")

#i'm added 
log_directory = os.path.join(dirname, 'logfiles')
os.makedirs(log_directory, exist_ok=True) 
# Set up logging
log_file = os.path.join(log_directory, 'log-US-VirtualVocations-{d}.log'.format(d=Today))
logging.basicConfig(filename=log_file, filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#logging.basicConfig(filename=r'C:\Users\Dell\Documents\NarveeProject\webscrapping\logfiles\log-US-{d}.log'.format(d=Today), filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logging.basicConfig(filename=os.path.join(dirname, 'logfiles/log-US-dice-{d}.log'.format(d=Today)), filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

### skills category excel
df=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents//IT_skill_category_HOT.xlsx'))
# skill_category_files = ['/Users/admin/Documents/IT_skill_test.xlsx'] #'/Users/admin/Documents/IT_skill_category_java.xlsx', '/Users/admin/Documents/IT_skill_category_DotNet.xlsx', '/Users/admin/Documents/IT_skill_category_Andriod.xlsx'
# skills = ['Andriod','DotNet','HOT','Ios','java', 'python','salesforce','SAP_BW_Hana']
# #for skill_file in skill_category_files:
# #df = pd.read_excel(os.path.join(dirname, '/Users/admin/Documents/IT_skill_test.xlsx'))
    


#df=pd.read_excel(os.path.join(dirname, '/Users/admin/Documents/IT_skill_category09.xlsx'))

startno=0
endno=len(df)


##DateFilter
start_date = Yesterday
end_date = Today

## Job Sites Excel
df1=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/JobSites1.xlsx'))

## Skills from Job_description
df2=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/listofskills.xlsx'))

## import common fields dictionary
from Commonfields import Commonfields


API_ENDPOINT = "http://narveetech.com/usit/requirements_api?api_key=9010096292ce32bb78bce7fe6cbaedc8&username=lekhana.pmk@gmail.com&password=Lekhana123$"
API_ENDPOINT1 = "http://192.168.0.194/usit/requirements_api?api_key=9010096292ce32bb78bce7fe6cbaedc8&username=testingteam@narveetech.com&password=Nadmin123$"

def VirtualVocations(commonfields, df, URL, startnum, endnum, df2, pagestart, pageend):
    job = commonfields
    unique_job_ids = set() 

    for i in range(startnum, endnum):
        for j in range(pagestart, pageend):
            skillname = df.loc[i, 'SkillName']
            url = URL.format(a=df.loc[i, 'skill4'], b=j)
            time.sleep(5)
            print('url:', url)
            time.sleep(5)
            driver.get(url)
            
            time.sleep(5)
            #jobelems=driver.find_elements_by_tag_name('dhi-search-card')
            jobelems = driver.find_elements(By.XPATH, '//dhi-search-card')
        
            
            print('resultContent:',len(jobelems))               
            for k in jobelems:

                driver.implicitly_wait(10)
                role = k.find_element(By.CLASS_NAME, 'jobTitle')
                print(f'ROLE: {role.text}')
                # Find the link element
                link_element = role.find_element(By.XPATH, './@href')

                 # Get the 'href' attribute value
                id_value = role.get_attribute('href')
                print(f'ID: {id_value}')    
                 #id_value = k.find_element(By.CLASS_NAME, 'card-title-link').get_attribute('id')
                if id_value not in unique_job_ids:
                    unique_job_ids.add(id_value)                        
                    link ="https://www.indeed.com/" + str(id_value)
                    #print(f'LINK: {link}')

                    # Use attributes of Commonfields class to store data
                    
                    #print(f'Job Title :{role.text}')
                    company_elem = k.find_element(By.CLASS_NAME, 'ng-star-inserted')
                    company = company_elem.text
                    #print(company)
                    job['vendor'].append(company)
                    location = k.find_element(By.CLASS_NAME,'text-body').text
                    #print(location)
                    posted_on = k.find_element(By.CLASS_NAME,'posted-date').text
                    #print(f'Posted on: {posted_on}')
                    job['posted_on'].append(posted_on)
                    jobtype = k.find_element(By.CLASS_NAME,'card-position-type').text
                    #print(f"JOb Type: {jobtype}")
                    job['Employment_type'].append(jobtype)
                    page = requests.get(link).text 
                    #print(f'Page: {page}')
                    
                    soup = BeautifulSoup(page, 'html.parser')
                    job_desc = soup.find_all('div', class_='highlight-black')
                    desc = [i.text for i in job_desc]
                    job_description = " \n".join(desc)
                    job['job_description'].append(job_description)
                    #print(f'Job Description: {job_description}')
                    job['category_skill'].append(skillname)
                    #print(f'Skills: {skillname}')
                    try:
                        nlp1 = nlp(job_description)
                        noun_chunks = list(nlp1.noun_chunks)
                        tokens = [token.text for token in nlp1 if not token.is_stop]
                        skills = list(df2['Skill'])
                        skillset = []
                        for token in tokens:
                            if token.lower() in skills:
                                skillset.append(token)
                        for token in noun_chunks:
                            token = token.text.lower().strip()
                            if token in skills:
                                skillset.append(token)
                        skills1 = [v.capitalize() for v in set([v.lower() for v in skillset])]
                        skills1 = ",".join(skills1)
                        job['job_skills'].append(skills1)
                    except:
                        job['job_skills'].append('None')  
        
        
    # for r in range(len(getattr(job, 'job_title'))):
    #     getattr(job, 'job_country').append('United States')


    #dice = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in job.items()]))
    dice = pd.DataFrame(dict([(k, pd.Series(job[k])) for k in job]))
    

    return dice

# Example usage


logging.info('indeed')
virtual_vocations = VirtualVocations(Commonfields(), df, df1.loc[19, 'ContractURL'], startno, endno, df2, 1, 2)



# logging.info('Dice2 started')
# dice2 = Dice(Commonfields(), df, df1.loc[19, 'ContractURL'], startno, endno, df2, 2, 3)

#### Concat all the dataframes
logging.info('Concatenation of DataFrames started')
dataframes=[VirtualVocations] #,dice2
#print('DataFrame', dataframes)
#data=pd.concat(dataframes,ignore_index=True,sort=False)
data = pd.DataFrame(Commonfields())
for dice in dataframes:
    data = pd.concat([data, pd.DataFrame(dice.__dict__)], ignore_index=True)
data=data.drop_duplicates()
#print('Data',data)
# +
dictionary=Commonfields()

logging.info('Extracting Email,Phone')
from DataCleaning import extract_email,extract_mobile_number, clean_posted

data

for c in range(len(data)):
    dictionary['job_industry'].append('IT industry')
    #print(c)
    desc=data.iloc[c,5]
    #desc=data.iloc[c,8]
    #print(desc)
    try:
        email= extract_email(desc)
        dictionary['email'].append(email)
    except:
        dictionary['email'].append('None')
    try:
        phone= extract_mobile_number(desc)
        dictionary['phone'].append(phone)
    except:
        dictionary['phone'].append('None')

# data['email']=dictionary['email']
# data['phone']=dictionary['phone']
# data['job_industry']=dictionary['job_industry']
data['email'] = dictionary['email']
data['phone'] = dictionary['phone']
data['job_industry'] = dictionary['job_industry']
# +
logging.info('Data Cleaning started')
from DataCleaning import clean_posted,date_format,clean_text


data = data.dropna(subset=['posted_on'], axis=0)

data['posted_on'] = data['posted_on'].apply(lambda x: clean_posted(x))


data['posted_on'] = data['posted_on'].apply(lambda x: date_format(x))

data['job_description'] = data['job_description'].apply(lambda x: clean_text(x))

data=data.drop_duplicates()
logging.info('length of data after dropping the duplicates %s ',len(data))
# -
#data.to_excel(os.path.join(dirname, 'Alljobsscraped/dice09-{d}.xlsx'.format(d=today)), index=False)
#excel_file_path = os.path.join(dirname, f'Alljobsscraped/dice09-{today}.xlsx')
#data.to_excel(excel_file_path, index=False)

output_directory = os.path.join(dirname, 'Alljobsscraped')
os.makedirs(output_directory, exist_ok=True)


# Save the Excel file in the created directory
excel_file_path = os.path.join(output_directory, 'indeed09-{d}.xlsx'.format(d=today))



fd=pd.DataFrame(columns=data.columns)
Technology=list(df2.loc[0:24,'Technology'])
#Technology

print(data['job_title'].apply(type).unique())
data['job_title'] = data['job_title'].apply(lambda x: x.lower() if isinstance(x, str) else x)
for i in range(len(Technology)):
    fd1=data.set_index('job_title')
    fd1=fd1.filter(like=Technology[i],axis=0)
    fd1=fd1.reset_index()
    fd=pd.concat([fd1,fd],ignore_index=True,sort=False)
fd['job_title'] = fd['job_title'].str.title()

fd=fd.drop_duplicates()

fd['Employment_type']=fd['Employment_type'].apply(lambda x: 'Contract')
fd['phone']=fd['phone'].apply(lambda x: clean_posted(x))

logging.info('Execution End')

jobsource1=[]
jobsource=data['job_source']

# for source in jobsource:
#     source1=[]
#     source1.append(source)
#     print(source1)
#     jobsource1.append(source1)

# data['job_source']=jobsource

data['source'] = 'INDEED'
#data['created_date']=timestamp

data1=data[['job_title','vendor','job_location','posted_on','job_description','Employment_type','job_skills','job_source','email','phone','category_skill','source']]

data1 =data1.fillna('None') 

# Load unique vendors from Unique_Vendors_List.xlsx into a set
unique_vendors_file = '/Users/admin/Documents_Vendor_List.xlsx'
unique_vendors_df = pd.read_excel(unique_vendors_file)
unique_vendors_set = set(unique_vendors_df['Vendor'].str.lower()) 

print("Vendors:++++++", data['vendor'])

# Assuming 'data' is your DataFrame containing scraped data
for vendor in data['vendor']:
    vendor_lower = vendor.lower()  # Convert to lowercase for case-insensitive comparison
    if vendor_lower in unique_vendors_set:
        print(f"{vendor} is present 1")
    else:
        print(f"{vendor} is not present 0")

# mycursor = mydb.cursor()
# sql = "INSERT INTO tbl_rec_requirement (job_title,vendor,job_location,posted_on,job_description,Employment_type,job_skills,job_source,email,phone,category_skill,source) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# for i,row in data1.iterrows():
#     mycursor.execute(sql, tuple(row))
#     mydb.commit()
# mydb.close()





# +
    #data.to_excel(r'C:\Users\Dell\Documents\NarveeProject\webscrapping\Alljobsscraped\alljobs1-dice-2020-12-16.xlsx',index=False)
    # -

data1.to_excel(os.path.join(dirname,'indeed09-{d}.xlsx'.format(d=today)),index=False)

# output_directory = os.path.join(dirname, 'Alljobsscraped')
# os.makedirs(output_directory, exist_ok=True)

# # Save the Excel file in the created directory
# excel_file_path = os.path.join(output_directory, f'dice09-{today}.xlsx')
# data1.to_excel(excel_file_path, index=False)


def print_success_with_stars():
    name = "SUCCESS"
    characters = {
        'S': [' ****', '*    ', ' *** ', '    *', '*   *', '**** '],
        'U': ['*   *', '*   *', '*   *', '*   *', '*   *', ' *** '],
        'C': [' *** ', '*   *', '*    ', '*    ', '*   *', ' *** '],
        'E': ['**** ', '*    ', '***  ', '*    ', '*    ', '**** ']
    }

    for i in range(6):
        for char in name:
            print(characters.get(char, ['     '])[i], end='   ')
        print()

if __name__ == "__main__":                           
    print_success_with_stars()
                                           