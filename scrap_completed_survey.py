from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service  # Import the Service class
import time  # Import the time module

# Define login credentials
email = "abdulwaheed@datacrypt.ae"
password = "MJpi5:b49?aQ}63"

# Specify the path to the Firefox binary and GeckoDriver executable
firefox_binary_path = '/usr/bin/firefox'
geckodriver_path = '/usr/local/bin/geckodriver'

# Configure Firefox options with the binary path
firefox_options = webdriver.FirefoxOptions()
firefox_options.binary_location = firefox_binary_path

# Create a Service object with the path to the GeckoDriver executable
service = Service(geckodriver_path)

# Create a Firefox webdriver with the specified paths and options
driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    # Open the login page
    driver.get("https://tally.so/login")

    # Find and fill in the email and password fields
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Find and click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for the page to load after login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/forms/3jbLJ4']"))
    )

    # Find and click the anchor with href="/forms/3jbLJ4"
    anchor_element = driver.find_element(By.XPATH, "//a[@href='/forms/3jbLJ4']")
    anchor_element.click()

    time.sleep(10)

    # Wait for the page to load after login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/forms/3jbLJ4/submissions']"))
    )

    # Find and click the anchor with href="/forms/3jbLJ4/submissions"
    submissions_anchor = driver.find_element(By.XPATH, "//a[@href='/forms/3jbLJ4/submissions']")
    submissions_anchor.click()

    # Add a 10-second delay after clicking the anchor element
    time.sleep(10)

    # Find and click the anchor with href="/forms/3jbLJ4/submissions/completed"
    completed_anchor = driver.find_element(By.XPATH, "//a[@href='/forms/3jbLJ4/submissions/completed']")
    completed_anchor.click()

    # Add another 10-second delay after clicking the completed anchor element
    time.sleep(10)

    # Find and click the anchor with href="/forms/3jbLJ4/submissions/download?filter=completed"
    download_anchor = driver.find_element(By.XPATH, "//a[@href='/forms/3jbLJ4/submissions/download?filter=completed']")
    download_anchor.click()
    
    time.sleep(1000)

except TimeoutException:
    print("Timeout occurred while waiting for elements.")
except NoSuchElementException as e:
    print(f"Element not found: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser after execution
    driver.quit()
