"""
Bulk Actions page element locators
"""

class BulkActionsPageElements:
    
    # Checkbox Selectors 
    BILALTEST1CX = "//a[span[normalize-space()='bilaltest1cx']]/ancestor::app-post-head/following-sibling::app-post-foot//input[@type='checkbox']"
    PRAGYAANTEST = "//a[contains(normalize-space(.),'pragyaantest')]/ancestor::app-post-head/following-sibling::app-post-foot//input[@type='checkbox']"
    ABDUL_A = "(//span[contains(normalize-space(),'Abdul A')]/ancestor::app-post-head/following::mat-checkbox)[1]//input[@type='checkbox']"
    PRAVEEN_SINGA = "//span[normalize-space()='Praveen Singa']/ancestor::app-post-head/following-sibling::app-post-foot//input[@type='checkbox']"
    ASISHLOCOUSER = "//app-post-head[.//span[normalize-space()='asishlocouser']]/following-sibling::app-post-body/following-sibling::app-post-foot//mat-checkbox//input[@type='checkbox']"
    KC_SUMO= "//app-post-head[.//span[text()='kc.sumo']]/following::app-post-foot[1]//input[@type='checkbox']"
    
    # Bulk Action Buttons
    RETAG_CATEGORY_BUTTON = "//span[normalize-space()='Retag Category']"
    ASSIGN_BUTTON = "//button//span[normalize-space()='Assign']"
    PUT_ON_HOLD_BUTTON = "//button//span[normalize-space()='Put on hold']"
    ESCALATE_BUTTON = "//button//span[normalize-space()='Escalate']"
    REPLY_BUTTON = "//button//span[normalize-space()='Reply']"
    REOPEN_BUTTON = "//button//span[normalize-space()='Reopen']"
    DIRECT_CLOSE_BUTTON = "//button//span[normalize-space()='Direct Close']"
    
    # Retag Category Elements
    PREMIUM_CHECKBOX = "//mat-checkbox//span[contains(text(),'Premium')]//preceding-sibling::input"
    POSITIVE_RADIO = "//mat-radio-button//span[contains(text(),'Positive')]//preceding-sibling::input"
    NEGATIVE_RADIO = "//mat-radio-button//span[contains(text(),'Negative')]//preceding-sibling::input"
    NEUTRAL_RADIO = "//mat-radio-button//span[contains(text(),'Neutral')]//preceding-sibling::input"
    SUBMIT_RETAG = "//button//span[text()='Submit']"
    
    # Assign Elements
    ASSIGN_FORM_DROPDOWN = "//form[@id='assignToForm']//mat-icon[text()='expand_more']"
    BILAL_SHAIKH_OPTION = "//span[contains(text(),'Bilal Shaikh')]"
    ASSIGN_CONFIRM_BUTTON = "//span[text()=' Assign ']"
    
    # Put on Hold Elements
    NOTE_FIELD = "//label[.//mat-label[normalize-space()='Add note']]/following::textarea[1]"
    SAVE_BUTTON = "//button//span[text()='Save']"
    
    # Escalate Elements
    ESCALATE_TO_DROPDOWN = "//mat-form-field[contains(.,'Escalate To')]//mat-icon[text()='expand_more']"
    JUWAIRIA_CSD_OPTION = "//span[contains(text(),'Juwairia CSD')]"
    ESCALATION_NOTE_FIELD = "//textarea[@placeholder='Write escalation note here...']"
    SEND_BUTTON = "//span[normalize-space()='Send']"
    
    # Reply & Close Elements
    REPLY_TYPE_DROPDOWN = "//mat-label[normalize-space(text())='Reply Type']/ancestor::mat-form-field//mat-select"
    REPLY_CLOSE_OPTION = "//mat-option//span[contains(text(),'Reply & Close')]"
    REPLY_AWAIT_OPTION = "//mat-option//span[contains(text(),'Reply & Await')]"
    REPLY_FIELD = "//textarea[@placeholder='Write Reply']"
    
    # Navigation Elements
    ON_HOLD_TAB = "//a[text()='On Hold ']"
    ON_HOLD_TAB_GENERIC = "//span[contains(text(),'On Hold')]"
    MORE_BUTTON = "//a[text()='More ']"
    CLOSED_TICKETS_MENU = "//span[text()=' Closed Tickets ']" 
    OPEN_TAB = "//a[text()='Open ']"
    CLOSED_TICKETS_TAB = "//a[text()='Closed Tickets ']"
    
    # Reopen Elements
    REOPEN_NOTE_FIELD = "//textarea[@placeholder='Enter note here']"
    SAVE_REOPEN_BUTTON = "//button//span[text()='Save']"
    
    # Direct Close Elements
    CONTINUE_BUTTON = "//button//span[text()='Continue']"
