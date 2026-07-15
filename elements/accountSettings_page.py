class AccountSettingsPageElements:
    """XPath elements for Account Settings page and Canned Responses"""
    
    # Profile Menu
    PROFILE_MENU = "//img[@src='assets/images/agentimages/sample-image.svg']"

    # Account Settings
    ACCOUNT_SETTINGS = "//span[text()='Account Settings']"
    
    # Search field in Account Settings
    SEARCH_FIELD = "//input[@placeholder='Search']"
    
    # Canned Responses
    CANNED_RESPONSES_LINK = "//span[text()='Canned Responses']"
    
    # Brand Selection
    BRAND_DROPDOWN = "//div[contains(@class, 'mat-mdc-select-arrow-wrapper')]"
    JUWS_BRAND_OPTION = "//span[text()='Juws']"
    
    # Add Response
    ADD_RESPONSES_BUTTON = "//span[text()=' Add Responses ']"
    RESPONSE_NAME_FIELD = "//input[@placeholder='Response Name']"
    RESPONSE_PREVIEW = "//textarea[@mattextareaautosize and contains(@class,'textarea-featured__input')]"
    
    # Attachment
    ATTACHMENT_BUTTON = "//span[text()=' Attachment ']"
    FIRST_IMAGE = "//span[text()='appleLogo.png']"
    SECOND_IMAGE = "//span[text()='unnamed.jpg']"
    ATTACH_BUTTON = "//span[text()=' Attach ']"
    
    # Save
    SAVE_RESPONSE_BUTTON = "//span[text()=' Save Response ']"
    
    # Keyword Configuration Elements
    KEYWORDS_CONFIGURATION_LINK = "//a[contains(@href, 'keywords') or text()='Keywords Configuration']"
    ADD_KEYWORDS_BUTTON = "//button[contains(., 'Add Keywords/Social Profiles')]"
    KEYWORDS_GROUP_NAME_FIELD = "//input[@placeholder='Keywords Group Name' or contains(@formcontrolname, 'groupName')]"
    
    # Social Media Checkboxes
    TWITTER_CHECKBOX = "//div[@id='twitter']//input[@type='checkbox'] | //mat-checkbox[contains(.,'Twitter')]//input | //input[contains(@id,'twitter')] | //label[contains(.,'Twitter')]//input"
    INSTAGRAM_CHECKBOX = "//div[@id='facebook']//input[@type='checkbox'] | //mat-checkbox[contains(.,'Facebook')]//input | //input[contains(@id,'facebook')] | //label[contains(.,'Facebook')]//input"
    
    # Keywords Input
    INCLUDED_KEYWORDS_FIELD = "(//input[@placeholder='Add New Keyword'])[2]"
    
    # Advanced Query Builder
    ADVANCE_QUERY_BUILDER = "//span[text()='Advance Query Builder'] | //button[contains(., 'Advance Query Builder')]"
    
    # Twitter Section
    TWITTER_SECTION = "//div[@id='twitter'] | //div[contains(., 'Twitter')]"
    
    # Query Builder Elements
    AND_TOGGLE = "//mat-button-toggle-group//button[contains(., 'AND')]"
    OR_TOGGLE = "//mat-button-toggle-group//button[contains(., 'OR')]"
    NOT_TOGGLE = "//mat-button-toggle-group//button[contains(., 'NOT')]"
    
    # Attribute Dropdown
    ATTRIBUTE_DROPDOWN = "//label[.//mat-label[text()='Attribute']]/ancestor::div[contains(@class,'mat-mdc-form-field')]//mat-select"
    TWEET_OPTION = "//mat-option[contains(., 'Tweet')]"
    
    # Operator Dropdown
    OPERATOR_DROPDOWN = "//mat-select[@aria-labelledby=//label[.//mat-label[text()='Operator']]/@id]"
    SHOULD_CONTAIN_OPTION = "//mat-option[contains(., 'Should Contain')]"
    SHOULD_NOT_CONTAIN_OPTION = "//mat-option[contains(., 'Should Not Contain')]"
    
    # Keywords Input Fields
    ENTER_KEYWORDS_FIELD = "//input[@placeholder='Enter Keywords'] | //input[contains(@id, 'chip-list-input')]"
    
    # Add Group/Attribute Buttons
    ADD_GROUP_BUTTON = "//button[contains(., '+ Add Group')]"
    ADD_ATTRIBUTE_BUTTON = "//button[contains(., '+ Add Attribute')]"
    
    # Save and Confirmation
    SAVE_BUTTON = "//button[contains(., 'Save') and not(contains(., 'Response'))]"
    YES_BUTTON = "//button[contains(., 'Yes')]"
    SUCCESS_MESSAGE = "//*[contains(text(), 'Successfully Created')]"
    ERROR_MESSAGE = "//*[contains(text(), 'Negated clauses cannot be')]"
    
    # Search and Filter
    SEARCH_KEYWORDS_FIELD = "//input[@placeholder='Search by Group Name, Keyword' or contains(@placeholder, 'Search by')]"
    SEARCH_KEYWORDS_BUTTON = "//button[contains(., 'search')]"
    
    # Keywords List
    KEYWORDS_ROW = "//tr[contains(., 'testing')]"
    DELETE_KEYWORD_BUTTON = "//button[contains(@class, 'delete') or .//mat-icon[text()='delete']]"
    
    # Feedback / Survey Form Elements
    FEEDBACK_SURVEY_FORM_LINK = "//span[text()='Feedback / Survey Form']"
    
    # Toggle Button for Feedback Form
    FEEDBACK_TOGGLE = "//input[@id='rounded-toggle-switch'] | //label[@for='rounded-toggle-switch']//preceding-sibling::input | //input[@type='checkbox'][following-sibling::label[contains(@class, 'rounded-toggle-switch-label')]]"
    
    # Feedback Rating
    FEEDBACK_RATING_TEXT = "//p[text()='Feedback Rating']"
    
    # Unit Dropdown
    UNIT_DROPDOWN = "//mat-label[contains(text(), 'Unit')]/ancestor::mat-form-field//mat-select | //mat-form-field[.//mat-label[contains(., 'Unit')]]//mat-select"
    DAYS_OPTION = "//mat-option//span[text()='Days']"
    
    # Expiry Duration Value Dropdown
    EXPIRY_DURATION_DROPDOWN = "//mat-label[contains(text(), 'Expiry Duration Value')]/ancestor::mat-form-field//mat-select | //mat-form-field[.//mat-label[contains(., 'Expiry Duration Value')]]//mat-select"
    DURATION_VALUE_1 = "//mat-option//span[text()='1']"
    
    # Manual Radio Button
    MANUAL_RADIO = "//label[text()='Manual ']"
    
    # Categories
    ADD_CATEGORIES_BUTTON = "//button[contains(., 'Add Categories')]"
    CATEGORY_NAME_INPUT = "//input[@formcontrolname='feedbackCategory']"
    ICON_DROPDOWN = "//mat-label[text()='Icon']/ancestor::mat-form-field//mat-select | //mat-form-field[.//mat-label[text()='Icon']]//mat-select"
    ICON_OPTION = "//mat-option[position()=1]//img"  # First icon option
    
    # Messages
    ADD_MESSAGES_BUTTON = "//button[contains(., 'Add Messages')]"
    MESSAGE_TEXTBOX = "//textarea[@formcontrolname='templateContent']"
    PERSONALIZE_BUTTON = "//button[contains(., 'Personalize')]"
    SCREEN_NAME_MENU = "//span[text()='Screen Name']"
    FEEDBACK_LINK_MENU = "//span[text()='Feedback Link']"
    ADD_MESSAGE_BUTTON = "//button[contains(., 'Add') and not(contains(., 'Categories')) and not(contains(., 'Messages'))]"
    RESET_BUTTON = "//button[contains(., 'Reset')]"
    
    # Layout Theme
    LAYOUT_THEME_TEXT = "//span[text()= 'Layout Theme']"
    LAYOUT_THEME_CARD_3 = "(//input[@type='radio'])[6]"
    LAYOUT_RADIO_5 = "//input[@id='mat-radio-5-input' or @type='radio'][position()=5]"
    SELECT_BUTTON = "//button[contains(., 'Select')]"
    
    # Preview and Save
    PREVIEW_IN_BROWSER = "//span[text()='Preview in browser']"
    SAVE_FEEDBACK_BUTTON = "//button[contains(., 'Save') and not(contains(., 'Response'))]"
    SUCCESS_MESSAGE_FEEDBACK = "//div[text()='Saved successfully.' or contains(text(), 'Saved successfully')]"
    
    # Manage Brands Elements
    MANAGE_BRANDS_LINK = "//span[text()='Manage Brands']"
    ADD_BRAND_BUTTON = "//button[contains(., 'Add Brand')]"
    ADD_BRAND_P_TAG = "//p[text()='Add Brand']"
    
    # Add Brand Form - Brand Details
    BRAND_NAME_FIELD = "//input[@formcontrolname='brandFriendlyName']"
    COUNTRY_DROPDOWN = "//mat-label[contains(text(), 'Country')]/ancestor::mat-form-field//mat-select"
    COUNTRY_SEARCH_FIELD = "//input[@placeholder='Search country']"
    INDIA_OPTION = "//span[text()='India ']"
    
    # Brand Logo Upload
    PHOTO_CAMERA_ICON = "//mat-icon[text()='photo_camera']"
    FILE_INPUT = "//input[@type='file']"
    
    # Brand Color
    SELECT_BRAND_COLOR = "//div[contains(@class, 'addbrands__body--left-selectbrandcolorwrapper')]"
    VIEW_OTHER_COLORS = "//p[contains(text(), 'View other brand colors')]"
    
    # AI Fields
    AI_FRIENDLY_NAME_FIELD = "//input[@id='aiFriendlyName']"
    GENERATE_DESCRIPTION_BUTTON = "//button[contains(., 'Generate Description')]"
    BRAND_DESCRIPTION_FIELD = "//textarea[@id='aiTagBrandDescription']"
    
    # Ticket Creation Toggle
    TICKET_CREATION_TOGGLE = "//input[@id='rounded-toggle-switch']"
    
    # Assign Users
    SEARCH_USERS_FIELD = "//input[@placeholder='Search users']"
    
    # Brand Engagement Guidelines
    BRAND_GUIDELINES_EDITOR = "//ckeditor[@formcontrolname='brandResponseGuidelines']"
    
    # Category Group
    CATEGORY_GROUP_DROPDOWN = "//mat-label[contains(text(), 'Category Group')]/ancestor::mat-form-field//mat-select"
    DEFAULT_OPTION = "//mat-option//span[text()='Default']"
    CATCHALL_CATEGORY_DROPDOWN = "//mat-label[contains(text(), 'Catch-all Category')]/ancestor::mat-form-field//mat-select"
    
    # Products & Services
    ADD_PRODUCT_BUTTON = "//p[text()='Add Product']"
    PRODUCT_NAME_FIELD = "//input[@placeholder='Enter Product Name']"
    
    # Competitors
    USE_MAPPED_COMPETITORS_TOGGLE = "//input[@id='rounded-toggle-switch-1']"
    ADD_COMPETITOR_BUTTON = "//p[text()='Add Competitor']"
    
    # Save/Cancel Buttons
    SAVE_BRAND_BUTTON = "//button[contains(., 'Save Brand')]"
    CANCEL_BUTTON = "//button[contains(., 'Cancel')]"
    
    # Validation Messages
    VALIDATION_BRAND_NAME = "//*[contains(text(), 'Brand Name') and contains(text(), 'required')]"
    VALIDATION_AI_FRIENDLY_NAME = "//*[contains(text(), 'AI Friendly Name') and contains(text(), 'required')]"
    VALIDATION_COUNTRY = "//*[contains(text(), 'Country') and contains(text(), 'required')]"
    VALIDATION_LOGO = "//*[contains(text(), 'logo') and contains(text(), 'required')]"
    SUCCESS_MESSAGE_GENERIC = "//*[contains(text(), 'successfully') or contains(text(), 'Successfully')]"
    
    # Brand Details
    BRAND_NAME_FIELD = "//input[@formcontrolname='brandFriendlyName']"
    COUNTRY_DROPDOWN = "//mat-label[contains(text(), 'Country')]/ancestor::mat-form-field//mat-select"
    COUNTRY_SEARCH_FIELD = "//input[@placeholder='Search country']"
    INDIA_OPTION = "//span[text()='India ']"
    AI_FRIENDLY_NAME_FIELD = "//input[@placeholder='AI Friendly Name *' or contains(@formcontrolname, 'aiFriendlyName')]"
    GENERATE_DESCRIPTION_BUTTON = "//button[contains(., 'Generate Description')]"
    
    # Brand Logo Upload
    PHOTO_CAMERA_ICON = "//mat-icon[text()='photo_camera'] | //span[text()='photo_camera']"
    FILE_INPUT = "//input[@type='file']"
    SAVE_UPLOAD_BUTTON = "//button[contains(., 'Save') and not(contains(., 'Brand'))]"
    
    # Brand Configuration
    OR_THIS_ONE_RADIO = "//label[contains(text(), 'Or this one')]"
    SEARCH_USERS_FIELD = "//input[@placeholder='Search users' or contains(@aria-label, 'Search users')]"
    USER_CHECKBOX = "//mat-checkbox[contains(., '{user}')]//input | //span[contains(text(), '{user}')]/ancestor::mat-checkbox//input"
    JUWSA = "//label[text()=' juwsa (Supervisor Agent) ']"
    TICKET_CREATION_TOGGLE = "//label[@for='rounded-toggle-switch']"
    
    # Editor
    EDITOR_IFRAME = "//iframe[contains(@title, 'Editor')]"
    EDITOR_BODY = "//body[@role='textbox'] | //body[contains(@class, 'cke_editable')]"
    
    # Category Configuration
    CATEGORY_GROUP_DROPDOWN = "//mat-label[contains(text(), 'Category Group')]/ancestor::mat-form-field//mat-select"
    DEFAULT_OPTION = "//mat-option//span[text()='Default']"
    CATCHALL_CATEGORY_DROPDOWN = "//mat-label[contains(text(), 'Catch-all Category')]/ancestor::mat-form-field//mat-select"
    MANAGER_APPROVAL_PENDING_OPTION = "//span[text()='ManagerApprovalPending ']"
    
    # Product Management
    ADD_PRODUCT_BUTTON = "//p[text()='Add Product']"
    PRODUCT_NAME_FIELD = "//input[@placeholder='Enter Product Name']"
    SYNONYMS_FIELD = "//input[@placeholder='Add Synonym']"
    SAVE = "//span[text()='Save']"
    
    # Final Actions
    SAVE_BRAND_BUTTON = "//button[contains(., 'Save Brand')]"
    SUCCESS_MESSAGE_GENERIC = "//*[contains(text(), 'successfully') or contains(text(), 'Successfully')]"
    
    # Validation Messages
    VALIDATION_PLEASE_FILL = "//*[contains(text(), 'Please fill in the following')]"
    VALIDATION_SELECT_LOGO = "//*[contains(text(), 'Please select brand logo')]"
    VALIDATION_SELECT_COUNTRY = "//*[contains(text(), 'Please select Country')]"
    VALIDATION_SELECT_CATCHALL = "//*[contains(text(), 'Please select a catch-all')]"
    VALIDATION_ASSIGN_USER = "//*[contains(text(), 'Please assign at least one')]"
    VALIDATION_PRODUCT_NAME = "//*[contains(text(), 'Product Name is required')]"
    
    # Product/Competitor Delete and Save
    DELETE_BUTTON = "//mat-icon[text()='delete']"
    YES_CONFIRM_BUTTON = "//button[contains(., 'Yes')]"
    SAVE_PRODUCT_BUTTON = "//button[contains(., 'Save') and not(contains(., 'Brand'))]"
    
    # Competitor Management
    ADD_COMPETITOR_BUTTON = "//p[text()='Add Competitor'] | //span[text()='Add Competitor']"
    COMPETITOR_NAME_FIELD = "//input[@placeholder='Enter competitor name']"
    CHECK_BUTTON = "//button[contains(@class, 'check') or .//mat-icon[text()='check']]"
    
    # Upload dialog
    UPLOAD_DIALOG = "#mat-mdc-dialog-0"
    
    # Brand Search and Edit
    SEARCH_BRAND_FIELD = "//input[@placeholder='Search by Brand Name, Users'] | //input[contains(@placeholder, 'Search by Brand')]"
    SEARCH_BRAND_BUTTON = "//app-grid-header//button[contains(., 'search')] | //button[@aria-label='search']"
    EDIT_BRAND_BUTTON = "//span[text()='Edit'] | //button[contains(., 'Edit')]"
    UPDATE_BRAND_BUTTON = "//button[contains(., 'Update Brand')]"
    BRAND_UPDATE_SUCCESS_MESSAGE = "//*[contains(text(), 'Brand updated successfully')]"
    
    # Manage Users Elements
    MANAGE_USERS_LINK = "//span[text()='Manage Users'] | //a[contains(., 'Manage Users')]"
    ADD_USER_BUTTON = "//button[contains(., 'Add User')]"
    SAVE_USER_BUTTON = "//button[contains(., 'Save User')]"
    
    # User Form Fields
    FIRST_NAME_LABEL = "//input[@formcontrolname='firstName']"
    FIRST_NAME_FIELD = "//input[@placeholder='First Name'] | //input[contains(@formcontrolname, 'firstName')]"
    LAST_NAME_LABEL = "//input[@formcontrolname='lastName']"
    LAST_NAME_FIELD = "//input[@placeholder='Last Name'] | //input[contains(@formcontrolname, 'lastName')]"
    USERNAME_FIELD = "//input[@formcontrolname='userName']"
    EMAIL_LABEL = "//input[@formcontrolname='emailID']"
    EMAIL_FIELD = "//input[@placeholder='Email'] | //input[contains(@formcontrolname, 'email')]"
    
    # Brand Assignment
    SEARCH_BRANDS_COMBOBOX = "//input[@aria-label='Search Brands'] | //input[@placeholder='Search Brands']"
    JUWS_BRAND_SELECTION = "//span[text()='Juws']"
    
    # User Validation Messages
    VALIDATION_NO_SPECIAL_CHARS = "//*[contains(text(), 'No special characters allowed')]"
    VALIDATION_ADD_USERNAME = "//*[contains(text(), 'Please add username')]"
    VALIDATION_ADD_EMAIL = "//*[contains(text(), 'Please add email')]"
    VALIDATION_VALID_EMAIL = "//*[contains(text(), 'Please add a valid email')]"
    VALIDATION_ASSIGN_BRANDS = "//*[contains(text(), 'Please assign brands')]"
    VALIDATION_EMAIL_EXISTS = "//*[contains(text(), 'Email already exists')]"
    
    # User Actions
    PROCEED_WITHOUT_ADDING_BUTTON = "//button[contains(., 'Proceed without adding')]"
    USER_ADDED_SUCCESS_MESSAGE = "//*[contains(text(), 'User Added Successfully')]"
    
    # Edit User Elements
    SEARCH_USER_FIELD = "//input[@placeholder='Search by User Name, First/'] | //input[contains(@placeholder, 'Search by User')]"
    SEARCH_USER_BUTTON = "//app-manageusers//button[contains(., 'search')] | //button[@aria-label='search']"
    USER_ROW_ACTION_BUTTON = "(//mat-icon[text()='more_horiz'])[1]"
    EDIT_MENU_ITEM = "//span[text()='Edit']"
    
    # Role Dropdown
    ROLE_DROPDOWN = "//mat-label[text()='Role']/ancestor::mat-form-field//mat-select | //mat-select[contains(@aria-label, 'Role')]"
    SUPERVISOR_AGENT_OPTION = "//span[text()='Supervisor Agent'] | //mat-option[contains(., 'Supervisor Agent')]"
    AGENT_OPTION = "(//span[text()='Agent'])[4]"
    
    # Update User
    UPDATE_USER_BUTTON = "//button[contains(., 'Update User')]"
    USER_UPDATED_SUCCESS_MESSAGE = "//*[contains(text(), 'User updated successfully')]"
    
    # Delete User Elements
    DELETE_MENU_ITEM = "//span[text()='Delete'] | //button[contains(., 'Delete')]"
    YES_DELETE_BUTTON = "//button[contains(., 'Yes')]"
    USER_DELETED_SUCCESS_MESSAGE = "//span[contains(text(), 'deleted successfully')]"
