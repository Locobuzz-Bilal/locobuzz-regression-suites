"""Quick test runner for individual tests"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the test module
from test_manage_brand import (
    test_manage_brand,
    test_create_brand_with_mandatory_fields,
    test_validation_without_brand_name,
    test_validation_without_country,
    test_validation_without_ai_friendly_name,
    test_select_brand_color,
    test_view_other_brand_colors,
    test_upload_valid_logo,
    test_upload_unsupported_logo_format,
    test_upload_logo_exceeding_size_limit
)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("MANAGE BRANDS TEST RUNNER")
    print("="*60)
    print("\nAvailable Tests:")
    print("1. test_manage_brand - Navigation test")
    print("2. test_create_brand_with_mandatory_fields - Fill fields")
    print("3. test_validation_without_brand_name - Validation test")
    print("4. test_validation_without_country - Validation test")
    print("5. test_validation_without_ai_friendly_name - Validation test")
    print("6. test_select_brand_color - Color selection")
    print("7. test_view_other_brand_colors - View colors")
    print("8. test_upload_valid_logo - Upload valid logo")
    print("9. test_upload_unsupported_logo_format - Upload invalid format")
    print("10. test_upload_logo_exceeding_size_limit - Upload large file")
    print("0. Run ALL tests")
    
    choice = input("\nEnter test number to run (0-10): ").strip()
    
    tests = {
        "1": ("Navigation Test", test_manage_brand),
        "2": ("Fill Mandatory Fields", test_create_brand_with_mandatory_fields),
        "3": ("Validation - Brand Name", test_validation_without_brand_name),
        "4": ("Validation - Country", test_validation_without_country),
        "5": ("Validation - AI Friendly Name", test_validation_without_ai_friendly_name),
        "6": ("Select Brand Color", test_select_brand_color),
        "7": ("View Other Colors", test_view_other_brand_colors),
        "8": ("Upload Valid Logo", test_upload_valid_logo),
        "9": ("Upload Invalid Format", test_upload_unsupported_logo_format),
        "10": ("Upload Large File", test_upload_logo_exceeding_size_limit),
    }
    
    if choice == "0":
        print("\n🚀 Running ALL tests...\n")
        for name, test_func in tests.values():
            print(f"\n{'='*60}")
            print(f"Running: {name}")
            print('='*60)
            try:
                test_func()
                print(f"✅ {name} - PASSED")
            except Exception as e:
                print(f"❌ {name} - FAILED: {e}")
    elif choice in tests:
        name, test_func = tests[choice]
        print(f"\n🚀 Running: {name}\n")
        test_func()
    else:
        print("❌ Invalid choice!")
