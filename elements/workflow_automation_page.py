"""
Workflow Automation page elements
"""

class WorkflowAutomationPageElements:
    # Navigation
    ACCOUNT_SETTINGS_MENU = "//div[contains(@class, 'sidebar__foot')]//a[contains(@class, 'sidebar__profile--link')]"
    ACCOUNT_SETTINGS_OPTION = "//span[text()='Account Settings']"
    SEARCH_INPUT = "//input[@placeholder='Search']"
    WORKFLOW_LINK = "//span[text()='WorkFlow Automation']"
    
    # Brand selection
    BRAND_DROPDOWN = "//mat-label[text()='Select Brand']/ancestor::mat-form-field//mat-select"
    BRAND_JUWS_OPTION = "//span[contains(text(),'Juws')]"

    # Feature toggle
    FEATURE_TOGGLE = "//div[contains(@class, 'rounded-toggle-switch')]//label[@for='rounded-toggle-switch']"

    # Create workflow
    CREATE_NEW_BUTTON = "//span[contains(text(),'Create New')]"
    WORKFLOW_NAME_INPUT = "//input[@placeholder='Enter workflow name']"
    
    # Triggers
    ADD_TRIGGER_BUTTON = "//p[contains(text(),'Add Trigger')]"
    NEW_TICKET_TRIGGER = "//p[contains(text(),'New Ticket')]"
    
    # Steps
    ADD_STEP_BUTTON = "//p[text()='Add Step']"
    
    # Canned Response
    CANNED_RESPONSE_BUTTON = "//p[contains(text(),'Canned Response')]"
    PERSONALIZE_BUTTON = "//span[text()='Personalize']"
    FIRST_NAME_OPTION = "//span[text()='First Name']"
    FULL_NAME_OPTION = "//span[text()='Full Name']"
    SCREEN_NAME_OPTION = "//span[text()='Screen Name']"
    MESSAGE_TEXTAREA = "//textarea[@placeholder='Write your message']"
    ADD_RESPONSE_BUTTON = "//span[contains(text(),'Add Response')]"
    ADD_ATTRIBUTES_BUTTON = "//span[text()='Add Attributes']"
    LOCATION_ATTRIBUTES = "//span[text()='Location Attributes']"
    LOCATION_NAME = "//span[text()='Location Name']"
    
    # Disposition
    DISPOSITION_DROPDOWN = "//mat-label[text()='Disposition Name']/ancestor::mat-form-field//mat-select"
    TICKET_SHOWN_OPTION = "//span[text()='Ticket Shown']"
    ORDER_RELATED_OPTION = "//span[text()='Order Related']"
    CATEGORY_EDIT_BUTTON = "//mat-icon[text()='edit']"
    EMAIL_TEST_CHECKBOX = "//label[text()=' Email Test']"
    POSITIVE_RADIO = "//label[text()=' Positive']"
    NEGATIVE_RADIO = "//label[text()=' Negative']"
    NEUTRAL_RADIO = "//label[text()=' Neutral']"
    NOTE_INPUT = "//input[@placeholder='Enter note']"
    
    # Mark as Closed
    MARK_CLOSED_BUTTON = "//p[text()='Mark ticket as Closed']"
    
    # Send Alert
    SEND_ALERT_BUTTON = "//p[text()='Send Alert']"
    ALERT_SUBJECT_INPUT = "//input[@placeholder='Enter Subject']"
    TO_EMAIL_COMBO = "//input[@placeholder='New To Email......']"
    EMAIL_OPTION = "//mat-option//span[contains(text(),'juw@gmail.com')]"
    EDITOR_IFRAME = "//iframe[@title='Editor, editor1']"
    
    # Set Category
    SET_CATEGORY_BUTTON = "//p[text()='Set Category']"
    UPPER_CATEGORY_DROPDOWN = "//mat-label[text()='Select Upper Category']/ancestor::mat-form-field//mat-select"
    HELLO_SHAIWAZ_OPTION = "//span[text()='Hello Shaiwaz']"
    
    # Set Priority
    SET_PRIORITY_BUTTON = "//p[text()='Set Priority']"
    MEDIUM_PRIORITY_BUTTON = "//p[contains(text(),'Medium')]"
    
    # Assign To
    ASSIGN_TO_BUTTON = "//p[text()='Assign To']"
    USER_CHECKBOX = "(//input[@type='checkbox'])[6]"
    
    # Add Delay
    ADD_DELAY_BUTTON = "//p[text()='Add Delay']"
    DELAY_INPUT = "//input[@formcontrolname='timeValue']"
    
    # Add Paths
    ADD_PATHS_BUTTON = "//p[text()='Add Paths']"
    PATH_A_INPUT = "//input[@placeholder='Path A']"
    SELECT_ATTRIBUTE = "//mat-label[text()='Select Attribute']"
    CHANNEL_ATTRIBUTE = "//span[text()=' Channel ']"
    SHOULD_CONTAIN = "//span[text()='Should Contain']"
    SHOULD_NOT_CONTAIN = "//span[text()=' Should Not Contain ']"
    SELECT_CHANNEL = "//mat-label[text()='Select Channel']"
    TWITTER_CHECKBOX = "//span[text()='Twitter']/ancestor::mat-checkbox"
    DELETE_PATH_MENU = "//div[contains(@class,'workflow-path__sizefix')]//mat-icon[normalize-space()='more_vert']"
    DELETE_PATH_BUTTON = "//span[contains(text(),'Delete Path')]"
    YES_BUTTON = "//span[contains(text(),'Yes')]"
    
    # Settings
    SETTINGS_ICON = "//mat-icon[text()='settings']"
    ALWAYS_ACTIVE_RADIO = "//mat-radio-button[@value='Always Active']"
    SEND_DEFAULT_REPLY_RADIO = "//label[normalize-space()='Send default reply to a customer']"
    
    # Save buttons
    SAVE_BUTTON = "//p[text()='Save']"
    SAVE_WORKFLOW_BUTTON = "//p[contains(text(),'Save Workflow')]"