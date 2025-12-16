from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv

load_dotenv()

## setting up neccessaries

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
account_email = os.environ.get("ACCOUNT_EMAIL")
account_password = os.environ.get("ACCOUNT_PASSWORD")

gym_url = os.environ.get("GYM_URL")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)
driver.get(gym_url)

# Booking configuration
days_to_find = ["thu", "fri"]
time_to_find = "1900"

# Booking stats
stats = {
    "classes_booked": 0,
    "waitlists_joined": 0,
    "already_booked": 0,
    "new_bookings": [],
    "total_bookings": 0,
    "total_waitlists": 0
}


# retry logic 
def retry(func, retries=7, description=None):
    for attempt in range(retries):
        if func():
            return True  # Success, stop retrying
        print(f"Retry {attempt + 1} on {description}")
    return False  

# login logic
def login():
    try:
        log_in_btn_el = driver.find_element(By.ID, value="login-button")
        log_in_btn_el.click()
        email_el = driver.find_element(By.ID, value="email-input")
        password_el = driver.find_element(By.ID, value="password-input")
        submit_el = driver.find_element(By.ID, value="submit-button")
        email_el.clear()
        email_el.send_keys(account_email)
        password_el.clear()
        password_el.send_keys(account_password)
        submit_el.click()
        
        # Wait for welcome message to confirm login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "welcome-message"))
        )
        print("Login successful")
        return True
    except Exception:
        return False

def book_class():
    try:
        # Wait for schedule page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-selected-day='week']"))
        )
        
        for day_to_find in days_to_find:
            classes = driver.find_element(By.XPATH, f"//*[contains(@id, '{day_to_find}')]")
            split_classes = classes.text.split("\n")
            timed_classes = classes.find_element(By.XPATH, f".//*[contains(@id, '{time_to_find}')]")
            book_btn = timed_classes.find_element(By.XPATH, ".//*[contains(@id, 'book-button')]")
            split_timed_class = timed_classes.text.split("\n")
            format_message = f"{split_timed_class[0]} on {split_timed_class[1]}, {split_classes[0]}"
            
            btn_text = book_btn.text
            if btn_text in ["Booked", "Waitlisted"]:
                stats["already_booked"] += 1
                print(f"Already {btn_text.lower()}: {format_message}")
            elif btn_text == "Join Waitlist":
                book_btn.click()
                stats["waitlists_joined"] += 1
                stats["new_bookings"].append(f"[New Waitlist] {format_message}")
                print(f"Joined waitlist: {format_message}")
            else:
                book_btn.click()
                stats["classes_booked"] += 1
                stats["new_bookings"].append(f"[New Booking] {format_message}")
                print(f"Booked class: {format_message}")
        return True
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_my_bookings():
    try:
        my_bookings_link = driver.find_element(By.ID, value="my-bookings-link")
        my_bookings_link.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "confirmed-bookings-section"))
        )
        
        confirmed_bookings_section = driver.find_element(By.ID, value="confirmed-bookings-section")
        bookings = confirmed_bookings_section.find_elements(By.CLASS_NAME, value="MyBookings_bookingCard__VRdrR")
        stats["total_bookings"] = len(bookings)
    except Exception as e:
        print(f"Error getting bookings: {e}")
        return False

    try:
        waitlist_section = driver.find_element(By.ID, value="waitlist-section")
        waitlists = waitlist_section.find_elements(By.CLASS_NAME, value="MyBookings_waitlist__rD_tl")
        stats["total_waitlists"] = len(waitlists)
    except NoSuchElementException:
        stats["total_waitlists"] = 0

    # Print summary
    total_classes = stats["total_bookings"] + stats["total_waitlists"]
    print("\n--- BOOKING SUMMARY ---")
    print(f"Classes booked: {stats['total_bookings']}")
    print(f"On waitlist: {stats['total_waitlists']}")
    print(f"Already booked/waitlisted: {stats['already_booked']}")
    print(f"Total classes: {total_classes}")
    
    print("\n--- DETAILED CLASS LIST ---")
    if stats["new_bookings"]:
        for booking in stats["new_bookings"]:
            print(booking)
    else:
        print("No new bookings or waitlists")
    return True



# Main execution
if retry(login, description="Login"):
    retry(book_class, description="Book classes")
    retry(get_my_bookings, description="Get bookings")
else:
    print("Login failed after all retries")

# driver.quit()


