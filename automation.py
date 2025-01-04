import logging
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# Configuration
DEVICE_NAME = "112203741T003444"
APP_PATH = "/home/yaj/Documents/ag-flutter/build/app/outputs/apk/prod/debug/app-prod-debug.apk"
PHONE_NUMBER = "9843661500"

SCROLL_DOWN_START = (265, 1220)
SCROLL_DOWN_END = (270, 405)
SCROLL_UP_START = (375, 477)
SCROLL_UP_END = (375, 1220)
SCROLL_DOWN_COUNT = 7
SCROLL_UP_COUNT = 2
ITERATION_COUNT = 6
MAX_LIKES = 10
MAX_RETRIES = 3

WAIT_TIMEOUT = 10
POPUP_TIMEOUT = 5
LIKE_BUTTON_TIMEOUT = 3

PHONE_INPUT_LOCATOR = (AppiumBy.XPATH, "//android.widget.EditText[@bounds='[37,588][683,692]']")
PROCEED_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Proceed' and @bounds='[37,728][683,800]']")
POPUP_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@bounds='[80,411][640,1185]']")
LIKE_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Like' and @bounds='[140,1107][257,1159]']")

POPUP_CLOSE_COORDS = (615, 405)

# Utility functions
def wait_for_element(driver, locator, timeout=WAIT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )

def click_element(driver, locator, timeout=WAIT_TIMEOUT):
    for _ in range(MAX_RETRIES):
        try:
            element = wait_for_element(driver, locator, timeout)
            element.click()
            return True
        except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
            logging.warning(f"Failed to click element: {e}. Retrying...")
    logging.error(f"Failed to click element after {MAX_RETRIES} attempts")
    return False

def perform_touch_action(driver, start_coords, end_coords):
    for _ in range(MAX_RETRIES):
        try:
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(*start_coords)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(*end_coords)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            return True
        except WebDriverException as e:
            logging.warning(f"Failed to perform touch action: {e}. Retrying...")
    logging.error(f"Failed to perform touch action after {MAX_RETRIES} attempts")
    return False

def check_element_exists(driver, locator, timeout=WAIT_TIMEOUT):
    try:
        wait_for_element(driver, locator, timeout)
        return True
    except (TimeoutException, NoSuchElementException):
        return False

# Main automation functions
def setup_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = DEVICE_NAME
    options.app_wait_activity = "com.agnepal.ambitionguru"
    options.app = APP_PATH
    options.no_reset = True
    options.automation_name = "UiAutomator2"
    options.app_wait_duration = 30000
    options.ensure_webviews_have_pages = True
    options.native_web_screenshot = True
    options.new_command_timeout = 3600
    options.connect_hardware_keyboard = True
    
    return webdriver.Remote("http://127.0.0.1:4723", options=options)

def login(driver):
    try:
        phone_input = wait_for_element(driver, PHONE_INPUT_LOCATOR)
        phone_input.send_keys(PHONE_NUMBER)
        logging.info("Phone number input successful")

        if click_element(driver, PROCEED_BUTTON_LOCATOR):
            logging.info("Proceed button clicked")
        else:
            raise Exception("Failed to click Proceed button")
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        raise

def handle_popup(driver):
    try:
        if check_element_exists(driver, POPUP_LOCATOR, POPUP_TIMEOUT):
            logging.info("Pop-up found")
            if perform_touch_action(driver, POPUP_CLOSE_COORDS, POPUP_CLOSE_COORDS):
                logging.info("Pop-up closed")
            else:
                logging.warning("Failed to close pop-up")
        else:
            logging.info("No pop-up found")
    except Exception as e:
        logging.error(f"Error handling popup: {str(e)}")

def perform_like_action(driver):
    if check_element_exists(driver, LIKE_BUTTON_LOCATOR, LIKE_BUTTON_TIMEOUT):
        if click_element(driver, LIKE_BUTTON_LOCATOR):
            logging.info("Like action performed successfully")
            return True
        else:
            logging.warning("Failed to perform like action")
    return False

def perform_scroll_and_like(driver):
    likes_performed = 0
    for iteration in range(ITERATION_COUNT):
        logging.info(f"Starting iteration {iteration + 1}")
        
        for scroll in range(SCROLL_DOWN_COUNT):
            if perform_touch_action(driver, SCROLL_DOWN_START, SCROLL_DOWN_END):
                logging.info(f"Scroll down {scroll + 1} completed")
            else:
                logging.warning(f"Failed to perform scroll down {scroll + 1}")
            time.sleep(0.5)
            
            if likes_performed < MAX_LIKES:
                if perform_like_action(driver):
                    likes_performed += 1
                    logging.info(f"Like performed. Total likes: {likes_performed}")
            
            if likes_performed >= MAX_LIKES:
                logging.info(f"Maximum number of likes ({MAX_LIKES}) reached")
                return
        
        for scroll in range(SCROLL_UP_COUNT):
            if perform_touch_action(driver, SCROLL_UP_START, SCROLL_UP_END):
                logging.info(f"Scroll up {scroll + 1} completed")
            else:
                logging.warning(f"Failed to perform scroll up {scroll + 1}")
            time.sleep(0.5)
        
        logging.info(f"Iteration {iteration + 1} completed")

def run_automation():
    driver = None
    try:
        driver = setup_driver()
        login(driver)
        handle_popup(driver)
        time.sleep(5)  # Wait for home page to load
        perform_scroll_and_like(driver)
        logging.info("Automation completed successfully")
    except Exception as e:
        logging.error(f"An error occurred during automation: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run_automation()