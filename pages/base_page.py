from appium.webdriver.common.appiumby import AppiumBy

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    PHONE_INPUT_LOCATOR = (AppiumBy.XPATH, "//android.widget.EditText[@bounds='[37,588][683,692]']")
    PROCEED_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Proceed' and @bounds='[37,728][683,800]']")
    OTP_INPUT_LOCATOR = (AppiumBy.XPATH, "//android.widget.EditText[@bounds='[37,713][683,825]']")
    CONFIRM_OTP_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Confirm Now' and @bounds='[37,950][683,1022]']")
    POPUP_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@bounds='[80,411][640,1185]']")
    LIKE_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Like' and @bounds='[140,1107][257,1159]']")
    PROFILE_ICON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Profile' and @bounds='[18,99][102,173]']")

