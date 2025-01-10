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
                time.sleep(2)
        
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
                time.sleep(2)
        
        logging.error(f"Failed to scroll up after {max_retries} attempts")
        return False

    def wait_for_next_question(self, timeout=20): # Updated to use LONG_WAIT_TIMEOUT
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

    def perform_additional_actions(self): # Updated to use LONG_WAIT_TIMEOUT and MAX_RETRIES
        actions = [
            ("Answer Later", "Answer Later"),
            ("Report", "Report"),
            ("Answer option is incorrect", "Answer option is incorrect"),
            ("Submit", "Submit"),
            ("Save", "Save")
        ]

        max_retries = 3 # Updated to use MAX_RETRIES
        for accessibility_id, action_name in actions:
            for attempt in range(max_retries):
                try:
                    # Wait for the element to be clickable
                    element = WebDriverWait(self.driver, 20).until( # Updated to use LONG_WAIT_TIMEOUT
                        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, accessibility_id))
                    )
                    element.click()
                    logging.info(f"Successfully clicked {action_name}")
                    
                    # Verify the action was performed
                    if action_name == "Report":
                        # Wait for the popup to appear
                        WebDriverWait(self.driver, 20).until( # Updated to use LONG_WAIT_TIMEOUT
                            EC.presence_of_element_located((AppiumBy.XPATH, "//android.view.View[@bounds='[80,407][640,1189]']"))
                        )
                    elif action_name == "Submit":
                        # Wait for the popup to disappear
                        WebDriverWait(self.driver, 20).until( # Updated to use LONG_WAIT_TIMEOUT
                            EC.invisibility_of_element_located((AppiumBy.XPATH, "//android.view.View[@bounds='[80,407][640,1189]']"))
                        )
            
                    time.sleep(2)  # Wait for 2 seconds between actions
                    break  # If successful, break the retry loop
                except Exception as e:
                    if attempt == max_retries - 1:  # If this was the last attempt
                        logging.error(f"Failed to perform action {action_name} after {max_retries} attempts: {str(e)}")
                        return False
                    else:
                        logging.warning(f"Failed to perform action {action_name}. Retrying... (Attempt {attempt + 1} of {max_retries})")
                        time.sleep(2)  # Wait before retrying

        return True

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

            # Perform additional actions for the last 3 questions of the first 10
            if 7 <= i < 10:
                logging.info(f"Waiting 1 second before performing additional actions for question {i+1}")
                time.sleep(1)  # Wait for 1 second after attempting the question
                max_retries = 3
                for attempt in range(max_retries):
                    if self.perform_additional_actions():
                        break
                    elif attempt == max_retries - 1:
                        logging.error(f"Failed to perform additional actions for question {i+1} after {max_retries} attempts")
                        return False
                    else:
                        logging.warning(f"Failed to perform additional actions for question {i+1}. Retrying... (Attempt {attempt + 1} of {max_retries})")
                        time.sleep(2)

            time.sleep(2)

        logging.info(f"Successfully answered {total_questions} questions")

        if not self.scroll_to_bottom():
            logging.warning("Failed to scroll to the bottom of the page. Attempting to submit anyway.")

        # Perform pre-submit actions
        if not self.perform_pre_submit_actions():
            logging.error("Failed to perform pre-submit actions")
            return False

        if not self.submit_test():
            logging.error("Failed to submit the test after answering all questions")
            return False

        if not self.handle_popup_submit():
            logging.error("Failed to handle popup submit")
            return False

        return True

    def submit_test(self): # Updated to use LONG_WAIT_TIMEOUT and MAX_RETRIES
        max_attempts = 3 # Updated to use MAX_RETRIES
        submit_locators = [
            (AppiumBy.XPATH, "//android.view.View[@content-desc='Submit' and @bounds='[18,1408][702,1462]']"),
            (AppiumBy.XPATH, "//android.view.View[@content-desc='Submit' and @bounds='[560,93][683,147]']"),
            (AppiumBy.XPATH, "//android.view.View[@content-desc='Submit']")
        ]

        for attempt in range(max_attempts):
            for index, locator in enumerate(submit_locators):
                try:
                    submit_button = wait_for_element(self.driver, locator, timeout=20) # Updated to use LONG_WAIT_TIMEOUT
                    if tap_element(self.driver, submit_button):
                        logging.info(f"Successfully clicked the Submit button (Attempt {attempt + 1}, Locator {index + 1})")
                        return True
                except Exception as e:
                    logging.warning(f"Failed to find or click Submit button with locator {index + 1}. Error: {str(e)}")
        
            if attempt < max_attempts - 1:
                logging.info(f"Retrying submit... (Attempt {attempt + 1})")
                time.sleep(2)

        logging.error("Failed to submit the test after multiple attempts")
        return False

    def handle_popup_submit(self): # Updated to use LONG_WAIT_TIMEOUT
        try:
            time.sleep(4)
            popup_submit_button = wait_for_element(self.driver, self.POPUP_SUBMIT_BUTTON_LOCATOR, timeout=20) # Updated to use LONG_WAIT_TIMEOUT
            if tap_element(self.driver, popup_submit_button):
                logging.info("Successfully clicked the Popup Submit button")
                return True
            else:
                logging.error("Failed to click the Popup Submit button")
                return False
        except Exception as e:
            logging.error(f"Error clicking Popup Submit button: {str(e)}")
            return False

    def click_done_button(self): # Updated to use LONG_WAIT_TIMEOUT
        try:
            time.sleep(3)
            done_button = wait_for_element(self.driver, self.DONE_BUTTON_LOCATOR, timeout=20) # Updated to use LONG_WAIT_TIMEOUT
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
            self.driver.back()
            time.sleep(2)
            
            if self.wait_for_element(self.driver, self.ANSWER_OPTION_A_LOCATOR, timeout=10):
                logging.info("Successfully recovered. Back on the test screen.")
                return True
            else:
                logging.error("Failed to recover. Not on the test screen.")
                return False
        except Exception as e:
            logging.error(f"Error during recovery attempt: {str(e)}")
            return False

    def scroll_to_bottom(self):
        try:
            screen_size = self.driver.get_window_size()
            start_x = screen_size['width'] * 0.5
            start_y = screen_size['height'] * 0.2
            end_y = screen_size['height'] * 0.8

            TouchAction(self.driver).press(x=start_x, y=start_y).move_to(x=start_x, y=end_y).release().perform()
            logging.info("Successfully scrolled to the bottom of the page")
            return True
        except Exception as e:
            logging.error(f"Error scrolling to the bottom of the page: {str(e)}")
            return False

    def perform_pre_submit_actions(self):
        try:
            actions = [
                (AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button[2]", "Filter button"),
                (AppiumBy.ACCESSIBILITY_ID, "All", "All filter"),
                (AppiumBy.ACCESSIBILITY_ID, "Not Attempted", "Not Attempted filter"),
                (AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button[2]", "Filter button"),
                (AppiumBy.ACCESSIBILITY_ID, "Not Attempted", "Not Attempted filter"),
                (AppiumBy.ACCESSIBILITY_ID, "Attempted", "Attempted filter"),
                (AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button[1]", "Close filter"),
                (AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button[2]", "Settings button"),
                (AppiumBy.ACCESSIBILITY_ID, "Serif\nAa", "Serif font option"),
                (AppiumBy.ACCESSIBILITY_ID, "Scrim", "Scrim option")
            ]

            for locator_type, locator_value, action_name in actions:
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((locator_type, locator_value))
                    )
                    element.click()
                    logging.info(f"Successfully clicked {action_name}")
                    time.sleep(1)  # Short pause between actions
                except Exception as e:
                    logging.error(f"Failed to perform action {action_name}: {str(e)}")
                    return False

            logging.info("Successfully performed all pre-submit actions")
            return True
        except Exception as e:
            logging.error(f"Error in perform_pre_submit_actions: {str(e)}")
            return False

