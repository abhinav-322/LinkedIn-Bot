from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Extract email and password
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
driver = webdriver.Chrome()
original_window = driver.current_window_handle

def linkedin_login():
    print("Logging into LinkedIn...")
    try:
        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        
        # Enter credentials
        driver.find_element(By.ID, "username").send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        # time.sleep(120)
        
        # Verify login success
        WebDriverWait(driver, 3000).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'global-nav__me')]"))
        )
        print("Login successful!")
        return True
        
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False


# def get_job_listings():
#     print("Navigating to job listings...")
#     driver.get("https://www.linkedin.com/jobs/collections/easy-apply")
#     time.sleep(3)  # Wait for listings to load

#     try:
#         apply_button = driver.find_element(By.ID, "jobs-apply-button-id")
#         if apply_button.text.strip() == "Easy Apply":
#             apply_button.click()
#             print("Clicked Apply button")

#             time.sleep(3)  # Wait for the apply modal to load

#             while True:
#                 try:
#                     # Try clicking the "Next" button
#                     next_button = WebDriverWait(driver, 5).until(
#                         EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Continue to next step"]'))
#                     )
#                     time.sleep(5)
#                     next_button.click()
#                     print("Clicked Next button")
#                     time.sleep(2)

#                 except TimeoutException:
#                     print("No Next button, checking for Review or Submit")

#                     try:
#                         # Check and click the "Review your application" button
#                         review_button = WebDriverWait(driver, 3).until(
#                             EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Review your application"]'))
#                         )
#                         time.sleep(5)
#                         review_button.click()
#                         print("Clicked Review button")
#                         time.sleep(2)
#                     except TimeoutException:
#                         print("No Review button found")

#                     try:
#                         # Check and click the "Submit application" button
#                         submit_button = WebDriverWait(driver, 3).until(
#                             EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Submit application"]'))
#                         )
#                         submit_button.click()
#                         print("Clicked Submit button")
#                         break  # Exit after submission
#                     except TimeoutException:
#                         print("No Submit button found. Ending process.")
#                         break

#         elif apply_button.text.strip() == "Apply":
#             print("Regular Apply job. Clicking and returning to LinkedIn tab.")
#             apply_button.click()
#             time.sleep(3)

#             # Wait for new tab to open
#             WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

#             new_tabs = driver.window_handles
#             for tab in new_tabs:
#                 if tab != original_window:
#                     driver.switch_to.window(tab)
#                     print("Switched to company tab.")
#                     time.sleep(2)
#                     driver.close()
#                     print("Closed company tab.")
#                     break

#             driver.switch_to.window(original_window)
#             print("🔙 Switched back to LinkedIn.")

#     except Exception as e:
#         print(f"Error in applying to job: {e}")

# def apply_to_jobs_with_reloading(reload_count):
#     for i in range(reload_count):
#         print(f"\n Reload attempt {i+1} of {reload_count}")
#         get_job_listings()
#         print("Waiting before next reload...\n")
#         time.sleep(2)  # Wait a few seconds before reloading

# if linkedin_login():
    apply_to_jobs_with_reloading(10)

# driver.quit()

def apply_this_job(job_url):
    # Store main window handle
    main_window = driver.current_window_handle
    
    try:
        # Open job in new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(job_url)
        print(f"\nProcessing job: {job_url}")
        
        # Wait for job page to load completely
        # WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.ID, "jobs-apply-button-id"))
        # )
        time.sleep(3)
        
        # Find and click apply button by ID
        try:
            buttons = driver.find_elements(By.ID, "jobs-apply-button-id")
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    btn.click()
                    break


            while True:
                try:
                    # Try clicking the "Next" button
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Continue to next step"]'))
                    )
                    time.sleep(3)
                    next_button.click()
                    print("Clicked Next button")
                    time.sleep(10)

                except TimeoutException:
                    print("No Next button, checking for Review or Submit")

                    try:
                        # Check and click the "Review your application" button
                        review_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Review your application"]'))
                        )
                        time.sleep(5)
                        review_button.click()
                        print("Clicked Review button")
                        time.sleep(2)
                    except TimeoutException:
                        print("No Review button found")

                    try:
                        # Check and click the "Submit application" button
                        submit_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Submit application"]'))
                        )
                        submit_button.click()
                        print("Clicked Submit button")
                        time.sleep(3)
                        break  # Exit after submission
                    except TimeoutException:
                        print("No Submit button found. Ending process.")
                        break
            
            
                
        except TimeoutException:
            print("Apply button not found or not clickable")
            
    except Exception as e:
        print(f"Error processing job: {str(e)}")
        
    finally:
        # Close job tab and return to main window
        try:
            if len(driver.window_handles) > 1:
                driver.close()
            driver.switch_to.window(main_window)
        except Exception as e:
            print(f"Error switching windows: {str(e)}")
        time.sleep(1)  # Brief pause before next job




def easy_jobs(num):
    try:
        for num in range(1, 11):  # Pages 1 to 10
            print(f"\n Visiting Page {num}...")

            if num == 1:
                print("\n This is the first page")
                driver.get("https://www.linkedin.com/jobs/collections/easy-apply")
            else:
                driver.get("https://www.linkedin.com/jobs/collections/easy-apply")
                time.sleep(3)
                next_page = f"Page {num}"
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'//button[@aria-label="{next_page}"]'))
                )
                time.sleep(2)
                # driver.execute_script("arguments[0].click();", next_page_button)
                next_page_button.click()
                time.sleep(5)
        
            # Wait for the jobs list to load (better than time.sleep)
            jobs_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.DgEiynQuYuEpvLebHnwINfbHjNGcXQNrexRNrM"))
            )
            
            jobs = jobs_list.find_elements(By.TAG_NAME, "li")
            print(f"Number of available jobs : {len(jobs)}")

            for job in jobs:
                try:
                    job_link = job.find_element(By.CSS_SELECTOR, "a.job-card-container__link")
                    job_url = job_link.get_attribute("href")  
                    
                    print(f"\nOpening job: {job_link.text.strip()}") 
                    print(f"URL: {job_url}")
                    
                    # driver.execute_script("window.open(arguments[0]);", job_url)
                    apply_this_job(job_url)
                    time.sleep(2)  # Wait for the new tab to load
                    
                    # Switch back to the main tab (if needed)
                    driver.switch_to.window(driver.window_handles[0])
                    
                except Exception as e:
                    print(f"Error processing job: {e}")
                    continue


    except Exception as e:
            print(f"Error loading jobs list: {e}")

    finally:
        driver.quit()  # Close the browser when done


if linkedin_login():
    easy_jobs(1)