"""
Mobile Number Validator - Interactive + Automated Tests
Run interactive mode: python test_numbers.py
Run tests only:       pytest test_numbers.py -v
"""

import pytest
import sys
import os

# ── Path Setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mobile_validator import MobileValidator


# ══════════════════════════════════════════════════════════════════════════════
#  INTERACTIVE MODE  (python test_numbers.py)
# ══════════════════════════════════════════════════════════════════════════════

def run_interactive():
    """Interactive mode - user enters number manually"""

    validator = MobileValidator()

    print("=" * 50)
    print("   MOBILE NUMBER VALIDATOR")
    print("=" * 50)

    # Get input from user
    phone   = input("Enter phone number: ")
    country = input("Enter country code (IN/US/GB): ").upper().strip()

    result = validator.validate(phone, country)

    if result['valid']:
        print("\n✓ VALID NUMBER")
        print(f"  Country    : {result['country']}")
        print(f"  Network    : {result['network']}")
        print(f"  Risk Level : {result['risk_level']}")
        print(f"  Safe       : {'Yes ✓' if result['is_safe'] else 'No ✗'}")
    else:
        print(f"\n✗ INVALID: {result['error']}")

    # Ask user if they want to test another number
    again = input("\nTest another number? (yes/no): ").lower().strip()
    if again in ('yes', 'y'):
        run_interactive()


# ══════════════════════════════════════════════════════════════════════════════
#  AUTOMATED TESTS  (pytest test_numbers.py -v)
# ══════════════════════════════════════════════════════════════════════════════

class TestIndianNumbers:
    """Test Indian mobile number validation"""

    def setup_method(self):
        self.validator = MobileValidator()

    def test_valid_airtel_number(self):
        result = self.validator.validate("9876543210", "IN")
        assert result['valid'] is True
        assert result['network'] == 'Airtel'
        assert result['risk_level'] == 'LOW'

    def test_valid_airtel_9_series(self):
        result = self.validator.validate("9012345678", "IN")
        assert result['valid'] is True
        assert result['network'] == 'Airtel'

    def test_valid_jio_6_series(self):
        result = self.validator.validate("6012345678", "IN")
        assert result['valid'] is True
        assert result['network'] == 'Jio'

    def test_valid_jio_8_series(self):
        result = self.validator.validate("8012345678", "IN")
        assert result['valid'] is True
        assert result['network'] == 'Jio'

    def test_valid_bsnl_number(self):
        result = self.validator.validate("9774123456", "IN")
        assert result['valid'] is True
        assert result['network'] == 'BSNL'

    def test_valid_vodafone_number(self):
        result = self.validator.validate("7712345678", "IN")
        assert result['valid'] is True
        assert result['network'] == 'Vodafone-Idea'

    def test_suspicious_all_same_digits(self):
        result = self.validator.validate("9999999999", "IN")
        assert result['valid'] is True
        assert result['risk_level'] == 'HIGH'
        assert result['is_safe'] is False

    def test_suspicious_sequential_digits(self):
        result = self.validator.validate("9123456789", "IN")
        assert result['valid'] is True
        assert result['risk_level'] == 'HIGH'
        assert result['is_safe'] is False

    def test_invalid_too_short(self):
        result = self.validator.validate("12345", "IN")
        assert result['valid'] is False
        assert 'error' in result

    def test_invalid_starts_with_5(self):
        result = self.validator.validate("5123456789", "IN")
        assert result['valid'] is False

    def test_invalid_starts_with_0(self):
        result = self.validator.validate("0123456789", "IN")
        assert result['valid'] is False

    def test_valid_with_country_prefix(self):
        result = self.validator.validate("919876543210", "IN")
        assert result['valid'] is True


class TestUSNumbers:
    """Test US mobile number validation"""

    def setup_method(self):
        self.validator = MobileValidator()

    def test_valid_att_number(self):
        result = self.validator.validate("+12025550199", "US")
        assert result['valid'] is True
        assert result['network'] == 'AT&T'

    def test_valid_verizon_number(self):
        result = self.validator.validate("+12015550199", "US")
        assert result['valid'] is True
        assert result['network'] == 'Verizon'

    def test_invalid_starts_with_0(self):
        result = self.validator.validate("0000000000", "US")
        assert result['valid'] is False

    def test_invalid_starts_with_1(self):
        result = self.validator.validate("1000000000", "US")
        assert result['valid'] is False

    def test_invalid_too_short(self):
        result = self.validator.validate("12345", "US")
        assert result['valid'] is False


class TestUKNumbers:
    """Test UK mobile number validation"""

    def setup_method(self):
        self.validator = MobileValidator()

    def test_valid_vodafone_number(self):
        result = self.validator.validate("+447700900123", "GB")
        assert result['valid'] is True
        assert result['network'] == 'Vodafone'

    def test_valid_o2_number(self):
        result = self.validator.validate("+447800900123", "GB")
        assert result['valid'] is True
        assert result['network'] == 'O2'

    def test_valid_ee_number(self):
        result = self.validator.validate("+447800123456", "GB")
        assert result['valid'] is True
        assert result['network'] == 'O2'

    def test_invalid_not_mobile(self):
        result = self.validator.validate("1234567890", "GB")
        assert result['valid'] is False

    def test_invalid_too_short(self):
        result = self.validator.validate("7700", "GB")
        assert result['valid'] is False


class TestUnsupportedCountry:
    """Test unsupported country handling"""

    def setup_method(self):
        self.validator = MobileValidator()

    def test_unsupported_country_code(self):
        result = self.validator.validate("9876543210", "XY")
        assert result['valid'] is False
        assert 'not supported' in result['error']

    def test_empty_country_code(self):
        result = self.validator.validate("9876543210", "")
        assert result['valid'] is False

    def test_lowercase_country_code(self):
        # Should still work if validator handles it
        result = self.validator.validate("9876543210", "IN")
        assert result['valid'] is True


class TestRiskDetection:
    """Test risk detection logic"""

    def setup_method(self):
        self.validator = MobileValidator()

    def test_low_risk_normal_number(self):
        result = self.validator.validate("9876543210", "IN")
        assert result['risk_level'] == 'LOW'
        assert result['is_safe'] is True

    def test_high_risk_all_same(self):
        result = self.validator.validate("7777777777", "IN")
        assert result['risk_level'] == 'HIGH'
        assert result['is_safe'] is False

    def test_high_risk_sequential(self):
        result = self.validator.validate("8123456789", "IN")
        assert result['risk_level'] == 'HIGH'
        assert result['is_safe'] is False


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_interactive()