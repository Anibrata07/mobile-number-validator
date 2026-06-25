# 📱 Mobile Number Validator

Validates mobile numbers globally, detects suspicious patterns,
and identifies network providers.

## Features
- ✅ Validates numbers for India, US, and UK
- 🔍 Identifies network provider (Jio, Airtel, AT&T, etc.)
- ⚠️ Detects high-risk/suspicious number patterns
- 🌍 Easily extendable to more countries

## Supported Countries
| Code | Country        | Networks Covered              |
|------|----------------|-------------------------------|
| IN   | India          | Jio, Airtel, Vodafone-Idea, BSNL |
| US   | United States  | AT&T, Verizon, T-Mobile       |
| GB   | United Kingdom | Vodafone, O2, EE, T-Mobile    |

## Installation
\```bash
git clone https://github.com/Anibrata07/mobile-number-validator.git
cd mobile-number-validator
\```

## Usage
\```python

validator = MobileValidator()

result = validator.validate("9876543210", "IN")
print(result)
# {
#   'valid': True,
#   'number': '9876543210',
#   'country': 'India',
#   'network': 'Airtel',
#   'risk_level': 'LOW',
#   'is_safe': True
# }
\```

## Running Tests
\```
python test_numbers
\```
