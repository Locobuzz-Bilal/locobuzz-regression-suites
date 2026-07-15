# Quick Start Guide - Single Store Manage Brands

## Fastest Way to Run

### Option 1: Use the Batch File (Easiest)
```bash
RUN_MANAGE_BRANDS_TEST.bat
```
Then select option 3 or 4 from the menu.

### Option 2: Direct Python Execution
```bash
python "tests/selenium/Single Store/Manage Brands/test_manage_brand.py"
```

### Option 3: Simple Standalone Script
```bash
python test_cx_login_simple.py
```

### Option 4: Pytest with Output
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -v -s
```

## What Each Test Does

### test_manage_brand_single_selection
- Logs into CX
- Selects "Twitter Auto" brand
- Verifies dashboard loads

### test_manage_brand_all_selection
- Logs into CX
- Selects all brands
- Verifies dashboard loads

## Default Settings
- **Username:** xagent
- **Password:** Locobuzz@123
- **Browser:** Chrome (visible)
- **URL:** https://cx.locobuzz.com/login

## Common Commands

Run single test:
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py::test_manage_brand_single_selection" -v -s
```

Run with screenshots on failure:
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -v --tb=short
```

Run in headless mode (edit script first):
```python
# Change in test_manage_brand.py:
driver = locobuzzLogin("xagent", "Locobuzz@123", headless=True)
```

## Troubleshooting

**Import errors?**
- Run from project root directory

**Brand selection fails?**
- Check brand names are correct
- Verify brand availability for user
- Look at screenshot in `tests/screenshots/single_store/manage_brands/`

**Element not found?**
- CX UI may have changed
- Check `elements/login_page.py` for updated locators

## File Structure
```
tests/selenium/Single Store/
└── Manage Brands/
    ├── __init__.py
    ├── test_manage_brand.py     # Main test script
    ├── README.md                 # Full documentation
    └── QUICK_START.md           # This file
```

## Next Steps
1. Run the test to verify it works
2. Customize credentials if needed
3. Add more test cases as required
4. Integrate with CI/CD pipeline
