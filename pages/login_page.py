import logging
import time
from utils.helpers import wait_for_element, tap_element
from pages.base_page import BasePage
from config.config import PHONE_NUMBER

class LoginPage(BasePage):
    def login(self):
        try:
            phone_input = wait_for_element(self.driver, self.PHONE_INPUT_LOCATOR)
            if not tap_element(self.driver, phone_input):
                raise Exception("Failed to tap phone input field")
            time.sleep(1)
            phone_input.clear()
            phone_input.send_keys(PHONE_NUMBER)
            logging.info("Phone number input successful")

            proceed_button = wait_for_element(self.driver, self.PROCEED_BUTTON_LOCATOR)
            if not tap_element(self.driver, proceed_button):
                raise Exception("Failed to tap Proceed button")
            logging.info("Proceed button tapped")
            return True
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def is_on_login_screen(self):
        from utils.helpers import check_element_exists
        return check_element_exists(self.driver, self.PHONE_INPUT_LOCATOR, timeout=5)
