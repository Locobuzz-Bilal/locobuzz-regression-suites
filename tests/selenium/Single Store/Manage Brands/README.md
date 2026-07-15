# Single Store - Manage Brands Module

## Overview
This module contains automated test scripts for brand management functionality in the CX platform, specific to Single Store testing.

## Location
```
tests/selenium/Single Store/Manage Brands/
```

## Files
- `test_manage_brand.py` - Main test script with brand management test cases
- `__init__.py` - Python package initialization
- `README.md` - This documentation file

## Test Cases

### 1. test_manage_brand_single_selection()
Complete brand management flow with single brand selection (Twitter Auto).

**Steps:**
1. Navigate to CX login page
2. Enter username and continue
3. Enter password and login
4. Select Twitter Auto brand
5. Submit and verify dashboard access

### 2. test_manage_brand_all_selection()
Brand management flow with all brands selection.

**Steps:**
1. Login to CX platform
2. Select all brands
3. Submit and verify access

## Usage

### Run all tests in this module
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -v
```

### Run specific test
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py::test_manage_brand_single_selection" -v -s
```

### Run with Allure reporting
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Direct execution
```bash
python "tests/selenium/Single Store/Manage Brands/test_manage_brand.py"
```

## Configuration

### Default Credentials
- Username: `xagent`
- Password: `Locobuzz@123`

### Browser Mode
- Default: Visible browser (headless=False)
- To enable headless mode, modify the script:
  ```python
  driver = locobuzzLogin("xagent", "Locobuzz@123", headless=True)
  ```

## Screenshots
Failed test screenshots are saved to:
```
tests/screenshots/single_store/manage_brands/
```

Format: `{test_name}_{timestamp}.png`

## Dependencies
- selenium
- pytest
- allure-pytest
- locobuzz_login module
- elements.login_page module

## Integration
This module integrates with:
- `locobuzz_login/CX_login.py` - Core login helper function
- `elements/login_page.py` - Element locators for login page
- Project root imports via sys.path manipulation

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running from the project root:
```bash
cd /path/to/project/root
python "tests/selenium/Single Store/Manage Brands/test_manage_brand.py"
```

### Element Not Found
If elements aren't found:
1. Check if CX UI has changed
2. Update locators in `elements/login_page.py`
3. Increase wait times in the script

### Brand Selection Failures
1. Verify brand names are correct
2. Check brand availability for the user
3. Review screenshot in screenshots directory
4. Check network connectivity

## Allure Reporting
Tests are tagged with:
- Feature: `Single Store - Manage Brands`
- Stories: `Brand Selection Flow`, `Brand Selection - All Brands`

## Next Steps
- Add brand switching tests
- Add brand filtering tests
- Add multi-brand management scenarios
- Add brand validation tests
