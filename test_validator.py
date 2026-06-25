from mobile_validator import MobileValidator   # ← Now works cleanly!

class TestIndianNumbers:

    def setup_method(self):
        self.validator = MobileValidator()

    def test_valid_airtel_number(self):
        result = self.validator.validate("9876543210", "IN")
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

    def test_suspicious_repeated_digits(self):
        result = self.validator.validate("9999999999", "IN")
        assert result['valid'] is True
        assert result['risk_level'] == 'HIGH'
        assert result['is_safe'] is False

    def test_invalid_number_too_short(self):
        result = self.validator.validate("12345", "IN")
        assert result['valid'] is False

    def test_invalid_starts_with_wrong_digit(self):
        result = self.validator.validate("5123456789", "IN")
        assert result['valid'] is False


class TestUSNumbers:

    def setup_method(self):
        self.validator = MobileValidator()

    def test_valid_us_number(self):
        result = self.validator.validate("+12025550199", "US")
        assert result['valid'] is True
        assert result['network'] == 'AT&T'

    def test_invalid_us_number(self):
        result = self.validator.validate("0000000000", "US")
        assert result['valid'] is False


class TestUKNumbers:

    def setup_method(self):
        self.validator = MobileValidator()

    def test_valid_uk_vodafone(self):
        result = self.validator.validate("+447700900123", "GB")
        assert result['valid'] is True
        assert result['network'] == 'Vodafone'

    def test_invalid_uk_number(self):
        result = self.validator.validate("1234567890", "GB")
        assert result['valid'] is False


class TestUnsupportedCountry:

    def setup_method(self):
        self.validator = MobileValidator()

    def test_unsupported_country(self):
        result = self.validator.validate("9876543210", "XY")
        assert result['valid'] is False
        assert 'not supported' in result['error']