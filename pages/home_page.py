import logging
import time
from utils.helpers import check_element_exists, perform_touch_action, tap_element, wait_for_element
from pages.base_page import BasePage
from config.config import (
    SCROLL_DOWN_START, SCROLL_DOWN_END, SCROLL_UP_START, SCROLL_UP_END,
    SCROLL_DOWN_COUNT, SCROLL_UP_COUNT, ITERATION_COUNT,
    POPUP_TIMEOUT, POPUP_CLOSE_COORDS
)

class HomePage(BasePage):
    def is_on_home_screen(self):
        return check_element_exists(self.driver, self.HOME_TAB_LOCATOR, timeout=5)

    def handle_popup(self):
        try:
            if check_element_exists(self.driver, self.POPUP_LOCATOR, POPUP_TIMEOUT):
                logging.info("Pop-up found")
                if perform_touch_action(self.driver, POPUP_CLOSE_COORDS, POPUP_CLOSE_COORDS):
                    logging.info("Pop-up closed")
                else:
                    logging.warning("Failed to close pop-up")
            else:
                logging.info("No pop-up found")
        except Exception as e:
            logging.error(f"Error handling popup: {str(e)}")

    def perform_scroll(self):
        for iteration in range(ITERATION_COUNT):
            logging.info(f"Starting iteration {iteration + 1}")
            
            for scroll in range(SCROLL_DOWN_COUNT):
                if perform_touch_action(self.driver, SCROLL_DOWN_START, SCROLL_DOWN_END):
                    logging.info(f"Scroll down {scroll + 1} completed")
                else:
                    logging.warning(f"Failed to perform scroll down {scroll + 1}")
                time.sleep(0.5)
            
            for scroll in range(SCROLL_UP_COUNT):
                if perform_touch_action(self.driver, SCROLL_UP_START, SCROLL_UP_END):
                    logging.info(f"Scroll up {scroll + 1} completed")
                else:
                    logging.warning(f"Failed to perform scroll up {scroll + 1}")
                time.sleep(0.5)
            
            logging.info(f"Iteration {iteration + 1} completed")

    def handle_popup_and_check_home(self):
        max_attempts = 3
        for attempt in range(max_attempts):
            self.handle_popup()
            if self.is_on_home_screen():
                logging.info("Successfully reached home screen after handling popup.")
                return True
            elif attempt < max_attempts - 1:
                logging.warning(f"Home screen not detected after popup. Attempt {attempt + 1} of {max_attempts}. Retrying...")
                time.sleep(5)
        logging.error("Failed to reach home screen after handling popup and maximum attempts")
        return False

    def navigate_to_test_tab(self):
        try:
            test_tab = wait_for_element(self.driver, self.TEST_TAB_LOCATOR)
            if tap_element(self.driver, test_tab):
                logging.info("Successfully navigated to Test tab")
                return True
            else:
                logging.error("Failed to tap Test tab")
                return False
        except Exception as e:
            logging.error(f"Error navigating to Test tab: {str(e)}")
            return False

    def navigate_to_chapterwise_test(self):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                chapterwise_test = wait_for_element(self.driver, self.CHAPTERWISE_TEST_LOCATOR, timeout=10)
                if tap_element(self.driver, chapterwise_test):
                    logging.info("Successfully navigated to Chapterwise test section")
                    return True
                else:
                    logging.warning(f"Failed to tap Chapterwise test. Attempt {attempt + 1} of {max_attempts}")
            except Exception as e:
                logging.warning(f"Error navigating to Chapterwise test section: {str(e)}. Attempt {attempt + 1} of {max_attempts}")
            
            if attempt < max_attempts - 1:
                logging.info("Attempting to refresh the Test tab")
                self.refresh_test_tab()
                time.sleep(2)
    
        logging.error("Failed to navigate to Chapterwise test section after multiple attempts")
        return False

    def is_on_test_tab_screen(self):
        return check_element_exists(self.driver, self.TEST_TAB_LOCATOR, timeout=5)

    def navigate_to_quick_exam(self):
        try:
            quick_exam = wait_for_element(self.driver, self.QUICK_EXAM_LOCATOR)
            if tap_element(self.driver, quick_exam):
                logging.info("Successfully navigated to Quick exam type")
                return True
            else:
                logging.error("Failed to tap Quick exam type")
                return False
        except Exception as e:
            logging.error(f"Error navigating to Quick exam type: {str(e)}")
            return False

    def refresh_test_tab(self):
        try:
            # Attempt to tap on another tab (e.g., Home tab) and then back to Test tab
            home_tab = wait_for_element(self.driver, self.HOME_TAB_LOCATOR, timeout=5)
            if tap_element(self.driver, home_tab):
                logging.info("Tapped Home tab for refreshing")
                time.sleep(1)
                test_tab = wait_for_element(self.driver, self.TEST_TAB_LOCATOR, timeout=5)
                if tap_element(self.driver, test_tab):
                    logging.info("Tapped Test tab again after refreshing")
                    return True
        except Exception as e:
            logging.error(f"Error refreshing Test tab: {str(e)}")
        return False

