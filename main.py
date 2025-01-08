import logging
import time
from utils.driver import setup_driver
from pages.login_page import LoginPage
from pages.otp_page import OTPPage
from pages.home_page import HomePage
from pages.chapterwise_test_page import ChapterwiseTestPage
from pages.quick_exam_page import QuickExamPage

def run_automation():
    driver = None
    try:
        driver = setup_driver()
        login_page = LoginPage(driver)
        otp_page = OTPPage(driver)
        home_page = HomePage(driver)
        chapterwise_test_page = ChapterwiseTestPage(driver)
        quick_exam_page = QuickExamPage(driver)
        
        if login_page.is_on_login_screen():
            logging.info("On login screen. Performing login.")
            if not login_page.login():
                raise Exception("Login failed. Aborting automation.")
            
            time.sleep(5)
            
            if otp_page.is_on_otp_screen():
                logging.info("OTP screen detected. Entering OTP.")
                if not otp_page.enter_otp():
                    raise Exception("OTP entry failed. Aborting automation.")
                time.sleep(5)
        else:
            logging.info("Not on login screen. Proceeding to check for popup and home screen.")
        
        if not home_page.handle_popup_and_check_home():
            raise Exception("Failed to reach home screen after handling popup")
        
        home_page.perform_scroll()
        logging.info("Scroll actions completed successfully")

        # Chapterwise Test
        if not home_page.navigate_to_test_tab():
            raise Exception("Failed to navigate to Test tab")
        
        if not home_page.navigate_to_chapterwise_test():
            raise Exception("Failed to navigate to Chapterwise test section")
        
        if not chapterwise_test_page.select_all_checkboxes():
            raise Exception("Failed to select all checkboxes in Chapterwise test")
        
        if not chapterwise_test_page.enter_number_of_questions(30):
            raise Exception("Failed to enter number of questions and tap coordinates for Chapterwise test")
        
        if not chapterwise_test_page.click_start_button():
            raise Exception("Failed to click Start button")
        
        if not chapterwise_test_page.answer_multiple_questions():
            raise Exception("Failed to answer multiple questions, submit test, and handle popup in Chapterwise test")
        
        if not chapterwise_test_page.click_done_button():
            raise Exception("Failed to click Done button")
        

        # Quick Exam
        if home_page.is_on_test_tab_screen():
            logging.info("On Test tab screen. Navigating to Quick exam type.")
            if not home_page.navigate_to_quick_exam():
                raise Exception("Failed to navigate to Quick exam type")
        else:
            logging.error("Not on Test tab screen after completing Chapterwise test")
            raise Exception("Failed to reach Test tab screen")
        
        # Perform Quick Exam actions
        if not quick_exam_page.select_all_checkboxes():
            raise Exception("Failed to select all checkboxes in Quick exam")
        
        if not quick_exam_page.enter_number_of_questions():
            raise Exception("Failed to enter number of questions for Quick exam")
        
        if not quick_exam_page.click_start_button():
            raise Exception("Failed to click Start button for Quick exam")
        
        if not quick_exam_page.answer_multiple_questions():
            raise Exception("Failed to answer multiple questions in Quick exam")
        
        if not quick_exam_page.submit_test():
            raise Exception("Failed to submit the Quick exam")
        
        if not quick_exam_page.handle_popup_submit():
            raise Exception("Failed to handle popup submit for Quick exam")
        
        if not quick_exam_page.click_done_button():
            raise Exception("Failed to click Done button for Quick exam")
        
        logging.info("Automation completed successfully")
        
    except Exception as e:
        logging.error(f"An error occurred during automation: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run_automation()

