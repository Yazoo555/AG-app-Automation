import logging
import time
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from utils.helpers import tap_element, wait_for_element, perform_touch_action
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class ChapterwiseTestPage(BasePage):
    def select_all_checkboxes(self):
        checkboxes = [
            self.CHECKBOX_1_LOCATOR,
            self.CHECKBOX_2_LOCATOR,
            self.CHECKBOX_3_LOCATOR,
            self.CHECKBOX_4_LOCATOR
        ]
        
        for i, checkbox in enumerate(checkboxes, 1):
            if not self.click_checkbox(checkbox):
                logging.error(f"Failed to select checkbox {i}")
                return False
            logging.info(f"Checkbox {i} selected successfully")
        
        logging.info("All checkboxes selected successfully")
        return True

    def click_checkbox(self, locator):
        try:
            checkbox = wait_for_element(self.driver, locator)
            if tap_element(self.driver, checkbox):
                logging.info(f"Successfully clicked checkbox at {locator}")
                return True
            else:
                logging.error(f"Failed to click checkbox at {locator}")
                return False
        except Exception as e:
            logging.error(f"Error clicking checkbox at {locator}: {str(e)}")
            return False

    def enter_number_of_questions(self, number):
        try:
            input_field = wait_for_element(self.driver, self.NUMBER_INPUT_LOCATOR)
        
            if not tap_element(self.driver, input_field):
                logging.error("Failed to tap the input field")
                return False
            logging.info("Successfully tapped the input field")
        
            time.sleep(1)
        
            input_field.clear()
        
            input_field.send_keys(str(number))
            logging.info(f"Successfully entered {number} into the input field")
        
            # Tap the coordinate (220, 135)
            if not perform_touch_action(self.driver, (220, 135), (220, 135)):
                logging.error("Failed to tap coordinate (220, 135)")
                return False
            logging.info("Successfully tapped coordinate (220, 135)")
        
            return True
        except Exception as e:
            logging.error(f"Error entering number of questions: {str(e)}")
            return False

    def click_start_button(self):
        try:
            start_button = wait_for_element(self.driver, self.START_BUTTON_LOCATOR)
            if tap_element(self.driver, start_button):
                logging.info("Successfully clicked the Start button")
                return True
            else:
                logging.error("Failed to click the Start button")
                return False
        except Exception as e:
            logging.error(f"Error clicking Start button: {str(e)}")
            return False

    def click_answer_option(self, option_locator):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                answer_option = wait_for_element(self.driver, option_locator, timeout=20)
                if tap_element(self.driver, answer_option):
                    logging.info(f"Successfully clicked the answer option {option_locator}")
                    return True
                else:
                    logging.warning(f"Failed to click the answer option {option_locator}. Attempt {attempt + 1} of {max_retries}")
            except Exception as e:
                logging.warning(f"Error clicking answer option {option_locator}: {str(e)}. Attempt {attempt + 1} of {max_retries}")
            
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
        
        logging.error(f"Failed to click answer option {option_locator} after {max_retries} attempts")
        return False

    def scroll_up(self):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                screen_size = self.driver.get_window_size()
                start_x = screen_size['width'] * 0.5
                start_y = screen_size['height'] * 0.8
                end_y = screen_size['height'] * 0.2

                TouchAction(self.driver).press(x=start_x, y=start_y).move_to(x=start_x, y=end_y).release().perform()
                logging.info("Successfully scrolled up")
                return True
            except WebDriverException as e:
                logging.warning(f"Error scrolling up: {str(e)}. Attempt {attempt + 1} of {max_retries}")
            
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
        
        logging.error(f"Failed to scroll up after {max_retries} attempts")
        return False

    def wait_for_next_question(self, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.ANSWER_OPTION_A_LOCATOR)
            )
            logging.info("Next question loaded successfully")
            return True
        except TimeoutException:
            logging.error(f"Timed out waiting for next question after {timeout} seconds")
            return False
        except Exception as e:
            logging.error(f"Error waiting for next question: {str(e)}")
            return False

    def answer_multiple_questions(self):
        total_questions = 30
        for i in range(total_questions):
            logging.info(f"Attempting to answer question {i+1}")
            
            if not self.wait_for_next_question():
                logging.error(f"Question {i+1} did not load. Attempting to recover...")
                if not self.recover_from_error():
                    logging.error("Failed to recover. Stopping the test.")
                    return False
                continue

            if i < 10:
                option_locator = self.ANSWER_OPTION_A_LOCATOR
            elif i < 20:
                option_locator = self.ANSWER_OPTION_B_LOCATOR
            else:
                option_locator = self.ANSWER_OPTION_C_LOCATOR
    
            if not self.click_answer_option(option_locator):
                logging.error(f"Failed to click answer for question {i+1}. Attempting to scroll.")
        
                if self.scroll_up():
                    time.sleep(1)
                    if not self.click_answer_option(option_locator):
                        logging.error(f"Failed to click answer for question {i+1} even after scrolling. Attempting to recover...")
                        if not self.recover_from_error():
                            logging.error("Failed to recover. Stopping the test.")
                            return False
                        continue
                else:
                    logging.error(f"Failed to scroll for question {i+1}. Attempting to recover...")
                    if not self.recover_from_error():
                        logging.error("Failed to recover. Stopping the test.")
                        return False
                    continue

            logging.info(f"Successfully answered question {i+1}")
            time.sleep(2)

        logging.info(f"Successfully answered {total_questions} questions")

        # Submit the test after answering all questions
        if not self.submit_test():
            logging.error("Failed to submit the test after answering all questions")
            return False

        # Handle popup submit
        if not self.handle_popup_submit():
            logging.error("Failed to handle popup submit")
            return False

        return True

    def submit_test(self):
        max_attempts = 3
        submit_locators = [
            (AppiumBy.XPATH, "//android.view.View[@content-desc='Submit' and @bounds='[18,1408][702,1462]']"),
            (AppiumBy.XPATH, "//android.view.View[@content-desc='Submit' and @bounds='[560,93][683,147]']"),
            (AppiumBy.XPATH, "//android.view.View[@content-desc='Submit']")
        ]
    
        for attempt in range(max_attempts):
            for locator in submit_locators:
                try:
                    submit_button = wait_for_element(self.driver, locator, timeout=5)
                    if tap_element(self.driver, submit_button):
                        logging.info(f"Successfully clicked the Submit button (Attempt {attempt + 1})")
                        return True
                except Exception as e:
                    logging.warning(f"Failed to find or click Submit button with locator {locator}. Error: {str(e)}")
        
            if attempt < max_attempts - 1:
                logging.info(f"Retrying submit... (Attempt {attempt + 1})")
                time.sleep(2)
    
        logging.error("Failed to submit the test after multiple attempts")
        return False

    def handle_popup_submit(self):
        try:
            time.sleep(4)  # Wait for 4 seconds as requested
            popup_submit_button = wait_for_element(self.driver, self.POPUP_SUBMIT_BUTTON_LOCATOR, timeout=20)
            if tap_element(self.driver, popup_submit_button):
                logging.info("Successfully clicked the Popup Submit button")
                return True
            else:
                logging.error("Failed to click the Popup Submit button")
                return False
        except Exception as e:
            logging.error(f"Error clicking Popup Submit button: {str(e)}")
            return False

    def click_done_button(self):
        try:
            time.sleep(3)  # Wait for 3 seconds as requested
            done_button = wait_for_element(self.driver, self.DONE_BUTTON_LOCATOR, timeout=20)
            if tap_element(self.driver, done_button):
                logging.info("Successfully clicked the Done button")
                return True
            else:
                logging.error("Failed to click the Done button")
                return False
        except Exception as e:
            logging.error(f"Error clicking Done button: {str(e)}")
            return False

    def recover_from_error(self):
        logging.info("Attempting to recover from error...")
        try:
            # Try to go back to the previous screen
            self.driver.back()
            time.sleep(2)
            
            # Check if we're back on the test screen
            if self.wait_for_element(self.driver, self.ANSWER_OPTION_A_LOCATOR, timeout=10):
                logging.info("Successfully recovered. Back on the test screen.")
                return True
            else:
                logging.error("Failed to recover. Not on the test screen.")
                return False
        except Exception as e:
            logging.error(f"Error during recovery attempt: {str(e)}")
            return False

