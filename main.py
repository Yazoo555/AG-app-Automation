import logging
import time
from utils.driver import setup_driver
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from pages.home_page import HomePage

def run_automation():
    driver = None
    try:
        driver = setup_driver()
        login_page = LoginPage(driver)
        otp_page = OTPPage(driver)
        home_page = HomePage(driver)
        
        if login_page.is_on_login_screen():
            logging.info("On login screen. Performing login.")
            if not login_page.login():
                raise Exception("Login failed. Aborting automation.")
            
            # Wait for a moment to let the screen transition
            time.sleep(5)
            
            if otp_page.is_on_otp_screen():
                logging.info("OTP screen detected. Entering OTP.")
                if not otp_page.enter_otp():
                    raise Exception("OTP entry failed. Aborting automation.")
                # Wait for a moment after OTP entry
                time.sleep(5)
        else:
            logging.info("Not on login screen. Proceeding to check for popup and home screen.")
        
        # Handle popup and check for home screen
        if not home_page.handle_popup_and_check_home():
            raise Exception("Failed to reach home screen after handling popup")
        
        # Perform scroll and like actions
        home_page.perform_scroll_and_like()
        logging.info("Automation completed successfully")
        
    except Exception as e:
        logging.error(f"An error occurred during automation: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run_automation()

