from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.config import DEVICE_NAME, APP_PATH

def setup_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = DEVICE_NAME
    options.app = APP_PATH
    options.app_package = "com.agnepal.ambitionguru"
    options.app_activity = "com.agnepal.ambitionguru.MainActivity"  # Update this if different
    options.no_reset = True
    options.automation_name = "UiAutomator2"
    options.app_wait_duration = 60000  # Increased from 30000 to 60000
    options.ensure_webviews_have_pages = True
    options.native_web_screenshot = True
    options.new_command_timeout = 7200  # Increased from 3600 to 7200
    options.connect_hardware_keyboard = True
    
    return webdriver.Remote("http://localhost:4723", options=options)

