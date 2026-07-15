# 🚀 Run Me First - Manage Brands Test

## Quickest Way to Test

### Option 1: Direct Python (Recommended for First Run)
```bash
python "tests/selenium/Single Store/Manage Brands/test_manage_brand.py"
```

### Option 2: Batch File Menu
```bash
RUN_MANAGE_BRANDS_TEST.bat
```
Then choose option 3 or 4

### Option 3: Pytest
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -v -s
```

## What You'll See

The browser will:
1. ✅ Open Chrome
2. ✅ Navigate to CX login
3. ✅ Enter username
4. ✅ Enter password
5. ✅ Select brand (Twitter Auto)
6. ✅ Submit and verify dashboard

## Default Credentials
- Username: `xagent`
- Password: `Locobuzz@123`

## Test Functions Available

1. **test_manage_brand_single_selection()** - Select single brand
2. **test_manage_brand_all_selection()** - Select all brands

## Need Help?
- Check `QUICK_START.md` for more options
- Check `README.md` for full documentation
- Screenshots saved to: `tests/screenshots/single_store/manage_brands/`

## That's It! 🎉
Just run the command and watch the magic happen!
