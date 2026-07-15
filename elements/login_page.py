"""
Login page element locators
"""

class LoginPageElements:
    #URL
    CX_URL = "https://cx.locobuzz.com/login"
    PREPROD_URL="https://preprodcx.locobuzz.com/login"
    UAT_URL = "https://locobuzzng-uat-aws.locobuzz.com/login"

    #Input Fields
    USERNAME_INPUT = "//input[@formcontrolname='username']"

    CONTINUE_BUTTON = "//button[contains(., 'Continue') and .//mat-icon[contains(text(),'lock')]]"

    PASSWORD_INPUT = '//input[@type="password"]'
    
    LOGIN_BUTTON = "//button[contains(., 'Login') and .//mat-icon[contains(text(),'lock')]]"

    #Select All Brands and Submit
    SELECT_ALL_BRANDS = "//span[text()='Select All']"
    SELECT_TWITTER_AUTO = "//span[text()='twitter auto']"
    SUBMIT_BUTTON = "//span[text()=' Submit ']"

    #Logout Elements
    LOGOUT_BUTTON = "//span[text()='Logout']"
    CONFIRM_LOGOUT_BUTTON = "//span[text()='Logout']"
    
    #Login Fields (alternative naming)
    USERNAME_FIELD = "//input[@formcontrolname='username']"
    PASSWORD_FIELD = '//input[@type="password"]'
    CONTINUE_BUTTON_ALT = "//button[contains(., 'Continue')]"
    LOGIN_BUTTON_ALT = "//button[contains(., 'Login')]"
    BilalSHaikh = "//button[text()='Bilal']"
    sample = "//span[text()='sample']"
    shivam_sample = "//span[text()='shivam b']"

