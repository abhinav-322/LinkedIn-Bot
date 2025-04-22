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


def get_job_listings():
    print("Navigating to job listings...")
    driver.get("https://www.linkedin.com/jobs/collections/recommended")
    time.sleep(3)  # Wait for listings to load

    try:
        apply_button = driver.find_element(By.ID, "jobs-apply-button-id")
        if apply_button.text.strip() == "Easy Apply":
            apply_button.click()
            print("Clicked Apply button")

            time.sleep(3)  # Wait for the apply modal to load

            while True:
                try:
                    # Try clicking the "Next" button
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Continue to next step"]'))
                    )
                    time.sleep(5)
                    next_button.click()
                    print("Clicked Next button")
                    time.sleep(2)

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
                        break  # Exit after submission
                    except TimeoutException:
                        print("No Submit button found. Ending process.")
                        break

        elif apply_button.text.strip() == "Apply":
            print("Regular Apply job. Clicking and returning to LinkedIn tab.")
            apply_button.click()
            time.sleep(3)

            # Wait for new tab to open
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

            new_tabs = driver.window_handles
            for tab in new_tabs:
                if tab != original_window:
                    driver.switch_to.window(tab)
                    print("Switched to company tab.")
                    time.sleep(2)
                    driver.close()
                    print("Closed company tab.")
                    break

            driver.switch_to.window(original_window)
            print("🔙 Switched back to LinkedIn.")

    except Exception as e:
        print(f"Error in applying to job: {e}")

def apply_to_jobs_with_reloading(reload_count):
    for i in range(reload_count):
        print(f"\n Reload attempt {i+1} of {reload_count}")
        get_job_listings()
        print("Waiting before next reload...\n")
        time.sleep(2)  # Wait a few seconds before reloading

if linkedin_login():
    apply_to_jobs_with_reloading(10)

driver.quit()