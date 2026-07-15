# Manage Brands - Test Coverage Summary

## 📋 Test Scenarios Covered

### ✅ Navigation Tests (1)
1. **test_manage_brand()** - Navigate to Manage Brands via Account Settings
   - Login → Profile Menu → Account Settings → Search "manage brand" → Click Manage Brands → Click Add Brand

### ✅ Field Validation Tests (3)
2. **test_validation_without_brand_name()** - Try saving without Brand Name
3. **test_validation_without_country()** - Try saving without Country selection
4. **test_validation_without_ai_friendly_name()** - Try saving without AI Friendly Name

### ✅ Logo Upload Tests (3)
5. **test_upload_valid_logo()** - Upload valid logo (jpg/png within size limit)
6. **test_upload_unsupported_logo_format()** - Upload unsupported format (.txt file)
7. **test_upload_logo_exceeding_size_limit()** - Upload logo exceeding size limit

### ✅ Brand Color Tests (2)
8. **test_select_brand_color()** - Select a brand color from default palette
9. **test_view_other_brand_colors()** - Click "View other brand colors" option

### ℹ️ Field Fill Test (Not Saving)
10. **test_create_brand_with_mandatory_fields()** - Fill all mandatory fields without saving
    - Brand Name, Country, AI Friendly Name
    - Does NOT save to avoid database pollution

## 📊 Total Tests: 10

## 🎯 Test Strategy
- Focus on validation and UI interactions
- Avoid actual brand creation (no delete functionality available)
- Test images are auto-generated in `tests/test_data/`

## 🚀 How to Run

### Run All Tests
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -v -s
```

### Run Specific Test
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py::test_manage_brand" -v -s
```

### Run Only Validation Tests
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -k "validation" -v -s
```

### Run Only Logo Tests
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -k "upload" -v -s
```

### Run Only Color Tests
```bash
pytest "tests/selenium/Single Store/Manage Brands/test_manage_brand.py" -k "color" -v -s
```

## 📦 Dependencies
- Pillow (PIL) - For test image generation
- Install: `pip install Pillow==10.2.0`

## 📸 Screenshots
Failure screenshots saved to: `tests/screenshots/single_store/manage_brands/`

## 🔑 Test Credentials
- Username: `bilalSS`
- Password: `Locobuzz@123`
- Environment: Staging (https://unification-staging.locobuzz.com)

## ⚠️ Important Notes
1. Tests do NOT save actual brands (to avoid database pollution)
2. Test images are auto-created in `tests/test_data/` folder
3. Each test runs independently with fresh login
4. Browser stays open after test for manual verification (Press Enter to close)
