"""
Manual Regression Sheet element locators
"""

class ManualRegElements:
    
    # Search Elements
    SEARCH_ICON = "//a[.//mat-icon[text()=' search']]"
    SEARCH_INPUT = "//input[@placeholder='Search for a Ticket ID, Author Name, Content or URL']"
    
    # Ticket Actions
    PRIORITY_LOW = "//span[text()='Low']"
    PRIORITY_MEDIUM = "//span[text()='Medium']"
    PRIORITY_HIGH = "//mat-option//span[text()='High']"
    
    # Duration/Date Filter
    DURATION_INPUT = "//input[@placeholder='Select Duration']"
    LAST_30_DAYS = "//button[text()='Last 30 Days']"
    CUSTOM_BUTTON = "//button[text()='custom']"
    DONE_BUTTON = "//button[text()='Done']"
    TODAY_BUTTON = "//button[text()='Today']"
    
    # More Options
    MORE_OPTIONS_ICON = "//span[text()='More']"
    ATTACH_TICKET_MENU = "//button[@role='menuitem']//span[text()='Attach Ticket']"
    
    # Attach Ticket Dialog
    ATTACH_TO_DROPDOWN = "//mat-label[text()='Attach to']/ancestor::mat-form-field//mat-select"
    ATTACH_NOTE_FIELD = "//textarea[@placeholder='Add note']"
    ATTACH_BUTTON = "//span[normalize-space()='Attach']"
    
    # Add Tab
    ADD_TAB_ICON = "//a[.//mat-icon[normalize-space(text())='add']]"
    ADD_TAB_BUTTON = "//span[normalize-space()='Add Tab']"
    TAB_NAME_INPUT = "//input[@formcontrolname='GroupName']"
    SUBMIT_TAB_BUTTON = "//span[normalize-space()='Submit']"

#   Create Ticket
    CREATE_TICKET_BUTTON = "//span[text()=' Create Ticket']"
    ENTER_NOTE_HERE  = '//textarea[@placeholder="Enter note here"]'
    
    # Tab Ticket Count
    OPEN_TAB_COUNT = "//a[contains(@class,'active')]//span[contains(text(),'(') and contains(text(),')')]"