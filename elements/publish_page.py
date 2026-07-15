"""
Publish page element locators
"""

class PublishPageElements:
    # Navigation
    PUBLISH_LINK = "//a[contains(., 'Publish')]//span[contains(text(), 'Publish')]"
    
    # Brand Selection
    BRAND_DROPDOWN = "//div[contains(@class, 'mat-mdc-select-arrow-wrapper')]"
    JUWS_BRAND_OPTION = "//span[text()=' Juws ']"
    
    # Compose
    COMPOSE_POST_BUTTON = "//button[contains(., 'Compose Post')]"
    LOCATION_MODE_BUTTON = "//button[contains(., 'Location Mode')]"
    
    # Account Selection
    FIRST_IMAGE = "(//img)[1]"
    ACCOUNT_CHECKBOX = "//input[@type='checkbox']"
    
    # Navigation Buttons
    NEXT_BUTTON = "//button[contains(., 'Next')]"
    
    # Media Attachment
    ATTACH_IMAGE_BUTTON = "//span[text()='Attach Image']"
    GALLERY_FIRST_IMAGE = "(//mat-icon[text()='check_circle'])[1]"
    ATTACH_BUTTON = "//span[text()=' Attach ']"
    
    # Caption
    CAPTION="//textarea[@formcontrolname='description']"
    CAPTION_FIELD = "//input[@placeholder='Enter post labels...']"
    
    # Publishing Options
    PUBLISH_NOW_RADIO = "//mat-radio-button//span[contains(text(), 'Publish Now')]"
    PUBLISH_LATER_RADIO = "//label[text()='Publish Later']"
    
    # Actions
    SEND_APPROVAL_BUTTON = "//button[contains(., 'Send for Approval')]"
    SAVE_DRAFT_BUTTON = "//button[contains(., 'Save Draft')]"
    
    # Post Management
    EDIT_ICON = "//mat-icon[text()='edit']"
    DELETE_ICON = "(//mat-icon[text()='delete_outline'])[1]"
    DELETE_CONFIRM_BUTTON = "//button[contains(., 'Delete')]"
    
    # Date Picker
    DATE_PICKER = "//mat-icon[text()='calendar_month']"
    DATE_29 = "(//span[text()='29'])[8]"
    APPLY_BUTTON = "(//button[text()='Apply'])[2]"
    
    # Location Mode Filters
    CITIES_DROPDOWN = "//mat-label[text()='Cities']"
    NEW_DELHI_OPTION = "//span[contains(text(), 'New Delhi')]"
    TAGS_DROPDOWN = "//mat-label[text()='Tags']"
    TAG_CHECKBOX = "//label[text()=' All ']"
    CHANNELS_DROPDOWN = "//mat-label[text()='Channels']"
    FACEBOOK_CHANNEL = "//mat-option//span[contains(text(), 'Facebook')]"
    OVERLAY_BACKDROP = ".cdk-overlay-backdrop.cdk-overlay-transparent-backdrop"
    APPLY_FILTERS_BUTTON = "//button[contains(., 'Apply')]"
    
    # No Data & Search
    NO_DATA_FOUND = "//p[contains(text(), 'No Data Found')]"
    CLEAR_ALL_FILTERS_BUTTON = "//button[contains(., 'Clear All Filters')]"
    SEARCH_LOCATION_INPUT = "//input[@placeholder='Search by name, city, tag.']"
    
    # Social Profile Selection
    PROFILE_CHECKBOX = "//mat-checkbox//input[@type='checkbox']"
    
    # Personalization
    PERSONALIZE_BUTTON = "//span[text()='Personalize']"
    PHONE_NUMBER_OPTION = "//li[text()=' PhoneNumber']"
    DISMISS_LINK = "//a[text()='Dismiss']"
    
    # Caption with placeholder
    CAPTION_TEXTAREA = "//textarea[@placeholder=\"What's on your mind?\"]"
    ATTACH_IMAGE_LINK = "//span[text()='Attach Image']"
    GALLERY_CHECK_CIRCLE = "(//mat-icon[text()='check_circle'])[1]"
    ATTACH_MODAL_BUTTON = "//button[contains(., 'Attach')]"
