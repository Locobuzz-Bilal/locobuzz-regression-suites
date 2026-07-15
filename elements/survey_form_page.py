class SurveyFormElements:
    """XPath elements for Survey Form functionality"""
    
    # Navigation elements
    PROFILE_MENU_BUTTON = "//li[contains(@class, 'listitem')]//a"
    ACCOUNT_SETTINGS_MENU = "//menuitem[@role='menuitem' or contains(., 'Account Settings')]"
    
    # Search and Survey Form
    SEARCH_INPUT = "//input[@placeholder='Search' or @name='Search']"
    SURVEY_FORM_LINK = "//a[text()='Survey Form' or contains(., 'Survey Form')]"
    
    # Brand Selection
    BRAND_DROPDOWN = "//mat-select[contains(@aria-label, 'Select Brand') or contains(@placeholder, 'Select Brand')]//div[contains(@class, 'mat-select-arrow')]"
    BRAND_OPTION_JUWS = "//mat-option[@id='mat-option-6']//span[contains(text(), 'Juws')]"
    
    # Form Creation
    CREATE_NEW_FORM_BUTTON = "(//button[contains(., 'Create New Form')])[1]"
    FIRST_IMAGE = "//img[@src='https://s3.amazonaws.com/locobuzz.socialimages/SurveyImage/reliancejiodb/74a0e691-c84d-4baa-892a-6729dd482688.png']"
    
    # Form Title
    UNTITLED_FORM_TEXT = "//app-text//div[@contenteditable]"
    FORM_TITLE_INPUT = "//div[contains(text(), 'Untitled form')]"
    
    # Drop Zone
    FORM_DROP_ZONE = "(//div[contains(@class,'form-container')]//div[@dnddropzone])[2]"
    
    # Rating Elements
    RATING_TEXT = "//text()[contains(., 'Rating')]/ancestor::*[self::div or self::span or self::button][1]"
    RATING_LABEL_INPUT = "(//input[contains(@class,'form-builder__field--input')])[2]"
    RATING_DROPDOWN = "//select[contains(@class,'form-builder__field--input')]"
    
    # Question Elements
    RATING_QUESTION_TEXT = "//text()[contains(., 'How would you like to rate')]/ancestor::*[1]"
    NPS_TEXT = "//text()[contains(., 'NPS')]/ancestor::*[self::div or self::span or self::button][1]"
    
    # Action Buttons
    PREVIEW_BUTTON = "//button[contains(., 'Preview')]"
    CLOSE_BUTTON = "//mat-icon[text()='close']"
    UPDATE_FORM_BUTTON = "//button[contains(., 'Update Form')]"
    COPY_BUTTON = "//button[contains(., 'Copy')]"
    SAVE_BUTTON = "//button[contains(., 'Save')]"
    
    # Edit and Delete Menu
    MORE_MENU_BUTTON = "//button[contains(., 'more_vert')]"
    EDIT_MENU_ITEM = "//mat-icon[text()='edit']"
    DELETE_MENU_ITEM = "//mat-icon[text()='delete']"
    DELETE_CONFIRMATION_YES = "//button[contains(., 'Yes')]"
    
    # Form Fields
    TESTING_1_FIELD = "//span[text()='testing 1']"
    TESTING_2_FIELD = "//span[text()='testing 2']"
    
    # Conditional Logic
    SET_CONDITIONAL_LOGIC = "//span[normalize-space()='Set conditional logic']"
    AND_TOGGLE_BUTTON = "(//span[text()='AND'])[1]"
    OR_TOGGLE_BUTTON = "(//span[text()='OR'])[2]"
    ADD_ATTRIBUTE_BUTTON = "//*[text()='+ Add Attribute']"
    ADD_GROUP_BUTTON = "//button[contains(., '+ Add Group')]"
    
    # Conditional Logic Dropdowns
    ATTRIBUTE_DROPDOWN = "//mat-label[normalize-space()='Attribute']/ancestor::mat-form-field//mat-select"
    OPERATOR_DROPDOWN = "//mat-label[normalize-space()='Operator']/ancestor::mat-form-field//mat-select"
    VALUE_INPUT = "//mat-label[normalize-space()='Value']/ancestor::mat-form-field//input"
    
    # Specific Conditional Logic Elements
    ATTRIBUTE_DROPDOWN_5 = "//mat-select[@id='mat-select-5']"
    OPERATOR_DROPDOWN_6 = "//mat-select[@id='mat-select-6']"
    ATTRIBUTE_DROPDOWN_7 = "//mat-select[@id='mat-select-7']"
    OPERATOR_DROPDOWN_8 = "//mat-select[@id='mat-select-8']"
    VALUE_INPUT_7 = "//input[@id='mat-input-7']"
    
    # Conditional Logic Options
    TESTING_3_OPTION = "//mat-option//span[contains(text(), 'testing 3')]"
    TESTING_2_OPTION = "//mat-option//span[contains(text(), 'testing 2')]"
    GREATER_THAN_OPTION = "//*[text()='greater than']"
    IS_EMPTY_OPTION = "//*[text()='is empty']"
    NOT_EQUAL_OPTION = "//*[text()='does not equal']"
    
    # Delete Icons
    DELETE_OUTLINE_ICON = "(//*[text()='delete_outline'])[2]"
    DELETE_ICON = "//*[text()='delete']"
    
    # Success Messages
    CONDITION_LOGIC_SAVED_MESSAGE = "//span[text()='Condition logic saved successfully.']"
    FORM_UPDATED_MESSAGE = "//*[text()='Form updated successfully.']"
    FORM_DELETED_MESSAGE = "//*[text()='Form deleted successfully.']"
