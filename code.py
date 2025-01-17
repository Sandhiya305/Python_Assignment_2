import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert


# Function to read data from files and return as a dictionary
def read_data_from_file(file_path):
    input_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                input_data[key.strip()] = value.strip()
    return input_data


# Function to read locators from the file
def read_locators_from_file(file_path):
    locators = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                locators[key.strip()] = value.strip()
    return locators


# Function to read credentials from the file
def read_credentials_from_file(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                credentials[key.strip()] = value.strip()
    return credentials


# Function to perform the login operation
def login_to_salesforce(driver, username, password):
    driver.get("https://login.salesforce.com")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "Login").click()

# Function to create a lead
def create_lead(driver, locators, input_data):
    # Wait for the lead page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, locators['lead_name_xpath']))
    )
    # Create lead
    driver.find_element(By.XPATH, locators['lead_name_xpath']).click()
    time.sleep(2)
    driver.find_element(By.XPATH, locators['lead_first_name_xpath']).send_keys(input_data['lead_first_name'])
    time.sleep(2)
    driver.find_element(By.XPATH, locators['lead_last_name_xpath']).send_keys(input_data['lead_last_name'])
    time.sleep(1)
    driver.find_element(By.XPATH, locators['lead_company_xpath']).send_keys(input_data['lead_company'])
    driver.find_element(By.XPATH, locators['lead_save_button_xpath']).click()
    time.sleep(1)


# Function to create account (for use case-2)
def create_account(driver, locators, input_data):
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, locators['convert_button_xpath']))
    )

    # Create account
    driver.find_element(By.XPATH, locators['convert_button_xpath']).click()
    time.sleep(2)
    driver.find_element(By.XPATH, locators['convert2_button_xpath']).click()
    time.sleep(3)

# Function to attach contact to account
def attach_contact_to_account(driver, locators, input_data):
    driver.find_element(By.XPATH, locators['select_account']).click()
    time.sleep(1)
    driver.find_element(By.XPATH, locators['new_contact_button']).click()
    time.sleep(1)
    driver.find_element(By.XPATH, locators['contact_lastname_xpath']).send_keys(input_data['contact_last_name'].split(" ")[0])
    time.sleep(1)
    driver.find_element(By.XPATH, locators['contact_save_button']).click()
    time.sleep(1)

# Function to create opportunity
def create_opportunity(driver, locators, opportunity_data):
    # Create opportunity linked to the account
    driver.find_element(By.XPATH, locators['opportunity_button_xpath']).click()
    time.sleep(1)
    driver.find_element(By.XPATH, locators['opportunity_save_button']).click()
    time.sleep(3)

# Main function to execute both use cases
def main_use_case_1_and_2():
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Read locators, input data, and credentials from files
    locators = read_locators_from_file("locators.txt")
    #account_data = read_data_from_file("input_data.txt")
    input_data = read_data_from_file("input_data.txt")  # This would contain data like lead_name, lead_phone, etc.
    credentials = read_credentials_from_file("credentials.txt")

    username = credentials.get("username")
    password = credentials.get("password")

    # Perform login
    login_to_salesforce(driver, username, password)

    # Use Case 1: Create a Lead and convert it to an Account
    create_lead(driver, locators, input_data)
    # If needed, perform the conversion of the lead into an account (can be a manual step or automated)

    # Use Case 2: Create an Account, Attach Contact, and Create Opportunity
    create_account(driver, locators, input_data)
    attach_contact_to_account(driver, locators, input_data)
    create_opportunity(driver, locators, input_data)

    driver.quit()


if __name__ == "__main__":
    main_use_case_1_and_2()
