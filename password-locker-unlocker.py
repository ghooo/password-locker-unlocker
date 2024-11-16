# This scripts solves password-locker.com sequential number-counting puzzles
# This Python script uses Selenium WebDriver to automate the process by detecting the target number, counting its occurrences in a grid, and submitting answers automatically.
# After completing all puzzles, it reveals the PIN code, reducing a 30+ minute manual task to under 2 minutes.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import time
import getpass  # For secure password input

def get_puzzle_progress(progress_text):
    # Extract current and total puzzles from text like "Solves: 0 / 90"
    match = re.search(r"Solves: (\d+) / (\d+)", progress_text)
    if match:
        return int(match.group(1)), int(match.group(2))
    raise ValueError(f"Could not parse puzzle progress. progress_text: {progress_text}")


def get_target_number(prompt_text):
    # Extract the number from text like "Enter the number of times X appears:"
    match = re.search(r"times (\d+) appears", prompt_text)
    if match:
        return int(match.group(1))
    raise ValueError("Could not find target number in prompt")

def solve_password_locker():
    # Get credentials securely
    print("\nPassword Locker Unlocker")
    print("-" * 25)
    username = input("Enter your username: ").strip()
    password = getpass.getpass("Enter your password: ").strip()
    
    if not username or not password:
        print("Error: Username and password cannot be empty")
        return
    
    # Initialize Chrome driver
    driver = webdriver.Chrome()
    
    try:
        # The following 2 lines specifiy chrome location for recording the demo
        # They are not needed will be removed
        # driver.set_window_position(-2888, -12)
        # driver.set_window_size(965, 1100)

        # Navigate to the website
        driver.get("https://password-locker.com/users/login/")
        
        # Wait for and fill in login credentials
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        # Click login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Wait for the first password item and click it
        first_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".password_block_card"))
        )
        first_item.click()
        
        while True:
            # Wait for the puzzle grid to appear
            time.sleep(2)  # Give the puzzle time to load
            
            # my-screentime-modal            
            # Check if we're done
            screentime_modal = driver.find_element(By.ID, "retrieve-screentime-passcode-modal")
            if "show" in screentime_modal.get_attribute("class").split():
                print("\nPuzzle completed! PIN dialog is now visible.")
                break

            # Get progress information
            progress_text = driver.find_element(By.ID, "progress").text
            current_solve, total_solves = get_puzzle_progress(progress_text)
            print(f"\nProgress: {current_solve} / {total_solves}")
            
            # Get the prompt text to determine which number we're counting
            prompt_text = driver.find_element(By.ID, "instructions").text
            target_number = get_target_number(prompt_text)
            print(f"Looking for occurrences of number: {target_number}")
            
            # Get all numbers from the grid
            grid_text = driver.find_element(By.ID, "numbers-array").text
        
            # # Count occurrences of target_number
            numbers = [int(num) for num in grid_text.split()]

            # Count occurrences of the target number
            count = numbers.count(target_number)
            print(f"Found {count} occurrences of {target_number}")
            
            # Find input field and submit answer
            answer_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "guess-textbox"))
            )
            answer_input.clear()
            answer_input.send_keys(str(count))
            answer_input.send_keys(Keys.RETURN)  # Send Enter key
            
            # # Wait a moment to see if the answer was accepted
            # time.sleep(2)
            
        # Wait for the "Show Pin All At Once" button and click it
        show_pin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Show Pin All At Once']"))
        )
        show_pin_button.click()        
        
        pin = driver.find_element(By.ID, "retrieve-progress-display").text
        print(f"The pin is: {pin}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        time.sleep(5)  # Give the puzzle time to load
        print()
        print()
        input("Press Enter to close the browser...")

if __name__ == "__main__":
    solve_password_locker()
