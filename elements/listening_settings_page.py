"""
Location Profile page element locators
"""

class ListeningSettingsPageElements:
    """XPath elements for Location Profile under Account Settings"""
    
    # Location Profile
    LOCATION_PROFILE_LINK = "//span[text()='Location Profile']"
    
    # Add New Location
    ADD_NEW_LOCATION_BUTTON = "//button[contains(., 'Add New Location')]"
    
    # Form Fields
    LOCATION_NAME_FIELD = "//input[@placeholder='Location Name*' or contains(@formcontrolname, 'locationName')]"
    ADDRESS_FIELD = "//input[@formcontrolname='locationAddress']"
    CITY_FIELD = "//input[@placeholder='City *' or contains(@formcontrolname, 'city')]"
    STATE_FIELD = "//input[@placeholder='State *' or contains(@formcontrolname, 'state')]"
    
    # Country Dropdown
    COUNTRY_DROPDOWN = "//mat-select[contains(@aria-label, 'Country')] | //label[contains(., 'Country')]/following-sibling::mat-select | //mat-form-field[.//mat-label[contains(., 'Country')]]//mat-select"
    SEARCH_COUNTRY_FIELD = "//input[@placeholder='Search Country']"
    INDIA_OPTION = "//span[text()='India']"
    
    # Pin Code
    PIN_CODE_FIELD = "//input[@formcontrolname='pincode']"
    
    # Coordinates
    LATITUDE_FIELD = "//input[@placeholder='Latitude *' or contains(@formcontrolname, 'latitude')] | //input[@type='number' and contains(@placeholder, 'Latitude')]"
    LONGITUDE_FIELD = "//input[@placeholder='Longitude *' or contains(@formcontrolname, 'longitude')] | //input[@type='number' and contains(@placeholder, 'Longitude')]"
    
    # Save Button
    SAVE_LOCATION_BUTTON = "//button[contains(., 'Save Location') or contains(., 'Save')]"
    
    # Validation Messages
    VALIDATION_ADDRESS = "//*[contains(text(), 'Please enter Location Address')]"
    VALIDATION_CITY = "//*[contains(text(), 'Please enter City')]"
    VALIDATION_STATE = "//*[contains(text(), 'Please enter State')]"
    VALIDATION_COUNTRY = "//*[contains(text(), 'Please select Country')]"
    VALIDATION_PINCODE = "//*[contains(text(), 'Please enter pincode')]"
    VALIDATION_LATITUDE = "//*[contains(text(), 'Please enter Latitude')]"
    VALIDATION_LONGITUDE = "//*[contains(text(), 'Please enter Longitude')]"
    
    # Success Message
    SUCCESS_MESSAGE = "//*[contains(text(), 'Location saved successfully')]"
    
    # Search and Filter Locations
    SEARCH_LOCATION_FIELD = "//input[@id='mat-input-6'] | //input[contains(@placeholder, 'Search') and ancestor::app-location-manager]"
    SEARCH_BUTTON = "//button[contains(., 'search') and ancestor::app-location-manager] | //button[.//mat-icon[text()='search']]"
    
    # Edit Location
    EDIT_LOCATION_BUTTON = "//img[contains(@alt, 'edit_location')] | //button[contains(., 'edit') or .//mat-icon[text()='edit']]"
    UPDATE_LOCATION_BUTTON = "//button[contains(., 'Update Location')]"
    UPDATE_SUCCESS_MESSAGE = "//*[contains(text(), 'Location updated successfully')]"
    
    # Delete Location
    DELETE_LOCATION_BUTTON = "//img[contains(@alt, 'delete') or contains(@src, 'delete')] | //button[contains(., 'delete') or .//mat-icon[text()='delete']]"
    CONFIRM_DELETE_BUTTON = "//button[contains(., 'Yes')]"
    DELETE_SUCCESS_MESSAGE = "//*[contains(text(), 'Location deleted successfully')]"
    
    # Location Row
    LOCATION_ROW_BY_NAME = lambda name: f"//tr[contains(., '{name}')]"

    # Category Mapping (for Account Settings)
    CATEGORY_MAPPING_LINK = "//a[contains(text(), 'Category Mapping') or @href='category-mapping']"
    CREATE_NEW_CATEGORY_BUTTON = "//button[contains(., 'Create New Category')]"
    CATEGORY_NAME_FIELD = "//input[@formcontrolname='feedbackCategory']"
    SAVE_BUTTON = "//button[contains(., 'Save') and not(contains(., 'Response'))]"
    ENTER_KEYWORDS_FIELD = "//input[@placeholder='Enter Keywords'] | //input[contains(@id, 'chip-list-input')]"
    ADVANCE_QUERY_BUILDER = "//span[text()='Advance Query Builder'] | //button[contains(., 'Advance Query Builder')]"
    ALL_WORDS_AND_FIELD = "//input[@placeholder='All these words (AND)']"
    ANY_WORDS_OR_FIELD = "//input[@placeholder='Any of these words (OR)']"
    NONE_WORDS_NOT_FIELD = "//input[@placeholder='None of these words (Do Not)']"
    OR_RADIO = "//mat-button-toggle-group//button[contains(., 'OR')]"
    ADD_GROUP_BUTTON = "//button[contains(., '+ Add Group')]"
    DELETE_BUTTON = "//mat-icon[text()='delete']"
    YES_BUTTON = "//button[contains(., 'Yes')]"
    SUCCESS_MESSAGE_GENERIC = "//*[contains(text(), 'successfully') or contains(text(), 'Successfully')]"
    SORT_BUTTON = "//button[contains(., 'sort')]"
    ASCENDING_RADIO = "//mat-radio-button//span[contains(text(), 'Ascending')]"
    CATEGORY_NAME_RADIO = "//mat-radio-button//span[contains(text(), 'Category Name')]"
    BRAND_MENTIONS_COMBOBOX = "//mat-select[@aria-label='Brand Mentions']"
    TESTING_OPTION = "//mat-option//span[text()='Testing']"
    BASED_ON_SUBJECT_BODY_RADIO = "//mat-radio-button//span[contains(text(), 'Based on subject and body')]"
    TICKET_CATEGORY_TAGGING_LABEL = "//label[contains(., 'Ticket Category Tagging')]"
    CHECK_CIRCLE_CATEGORY = "//span[contains(text(), 'check_circleTicket Category')]"
    CHIP_LIST_INPUT_1 = "(//input[contains(@id, 'chip-list-input')])[1]"
    CHIP_LIST_INPUT_2 = "(//input[contains(@id, 'chip-list-input')])[2]"
