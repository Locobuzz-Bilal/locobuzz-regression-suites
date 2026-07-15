"""
    Reply Workflow Panel Page Elements
"""

class ReplyPanelPageElements:


    #Starting from Reply & Assign
    # Search Ticket Icon
    SEARCH_ICON = "//a[.//mat-icon[text()=' search']]"
    # Search Input Box - Ticket ID
    
    SEARCH_INPUT_BOX = '//input[@placeholder="Search for a Ticket ID, Author Name, Content or URL"]'

    # Reply Input Box - Main reply textarea
    REPLY_INPUT_BOX = '//textarea[@placeholder="Write Reply"]'

    # Reply Button
    REPLY_BUTTON = "//span[text()='Reply']"

    # Discard and Submit Button
    DISCARD_BUTTON = "//span[text()=' Discard ']"
    DISCARD_CANCEL_BUTTON = "(//button//span[text()=' Cancel '])[2]"
    DISCARD_SUBMIT_BUTTON = "//span[normalize-space()='Submit']"

    # Reply Type Dropdown
    REPLY_TYPE_DROPDOWN = "//mat-label[normalize-space(text())='Reply Type']/ancestor::mat-form-field//mat-select"
    EMAIL_REPLY_TYPE_DROPDOWN = "//mat-icon[contains(@class,'cursor-pointer') and contains(text(),'expand_more')]"

    # Reply & Assign Option
    REPLY_AND_ASSIGN_OPTION = "//span[normalize-space()='Reply & Assign']"
    REPLY_AND_ASSIGN_OPTION_ALTERNATE = "//span[contains(normalize-space(),'Reply & Assign')]"

    # Next Button after Reply
    REPLY_NEXT_BUTTON = "//span[text()=' Next ']"

    # Assign To Dropdown
    ASSIGN_TO_DROPDOWN = "(//input[@type='text'])[3]"

    # Juwairia Agent
    JUWAIRIA_AGENT_OPTION = "//span[contains(text(),'Juwairia Agent')]"

    # Add Note
    ADD_NOTE_INPUT = '(//textarea[@formcontrolname="replyEscalateNote"])[2]'

    #Send Button
    SEND_BUTTON = "//span[text()=' Send ']"

    EMAIL_SEND_BTN = "//mat-icon[text()='send']"



    # Starting from Reply & Await-------------------------------
    REPLY_AWAIT_OPTION = "//span[text()=' Reply & Awaiting response from Customer ']"
    MORE_DROPDOWN = "//a[text()='More ']"

    # Starting from Reply & On Hold----------------------------
    More_ICON = "(//a[@aria-haspopup='menu' and .//mat-icon[text()='keyboard_arrow_down']])"

    INBOX = "//mat-icon[text()='inbox']"

    AWAITING_FROM_CUSTOMER_TAB = "//span[text()=' Awaiting From Customer ']"
    

    REPLY_AND_ONHOLD = "//span[text()=' Reply & On Hold ']"

    EMAIL_REPLY_AND_AWAIT = "//span[text()='Reply & Awaiting response from Customer']"
    
    EMAIL_REPLY_AND_ONHOLD = "//span[text()='Reply & On Hold']"
    REPLY_AND_ONHOLD_OPTION_ALTERNATE = "//span[contains(text(),'Reply & On Hold')]"


    NEXT_ARROW="//div[contains(@class, 'mat-mdc-tab-header-pagination') and contains(@class, 'after')]"
    TIMELINE_TAB="//span[text()='Timeline']"

    # Email Reply & Escalate
    EMAIL_REPLY_AND_ESCALATE = "//span[normalize-space()='Reply & Escalate']"
    REPLY_AND_ESCALATE_OPTION_ALTERNATE = "//span[contains(normalize-space(),'Reply & Escalate')]"
    JUWAIRIA_CSD_OPTION = "//span[contains(text(),'Juwairia CSD')]"


    # Starting from Reply & Escalate-------------------------------
    ON_HOLD_TAB = "//a[text()='On Hold ']"
    ON_HOLD_TAB2 = "//span[text()=' On Hold ']"

    REPLY_AND_ESCALATE_OPTION = "//span[text()='  Reply & Escalate ']"

    ESCALATION_NOTE_INPUT_BOX = '//textarea[@placeholder="Write escalation note here..."]'




    #Starting from CSD Approve -------------------------------
    APPROVE_ICON = "//mat-icon[normalize-space()='check_circle_outline']/ancestor::span[contains(@class,'custom__foot--approve')]"
    CSD_APPROVE_ICON_ALTERNATE = "//mat-icon[text()='check_circle_outline']"

    ENTER_APPROVAL_NOTE = "//textarea[@placeholder='Enter Note Here']"
    CSD_APPROVAL_NOTE_INPUT = "//textarea[@placeholder='Enter Note Here']"
    
    CSD_SAVE_BUTTON = "//span[text()=' Save ']"

    ATTACH_PHOTO = "//a[.//mat-icon[text()='insert_photo']]"

    PHOTO_URL = "//img[contains(@src,'002c68f8-4ff7-4678-b064-e6322f903bb8.png')]"

    ATTACH_BUTTON = "//button//span[normalize-space(text())='Attach']"

    PHOTO_SAVE_BUTTON = "//button//span[normalize-space(text())='Save']"

    #Starting from Reply & Close -------------------------------

    PENDING_TAB = "//a[text()='Pending ']"
    PENDING_TAB_ALTERNATE = "//span[contains(text(),'Pending')]"
    DISMISS = "//a[text()='Dismiss']"

    REPLY_AND_CLOSE_OPTION = "//mat-option//span[normalize-space()='Reply & Close']"
    EMAIL_REPLY_AND_CLOSE = "//span[text()='Reply & Close']"
    REPLY_AND_CLOSE_OPTION_ALTERNATE = "//span[contains(text(),'Reply & Close')]"


    # Starting from Other Actions - Open Ticket -------------------------------
    
    #More Options Icon
    MORE_OPTIONS_ICON = "//span[text()=' More ']"
    #//span[text()='Closed Tickets']


    # Closed Tickets Tab
    CLOSED_TICKETS_TAB = "//span[text()='Closed Tickets']"
    CT_TAB_ALTERNATE = "//span[text()=' Closed Tickets ']"
    
    # Account Box Icon
    ACCOUNT_BOX_ICON = "//mat-icon[text()='account_box']"
    
    # Overview Tab
    OVERVIEW_TAB = "//div[@role='tab' and .='Overview']"
    
    # Ticket Status Dropdown
    TICKET_STATUS_DROPDOWN = "//mat-label[normalize-space()='Ticket Status']/ancestor::mat-form-field//div[contains(@class,'mat-mdc-select-trigger')]"
    
    # Open Status Option
    OPEN_STATUS_OPTION = "//mat-option//span[normalize-space()='Open']"
    
    # Close Icon
    CLOSE_ICON = "//mat-icon[text()='close']"
    
    # Open Tab (in ticket list)
    OPEN_TAB = "//a[text()='Open ']"
    #//a[normalize-space(.)='Open' or contains(text(),'Open')]
    
    # More Button
    MORE_BUTTON = "//span[text()='More']"
    
    # Mark Influencer Button
    MARK_INFLUENCER_BUTTON = "//button//span[text()='Mark Influencer']"
    
    # Select Influencer Category Dropdown
    INFLUENCER_CATEGORY_DROPDOWN = "//mat-label[text()='Select Influencer Category']"
    
    # Anchor Option (Influencer Category)
    ANCHOR_OPTION = "//mat-option//span[normalize-space()='Anchor']"
    
    # Mark Influencer Confirm Button
    MARK_INFLUENCER_CONFIRM = "//button//span[text()=' Mark Influencer ']"
    
    # Others Section (Mentions)
    OTHERS_SECTION = "//mat-icon[@role='img' and normalize-space(text())='alternate_email']"
    
    # Mention Category Options
    MENTION_JUW_TESTING_1 = "//label[text()=' juw testing 1']"
    MENTION_TESTING_2 = "//label[text()=' testing 2']"
    MENTION_TESTING_3 = "//label[text()=' testing 3 ']"
    MENTION_NEUTRAL = "//label[text()=' Neutral']"
    MENTION_SUBMIT = "//span[text()='Submit']"
    
    # Open Link Button
    OPEN_LINK_BUTTON = "//span[text()='Open Link']"
    
    # Send Email Button
    SEND_EMAIL_BUTTON = "//span[contains(text(),'Send Email')]"
    
    # Email Input Field
    EMAIL_INPUT_FIELD = "//input[@placeholder='New To Email...']"
    
    # Email Send Button
    EMAIL_SEND_BUTTON = "//span[text()=' Send ']"
    
    # Open Details Button
    OPEN_DETAILS_BUTTON = "//span[text()='Open Details ']"
    
    # Add Note Button
    ADD_NOTE_BUTTON = "//span[text()=' Add Note ']"
    
    # Add Note Text Area
    ADD_NOTE_TEXTAREA = "//mat-form-field[.//mat-label[normalize-space()='Add Note']]//textarea"
    
    # Attach Media Button (for notes)
    ATTACH_MEDIA_BUTTON = "//div[contains(@class,'note-elem')]//a[.//span[normalize-space()='Attach Media']]"
    
    # First Image in Media Gallery
    FIRST_IMAGE = "//img[contains(@src,'002c68f8-4ff7-4678-b064-e6322f903bb8.png')]"
    
    # Attach Button (Media)
    ATTACH_BUTTON_MEDIA = "//button//span[text()=' Attach ']"
    
    # Save Button (for note)
    SAVE_BUTTON = "//span[text()=' Save ']"
    
    # Back to Ticket List Button
    BACK_TO_TICKET_LIST = "//span[text()='Back To Ticket List ']"
    
    # Personal Details Tab
    PERSONAL_DETAILS_TAB = "//span[text()='Personal Details']"
    
    # Name Input Field
    NAME_INPUT_FIELD = "//mat-form-field[.//mat-label[text()='Name']]//input"
    
    # Update Button
    UPDATE_BUTTON = " //span[text()=' Update ']"
    
    # Direct Close Dropdown
    DIRECT_CLOSE_DROPDOWN = "//span[.//span[text()='Direct Close']]//mat-icon[text()='keyboard_arrow_down']"
    
    # Close With Note Option
    CLOSE_WITH_NOTE_OPTION = "//span[text()='Close With Note']"
    
    # Note Text Area (for closing)
    CLOSE_NOTE_TEXTAREA = "//textarea[@name='textArea']"
    
    # Attach Media Button (for closing)
    ATTACH_MEDIA_CLOSE = "//span[text()='Attach Media']"
    
    # Specific Image URL
    SPECIFIC_IMAGE = '//img[@src="https://images.locobuzz.com/LocoBuzzImages/SocialPostTriggerScheduling/reliancejiodb/002c68f8-4ff7-4678-b064-e6322f903bb8.png"]'
    X_IMAGE = '//img[@src="https://images.locobuzz.com/LocoBuzzImages/SocialPostTriggerScheduling/reliancejiodb/8a836253-0c1f-426e-9576-dea6d5ba4e22.jpg"]'
    
    # Attach Button (for closing)
    ATTACH_BUTTON_CLOSE = "//span[text()=' Attach ']"
    
    # Direct Close Button
    DIRECT_CLOSE_BUTTON = "//span[text()=' Direct Close ']"


    # Starting from Closed Ticket Flow -------------------------------
    
    # Profile Image (bilal_superadmin)
    PROFILE_IMAGE = "//img[@src='https://s3.amazonaws.com/locobuzz.socialimages/LocobuzzUserProfileImages/reliancejiodb/caf8c5b1-b7ec-46e6-a351-12845d3d37f3.png']"
    
    # Account Settings
    ACCOUNT_SETTINGS = "//span[text()='Account Settings']"
    
    # Search Box (Account Settings)
    SEARCH_BOX = "//input[@placeholder='Search']"
    
    # Ticket Disposition Link
    TICKET_DISPOSITION_LINK = "//a[@href='/account/ticketdisposition']"
    
    # Feature Active/Inactive Text
    FEATURE_ACTIVE = "//p[contains(text(),'Feature Active')]"
    FEATURE_INACTIVE = "//p[contains(text(),'Feature Inactive')]"
    
    # Toggle Switch Label
    TOGGLE_SWITCH_LABEL = "//div[@class='rounded-toggle-switch']/label[@for='rounded-toggle-switch-ticketDispositions']"
    
    # Yes Button (Confirmation)
    YES_BUTTON = "//span[text()='Yes']"
    
    # Logout Option
    LOGOUT_OPTION = "//span[text()='Logout']"
    
    # Logout Confirm Button
    LOGOUT_CONFIRM = "//span[text()=' Logout ']"
    
    # Select All Button
    SELECT_ALL_BUTTON = "//span[text()='Select All']"
    
    # Disposition Name Dropdown
    DISPOSITION_NAME_DROPDOWN = "//mat-select[@formcontrolname='dispositionName']"
    
    # Product Related Option
    PRODUCT_RELATED_OPTION = "//mat-option[.//span[text()='Product Related']]"
    
    # Enter Note Textarea
    ENTER_NOTE_TEXTAREA = "//textarea[@placeholder='Enter note']"
    
    # Save & Close Button
    SAVE_AND_CLOSE_BUTTON = "//span[text()=' Save & Close ']"


    CLOSE_ICON="//mat-icon[text()='close']"

    #Canned Response with attachment
    CANNED_RESPONSE="//img[@src='assets/images/chatbot/canned.svg']"
    CANNED_RESPONSE_ICON = "//img[@src='assets/images/chatbot/canned.svg']"  # 3rd image icon in reply panel
    CANNED_RESPONSE_DROPDOWN = "(//div[contains(@class,'inputWithClose')]//input[@type='text'])[2]"
    SELECT_CANNED_BUTTON = "//button//span[text()=' Select ']"
    SEARCH_FIELD = "//input[@placeholder='Search for a Ticket ID, Author Name, Content or URL']"
    SELECT="//span[text()=' Select ']"

    #Response genie
    USE="//span[text()=' Use ']"

    #Attach media
    ATTACH_MEDIA="(//mat-icon[text()='insert_photo'])[1]"
    MEDIA="(//mat-icon[text()='check_circle'])[1]"

    #Cancel btn
    CANCEL = "//span[text()=' Cancel ']"

    #Edit btn
    EDIT='//span[text()="Edit"]'

    #update btn
    UPDATE='//span[text()=" Update "]'

    #Delete btn
    DELETE='//span[text()="Delete"]'


    # Chatbot Elements -------------------------------
    # Chat bubble icon to open chatbot
    CHAT_BUBBLE_ICON = "//img[@alt='chat bubble icon']"
    
    # Chatbot reply input
    CHATBOT_REPLY_INPUT = "//textarea[@placeholder='Write your reply']"
    
    # Chatbot send button
    CHATBOT_SEND_BUTTON = "//button[contains(@class, 'send') or .//mat-icon[text()='send']]"
    
    # Attach file icon
    CHATBOT_ATTACH_FILE_ICON = "//mat-icon[text()='attach_file']"
    CHATBOT_ATTACH_BTN = "//span[text()=' Attach ']"
    
    # Apple logo file option
    CHATBOT_APPLE_LOGO = "//div[contains(text(), 'appleLogo.png')] | //span[contains(text(), 'appleLogo.png')]"
    
    # Emoji/satisfied icon
    CHATBOT_EMOJI_ICON = "(//mat-icon[normalize-space()='sentiment_satisfied_alt'])[1]"
    
    # Select button for emoji
    CHATBOT_EMOJI = "//span[@aria-label='😃, smiley']"
    
    # Escalation warning icon
    CHATBOT_ESCALATE_ICON = "//mat-icon[text()='escalator_warning']"
    
    # Escalate To dropdown
    CHATBOT_ESCALATE_DROPDOWN = "//mat-form-field[contains(., 'Escalate To')]//mat-icon"
    
    # Juwairia CSD option in escalate dropdown
    CHATBOT_JUWAIRIA_CSD = "//mat-option//span[contains(text(), 'Juwairia CSD')]"
    
    # Escalation note textarea
    CHATBOT_ESCALATION_NOTE = "//textarea[@placeholder='Write escalation note here...']"
    
    # Send button for escalation
    CHATBOT_SEND_ESCALATION = "//button[text()='Send' or contains(., 'Send')]"
    
    # Cancel/close chatbot button
    CHATBOT_CANCEL_BUTTON = "//app-chatbot//mat-icon[text()='cancel'] | //mat-icon[text()='close']"
    
    # Yes button to confirm close
    CHATBOT_YES_BUTTON = "//button[text()='Yes' or contains(., 'Yes')]"
    
    # Success message
    CHATBOT_SUCCESS_MESSAGE = "//*[contains(text(), 'Ticket Closed successfully')]"
    
    # Close notification link
    CHATBOT_CLOSE_NOTIFICATION = "//a[contains(@class, 'close') or .//mat-icon[text()='close']]"

    #Chatbot close ticket button
    CHATBOT_CLOSE_BUTTON = "//mat-icon[text()='cancel']"

    #Chatbot canned response icon
    CHATBOT_CANNED_RESPONSE_ICON = "//img[@src='assets/images/chatbot/canned.svg']"

    #Chatbot select btn
    CHATBOT_SELECT_BUTTON = "//span[text()=' Select ']"