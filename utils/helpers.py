import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from config.config import WAIT_TIMEOUT, MAX_RETRIES

def wait_for_element(driver, locator, timeout=WAIT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )

def wait_for_element_to_be_clickable(driver, locator, timeout=WAIT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )

def click_element(driver, locator, timeout=WAIT_TIMEOUT):
    for _ in range(MAX_RETRIES):
        try:
            element = wait_for_element_to_be_clickable(driver, locator, timeout)
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

def tap_element(driver, element):
    try:
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to(element)
        actions.w3c_actions.pointer_action.click()
        actions.w3c_actions.perform()
        return True
    except Exception as e:
        logging.error(f"Failed to tap element: {e}")
        return False

def check_element_exists(driver, locator, timeout=WAIT_TIMEOUT):
    try:
        wait_for_element(driver, locator, timeout)
        return True
    except (TimeoutException, NoSuchElementException):
        return False

