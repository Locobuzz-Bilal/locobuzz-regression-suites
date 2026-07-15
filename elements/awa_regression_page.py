class AWAElements:

    OVERVIEW_TAB = "//span[text()='Overview']"

    # Main navigation
    WIDGETS_MAKER_BUTTON = "//span[text()='Widgets Maker']"

    # iframe
    ANALYTICS_IFRAME = "//iframe[@name='analyticsFrame']"

    # In-iframe elements (use relative XPATH after switching to iframe)
    CREATE_NEW_WIDGET_BUTTON = "//button[.//span[text()='Create New Widget'] or contains(., 'Create New Widget')]"
    GRID = "//img[@src='/static/media/grid-chart.5a6eee3820755551d786c9acfb19e028.svg']"
    DATE = "//strong[text()='Date']"
    ADD_ANOTHER_MEASURES_BTN = "//span[text()='Add another Measures(Numeric)']"
    COUNT_OF_LIKE_REACTIONS = "//strong[contains(text(), 'Count of like reactions')]"
    SELECT_ATTRIBUTE = "(//span[text()='Click to select attribute'])[1]"
    ATTRIBUTE_CITY = "//strong[text()='City']"
    ATTRIBUTE_COUNTRY = "//strong[text()='Country']"
    SAVE_WIDGET_BTN = "//button[.//span[text()='Save Widget'] or contains(., 'Save Widget')]"
    ADD_TAG_INPUT = "//input[@placeholder='Add a tag' or @aria-label='Add a tag']"
    WIDGET_NAME_INPUT = "//input[@placeholder='Enter Widget Name' or @aria-label='Enter Widget Name']"
    SAVE_BTN = "//button[.//span[text()='Save'] and not(contains(., 'Save Widget'))]"
    SUCCESS_WIDGET_SAVED = "//*[contains(text(), 'Widget saved successfully')]"
    SEARCH_INPUT = "(//input[@placeholder='Search'])[2]"
    SEARCH_ICON = "//img[@name='search' or @alt='search' or @title='search']"
    MORE_ICON = "//img[@src='/static/media/Dot_icon.d2a8952bba928acc82883022429bedd6.svg']"
    EDIT_WIDGET_TEXT = "//div[text()='Edit Widget']"
    DONUT = "//img[@src='/static/media/doughnut-chart.a4a79fc499e98cf2fd856407971c80a2.svg']"
    BRAND_NAME_TEXT = "//strong[contains(text(), 'Brand Name')]"
    VIEW_ICON = "//img[@name='View Icon' or contains(@alt,'View')]"
    DUPLICATE_WIDGET_BTN = "//button[contains(., 'Duplicate Widget') or contains(., 'Duplicate &')]"
    DELETE_WIDGET_TEXT = "//div[text()='Delete Widget']"
    DELETE_BTN = "//button[.//span[text()='Delete'] or contains(., 'Delete')]"
    WIDGET_DELETED_SUCCESS = "//*[contains(text(), 'Widget deleted successfully') or contains(text(), 'Widget deleted successfully!')]"
    
    # Save Dashboard elements
    SAVE_DASHBOARD_BTN = "//button[contains(., 'Save Dashboard')]"
    DASHBOARD_SUCCESS_MESSAGE = "//*[contains(text(), 'Dashboard updated successfully')]"
    DISMISS_BTN = "//button[contains(., 'Dismiss')]"
    MORE = "//div[.//div[normalize-space()='Mentions Count']]//i[contains(@class,'fa-ellipsis-h')]"
    SAVE_AS = "//span[text()='Save As']"
    
    # Dashboard navigation and creation
    ALL_DASHBOARDS_BUTTON = "//span[contains(., 'All Dashboards')]"
    CREATE_NEW_DASHBOARD_BUTTON = "//button[contains(., 'Create New Dashboard')]"
    DASHBOARD_NAME_INPUT = "//input[@id='outlined-required' or @placeholder='Dashboard Name']"
    CLICK_TO_ADD_WIDGET = "//div[contains(text(), 'Click to add widget')]"
    ADD_WIDGET_BUTTON = "//button[contains(., 'Add Widget')]"
    DASHBOARD_CREATED_SUCCESS = "//*[contains(text(), 'Dashboard created successfully')]"
    
    # Dashboard editing
    EDIT_DASHBOARD_TEXT = "//div[text()='Edit']"
    ADD_SECTION_TEXT = "//span[text()='+ Add Section']"
    ADD_SECTION_BUTTON = "//button[contains(., 'Add Section')]"
    SECTION_NAME_INPUT = "//div[@role='dialog']//input[@type='text']"
    SAVE_SECTION_BUTTON = "//button[contains(., 'Save')]"
    SAVE_CHANGES_BUTTON = "//button[contains(., 'Save Changes')]"
    CLOSE_TAB = '//img[@src="/static/media/Close.88c417f2e086b1e320ff4629175cfc49.svg"]'

    # Dashboard search and actions
    DASHBOARD_SEARCH_INPUT = "(//input[@placeholder='Search'])[2]"
    DASHBOARD_SEARCH_ICON = "//img[@alt='search' or @name='search']"
    DASHBOARD_MORE_ICON = "//img[@alt='more' or @name='more']"
    DUPLICATE_DASHBOARD_TEXT = "//div[text()='Duplicate']"
    DUPLICATE_DASHBOARD_INPUT = "//div[@role='dialog']//input[@type='text']"
    DUPLICATE_SAVE_BUTTON = "//button[contains(., 'SAVE')]"
    DASHBOARD_DUPLICATED_SUCCESS = "//*[contains(text(), 'Dashboard duplicated')]"
    DELETE_DASHBOARD_TEXT = "//span[text()='Delete']"
    DELETE_DASHBOARD_YES_BUTTON = "//button[contains(., 'YES')]"
    DASHBOARD_DELETED_SUCCESS = "//*[contains(text(), 'Dashboard deleted successfully')]"
    
    # Download PDF/PPT elements
    DOWNLOAD_PDF_BUTTON = "//span[text()='Download PDF']"
    PDF_CONFIRMATION_MESSAGE = "//*[contains(text(), 'You will receive the PDF')]"
    DOWNLOAD_PPT_BUTTON = "//span[text()='Download PPT']"
    DOWNLOAD_AS_NATIVE_BUTTON = "//div[text()='Download as Native']"
    NEXT_BUTTON = "//button[contains(., 'Next')]"
    DOWNLOAD_PPT_CONFIRM_BUTTON = "//button[contains(., 'Download PPT')]"
    PPT_GENERATING_MESSAGE = "//*[contains(text(), 'Generating your PPT report')]"
    PPT_DOWNLOADED_MESSAGE = "//*[contains(text(), 'PPT report downloaded')]"
    
    # Share Link elements
    SHARE_BUTTON = "//span[text()='Share']"
    OPEN_LINK_GENERATOR_BUTTON = "//button[contains(., 'Open Link Generator')]"
    ALLOW_BRAND_SWITCHING_CHECKBOX = "//span[text()='Allow Brand Switching']"
    OPEN_FOR_ANYONE_RADIO = "//span[text()='Open for anyone']"
    GENERATE_SHAREABLE_LINK_BUTTON = "//button[contains(., 'Generate Shareable Link')]"
    COPY_LINK_BUTTON = "//button[contains(., 'Copy')]"
    DEEP_DIVE_TAB = "//div[contains(@class, 'deep_dive_tab')]//div[contains(@class, 'd-flex')]"

    #Schedule Report elements
    SCHEDULE_REPORT_BUTTON = "//*[text()='Schedule Report']"
    SCHEDULE_REPORT_NEXT_BUTTON = "//button[contains(., 'Next')]"
    SCHEDULE_REPORT_RADIO = "//input[@type='radio' and @value='schedule'] | //label[contains(., 'Schedule Report')]"
    FREQUENCY_DIV = "//span[text()='Hourly']"
    FREQUENCY_MONTHLY_OPTION = "//div[text()='Monthly']"
    PERIOD_SELECTOR = "//label[contains(text(),'Data Duration')]/preceding-sibling::div[contains(@class,'ant-select')]"
    LAST_MONTH_OPTION = "//*[text()='Last month']"
    DAY_SELECTOR = "//label[contains(text(),'Schedule Day')]/preceding-sibling::div[contains(@class,'ant-select')]"
    SECOND_DAY_OPTION = "//*[text()='2nd of every month']"
    TIME_SELECTOR = "//label[contains(text(),'Schedule Time')]/preceding-sibling::div[contains(@class,'ant-select')]"
    TIME_12_30 = "//*[contains(text(),'12:30 AM') or @title='12:30 AM']"
    PREVIEW_BUTTON = "//button[contains(., 'Preview')]"
    LISTENING_OVERVIEW_TEXT = "//div[@id='pdfconvert']//*[text()='Listening Overview'] | //*[contains(text(), 'Listening Overview')]"
    SCHEDULE_REPORT_FINAL_BUTTON = "//button[contains(., 'Schedule Report')]"
    REPORT_SCHEDULED_SUCCESS = "//*[contains(text(), 'Report scheduled successfully')]"

    # Filter elements
    CATEGORY_LOCATION_BUTTON = "//span[text()='Category & Location']"
    BRAND_EXPAND = "(//span[contains(@class,'accordionArrow')])[1]"
    ALL_CHECKBOX = "(//span[text()='All'])[2]/parent::label"
    DONE_BUTTON = "//button[contains(., 'Done') or contains(., 'DONE') or .//span[contains(text(), 'Done')] or @aria-label='Done']"
    HEADER_FILTER_BUTTON = "//img[@alt='Header Filter']"
    FILTER_SEARCH_INPUT = "//input[@placeholder='Search' or @name='Search']"
    CATEGORY_ARROW_BUTTON = "//button[contains(., 'arrow') and contains(., 'Category')] | //button[contains(., 'Category')]//mat-icon[contains(text(), 'arrow')] | //*[contains(text(), 'Category')]//ancestor::button"
    CATEGORY_SEARCH_INPUT = "//input[@placeholder='Search Category' or contains(@placeholder, 'Search')]"
    INCLUDE_CHECKBOX = "//input[@type='checkbox' and contains(@name, 'Include')] | //span[contains(text(), 'Include')]//input[@type='checkbox'] | //*[contains(text(), 'Include')]//ancestor::label//input[@type='checkbox']"
    APPLY_BUTTON = "//button[contains(., 'Apply')]"
    BRAND_MENTIONS_TEXT = "//*[@aria-label='Listening Overview' or contains(@class, 'Listening Overview')]//text()[contains(., 'Brand Mentions')]/ancestor::*[1] | //text()[normalize-space()='Brand Mentions']/ancestor::*[self::div or self::span or self::button][1]"

    # Twitter Widget elements
    TWITTER_CHANNEL = "(//span[text()='Twitter'])[2]"
    CHANNEL_TWITTER_WIDGET = "//span[text()='Channel']"
    MENTIONS_BUTTON = "//button[contains(., 'Mentions') or @name='Mentions' or @aria-label='Mentions']"
    WORD_CLOUD_BUTTON = "//button[contains(., 'Word Cloud') or @name='Word Cloud' or @aria-label='Word Cloud']"
    CATEGORY_BUTTON = "//button[contains(., 'Category') or @name='Category' or @aria-label='Category']"
    INFLUENCERS_BUTTON = "//button[contains(., 'Influencers') or @name='Influencers' or @aria-label='Influencers']"
    SOURCE_POST_BUTTON = "//button[contains(., 'Source of Post') or @name='Source of Post' or @aria-label='Source of Post']"
    LOCATION_PROFILES_BUTTON = "//button[contains(., 'Location Profiles') or @name='Location Profiles' or @aria-label='Location Profiles']"
