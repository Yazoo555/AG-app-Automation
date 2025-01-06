import logging
import time
from utils.helpers import wait_for_element, wait_for_element_to_be_clickable, tap_element
from pages.base_page import BasePage
from config.config import OTP

class OTPPage(BasePage):
    def enter_otp(self):
        try:
            otp_input = wait_for_element(self.driver, self.OTP_INPUT_LOCATOR)
            if not tap_element(self.driver, otp_input):
                raise Exception("Failed to tap OTP input field")
            time.sleep(1)
            otp_input.clear()
            
            for digit in OTP:
                otp_input.send_keys(digit)
                time.sleep(0.5)
            
            logging.info(f"OTP '{OTP}' input successful")

            confirm_button = wait_for_element_to_be_clickable(self.driver, self.CONFIRM_OTP_BUTTON_LOCATOR, timeout=15)
            if not tap_element(self.driver, confirm_button):
                raise Exception("Failed to tap Confirm Now button")
            logging.info("Confirm Now button tapped")
            return True
        except Exception as e:
            logging.error(f"OTP entry failed: {str(e)}")
            return False

    def is_on_otp_screen(self):
        from utils.helpers import check_element_exists
        return check_element_exists(self.driver, self.OTP_INPUT_LOCATOR, timeout=5)

