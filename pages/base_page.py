from appium.webdriver.common.appiumby import AppiumBy

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    PHONE_INPUT_LOCATOR = (AppiumBy.XPATH, "//android.widget.EditText[@bounds='[37,588][683,692]']")
    PROCEED_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Proceed' and @bounds='[37,728][683,800]']")
    OTP_INPUT_LOCATOR = (AppiumBy.XPATH, "//android.widget.EditText[@bounds='[37,713][683,825]']")
    CONFIRM_OTP_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Confirm Now' and @bounds='[37,950][683,1022]']")
    POPUP_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@bounds='[80,411][640,1185]']")
    HOME_TAB_LOCATOR = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Home\nTab 1 of 6' and @bounds='[0,1405][120,1515]']")
    TEST_TAB_LOCATOR = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Test\nTab 3 of 6' and @bounds='[240,1405][360,1515]']")
    CHAPTERWISE_TEST_LOCATOR = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Chapterwise' and @bounds='[36,192][180,318]']")
    CHECKBOX_1_LOCATOR = (AppiumBy.XPATH, "//android.widget.CheckBox[@bounds='[28,217][105,275]']")
    CHECKBOX_2_LOCATOR = (AppiumBy.XPATH, "//android.widget.CheckBox[@bounds='[28,321][105,379]']")
    CHECKBOX_3_LOCATOR = (AppiumBy.XPATH, "//android.widget.CheckBox[@bounds='[28,425][105,483]']")
    CHECKBOX_4_LOCATOR = (AppiumBy.XPATH, "//android.widget.CheckBox[@bounds='[28,529][105,587]']")
    NUMBER_INPUT_LOCATOR = (AppiumBy.XPATH, "//android.widget.EditText[@bounds='[37,1308][683,1412]']")
    START_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Start' and @bounds='[406,1426][683,1498]']")
    ANSWER_OPTION_A_LOCATOR = (AppiumBy.XPATH, "//android.view.View[starts-with(@content-desc, 'A.')]")
    ANSWER_OPTION_B_LOCATOR = (AppiumBy.XPATH, "//android.view.View[starts-with(@content-desc, 'B.')]")
    ANSWER_OPTION_C_LOCATOR = (AppiumBy.XPATH, "//android.view.View[starts-with(@content-desc, 'C.')]")
    SUBMIT_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Submit' and @bounds='[18,1410][702,1464]']")
    POPUP_SUBMIT_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Submit' and @bounds='[369,1050][545,1121]']")
    DONE_BUTTON_LOCATOR = (AppiumBy.XPATH, "//android.view.View[@content-desc='Done' and @bounds='[576,109][687,163]']")
    QUICK_EXAM_LOCATOR = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Quick' and @bounds='[217,192][285,318]']")

