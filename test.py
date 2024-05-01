import time
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import atexit
import requests
def perform_linkedin_job_search(job_titles):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

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

    # sign in page for LinkedIn
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
    job_data = pd.DataFrame(columns=['Job_Title', 'Company_Name', 'Location', 'Job_Href'])
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input')))

    # # Perform the search
    # search_input = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')

    # # Clear the search input field before entering a new query
    # search_input.clear()

    # # Enter the new search query
    # search_input.send_keys(job_titles[1])
    # time.sleep(3)
    # search_input.send_keys(Keys.ENTER) 
    # time.sleep(2)

        

    # # Wait for the "Jobs" button to be clickable
    # jobs_button_xpath = "//button[text()='Jobs']"
    # try:
    #     WebDriverWait(driver, 13).until(EC.element_to_be_clickable((By.XPATH, jobs_button_xpath)))
    #     jobs_button = driver.find_element(By.XPATH, jobs_button_xpath)
    #     jobs_button.click()
    #     time.sleep(5)
    # except StaleElementReferenceException:
    #     print("Element reference is stale. Retrying...")
    #     time.sleep(2)  # Wait for the element to stabilize
    #     # Retry finding and clicking the element
    #     jobs_button = driver.find_element(By.XPATH, jobs_button_xpath)
    #     jobs_button.click()
    #     time.sleep(5)
    # except Exception as e:
    #     print("Error clicking Jobs button:", e)
    #       # Skip to the next iteration of the loop if an error occurs

    URL = 'https://www.linkedin.com/jobs/search/?currentJobId=3901699523&f_JT=C&f_TPR=r86400&geoId=103644278&keywords={a}&location=United%20States&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true&sortBy=R'

    # location_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "jobs-search-box-location-id-ember")]')))

    # # Clear the location input field
    # location_input.clear()

    # # Enter the desired location
    # location_input.send_keys("United States")  # Replace "Your Desired Location" with the location you want
    
    # # Press Enter to perform the search
    # location_input.send_keys(Keys.ENTER)
    # time.sleep(5)
    # # Find the button element
    # date_posted_button = driver.find_element(By.ID, "searchFilter_timePostedRange")

    # # Click on the button
    # date_posted_button.click()

    # # Find the label element
    # label_element = driver.find_element(By.XPATH, "//label[@for='timePostedRange-r86400']")

    # # Click on the label element
    # label_element.click()



    # # Get the current URL
    # url = driver.current_url
    

    # Loop through job titles
    for job_title in job_titles:
        driver.get((URL).format(a= job_title))
        print("URL-----------",(URL).format(a= job_title) )
        time.sleep(5)
        # Get HTML content of the page
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find job card elements
        job_cards = soup.find_all('li', class_='jobs-search-results__list-item')
        print(len(job_cards))

        # Loop through job cards
        for job_card in job_cards:
        
            # Extract job details
            job_title_element = job_card.find('a', class_='job-card-list__title')
            job_title = job_title_element.text.strip()
            job_href = job_title_element['href']  # Extracting href attribute
            job_href = "https://www.linkedin.com/" + str(job_href)
            print('Title:',job_title)
            print('Link:',job_href)
            company_name = job_card.find('span', class_='job-card-container__primary-description').text.strip()
            print(company_name)
            location = job_card.find('li', class_='job-card-container__metadata-item').text.strip()
            print('Location:',location)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            #print(soup)
            job_description_element = soup.find('div', class_='jobs-description')
            job_description = job_description_element.text.strip() #if job_description_element else None
            print(job_description)
            
            #time_posted = job_card.find('time').text.strip()
            
            print("---------------")
            job_data.loc[len(job_data)] = {'Job_Title': job_title,
                                            'Company_Name': company_name,
                                            'Location': location,
                                            'Job_Href': job_href} 
            


    # Save job data to Excel
    folder_path = "Job_Data"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "Job_Data.xlsx")
    job_data.to_excel(file_path, index=False)
    print(f"Job data saved to {file_path}")

    driver.quit()

# Example usage:
job_titles_to_search = ['Python', 'Data Scientist', 'Software Engineer']  # List of job titles to search
perform_linkedin_job_search(job_titles_to_search)
