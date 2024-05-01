import time
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import atexit
import datetime

def scrape_linkedin_jobs(skills):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    # driver.maximize_window()

    # Function to release ChromeDriver
    def release_chromedriver():
        try:
            # Close the ChromeDriver session
            driver.quit()
            print("ChromeDriver released successfully.")
        except Exception as e:
            print(f"Error releasing ChromeDriver: {e}")

    # Register the release function to be called on script exit
    atexit.register(release_chromedriver)

    # Sign in page for LinkedIn
    driver.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")
    time.sleep(3)

    # Logging in to LinkedIn
    username = driver.find_element(By.ID, "username")
    username.send_keys("maheshwarisingatam@gmail.com")  # Replace with your LinkedIn username

    pwrd = driver.find_element(By.ID, "password")
    pwrd.send_keys("Mahi$9676")  # Replace with your LinkedIn password

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

    # Create an empty DataFrame to store job data
    job_data = pd.DataFrame(columns=['Job_Title', 'Company_Name', 'Location', 'Posted_Date'])

    # Loop through each skill
    for skill in skills:
        # Format the URL with the skill
        url = f"https://www.linkedin.com/jobs/search/?currentJobId=3913361157&f_JT=C&f_TPR=r86400&f_WT=2&keywords={skill}&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"

        # Open the URL
        driver.get(url)

        # Wait for the page to load
        # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results")))

        # Get the HTML content of the page
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

       # Find all job elements
        job_elements = driver.find_elements(By.XPATH, "//ul[@class='jobs-search__results-list']/li")
        print("Job elements", len(job_elements))
        # Iterate through each job element
        for job in job_elements:
            # Extract job details
            job_title = job.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
            company_name = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
            location = job.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
                # Extracting the posted date
            # Extracting the posted date
            posted_date_element = job.find_element(By.CLASS_NAME, "job-search-card__listdate--new")
            if posted_date_element:
                posted_date = posted_date_element.get_attribute("datetime")  # Extract the datetime attribute
                # Format the datetime object as desired
                posted_date = datetime.datetime.strptime(posted_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            else:
                print("No Posted date")  # Handle the case where the datetime attribute is not present
                # posted_date = ""
            
            a_element = job.find_element(By.TAG_NAME, 'a')

                # Retrieve the href attribute
            link = a_element.get_attribute('href')
            print("Link: ",  link)
        
            

            # Add job data to DataFrame
            job_data = job_data._append({'Job_Title': job_title,
                                        'Company_Name': company_name,
                                        'Location': location,
                                        'Link':link,
                                        'Posted_Date': posted_date}, ignore_index=True)


    return job_data

# Example usage:
skills = ['Python', 'Java', 'Software Development']  # List of skills to search
job_data = scrape_linkedin_jobs(skills)
print(job_data)
