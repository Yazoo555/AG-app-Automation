import logging
import time
from utils.helpers import check_element_exists, wait_for_element, tap_element, perform_touch_action
from pages.base_page import BasePage
from config.config import (
    SCROLL_DOWN_START, SCROLL_DOWN_END, SCROLL_UP_START, SCROLL_UP_END,
    SCROLL_DOWN_COUNT, SCROLL_UP_COUNT, ITERATION_COUNT, MAX_LIKES,
    POPUP_TIMEOUT, LIKE_BUTTON_TIMEOUT, POPUP_CLOSE_COORDS
)

class HomePage(BasePage):
    def is_on_home_screen(self):
        return check_element_exists(self.driver, self.PROFILE_ICON_LOCATOR, timeout=5)

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

    def perform_like_action(self):
        if check_element_exists(self.driver, self.LIKE_BUTTON_LOCATOR, LIKE_BUTTON_TIMEOUT):
            like_button = wait_for_element(self.driver, self.LIKE_BUTTON_LOCATOR)
            if tap_element(self.driver, like_button):
                logging.info("Like action performed successfully")
                return True
            else:
                logging.warning("Failed to perform like action")
        return False

    def perform_scroll_and_like(self):
        likes_performed = 0
        for iteration in range(ITERATION_COUNT):
            logging.info(f"Starting iteration {iteration + 1}")
            
            for scroll in range(SCROLL_DOWN_COUNT):
                if perform_touch_action(self.driver, SCROLL_DOWN_START, SCROLL_DOWN_END):
                    logging.info(f"Scroll down {scroll + 1} completed")
                else:
                    logging.warning(f"Failed to perform scroll down {scroll + 1}")
                time.sleep(0.5)
                
                if likes_performed < MAX_LIKES:
                    if self.perform_like_action():
                        likes_performed += 1
                        logging.info(f"Like performed. Total likes: {likes_performed}")
                
                if likes_performed >= MAX_LIKES:
                    logging.info(f"Maximum number of likes ({MAX_LIKES}) reached")
                    return
            
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

