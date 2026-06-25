"""
Mobile Number Validator
Validates mobile numbers, detects risks, and identifies network providers
"""

import re
from typing import Dict, Optional


class MobileValidator:
    """Validates mobile numbers globally"""

    COUNTRY_PATTERNS = {
        'IN': {  # India
            'pattern': r'^(?:91)?[6-9]\d{9}$',
            'country_name': 'India',
            'country_code': '91',
            # Key: starting digit(s) of the 10-digit national number
            # Based on TRAI number allocation blocks
            'networks': {
                '6': 'Jio',
                '70': 'Airtel',
                '71': 'Airtel',
                '72': 'Airtel',
                '73': 'Airtel',
                '74': 'Airtel',
                '75': 'Airtel',
                '76': 'Airtel',
                '77': 'Vodafone-Idea',
                '78': 'Vodafone-Idea',
                '79': 'Vodafone-Idea',
                '80': 'Jio',
                '81': 'Jio',
                '82': 'Jio',
                '83': 'Jio',
                '84': 'BSNL',
                '85': 'BSNL',
                '86': 'Vodafone-Idea',
                '87': 'Airtel',
                '88': 'Vodafone-Idea',
                '89': 'Jio',
                '90': 'Airtel',
                '91': 'Airtel',
                '92': 'Airtel',
                '93': 'Vodafone-Idea',
                '94': 'Vodafone-Idea',
                '95': 'Vodafone-Idea',
                '96': 'Airtel',
                '97': 'BSNL',
                '98': 'Airtel',
                '99': 'Airtel',
            }
        },
        'US': {  # United States
            'pattern': r'^(?:\+?1)?[2-9]\d{2}[2-9](?!11)\d{6}$',
            'country_name': 'United States',
            'country_code': '1',
            # US carriers are identified by area code blocks
            'networks': {
                '201': 'Verizon',
                '202': 'AT&T',
                '203': 'AT&T',
                '205': 'AT&T',
                '206': 'T-Mobile',
                '210': 'AT&T',
                '212': 'Verizon',
                '213': 'AT&T',
            }
        },
        'GB': {  # United Kingdom
            'pattern': r'^(?:\+?44)?7\d{9}$',
            'country_name': 'United Kingdom',
            'country_code': '44',
            # UK mobile numbers all start with 07xxx nationally
            # Ofcom allocation by first 4 digits of national number
            'networks': {
                '7400': 'BT',
                '7500': 'O2',
                '7600': 'Vodafone',
                '7700': 'Vodafone',
                '7800': 'O2',
                '7900': 'Vodafone',
                '771': 'Vodafone',
                '772': 'Vodafone',
                '773': 'Vodafone',
                '774': 'Vodafone',
                '775': 'Vodafone',
                '776': 'Vodafone',
                '777': 'Vodafone',
                '778': 'O2',
                '779': 'O2',
                '780': 'EE',
                '781': 'EE',
                '782': 'EE',
                '783': 'EE',
                '784': 'EE',
                '785': 'O2',
                '786': 'O2',
                '787': 'O2',
                '788': 'O2',
                '789': 'O2',
                '790': 'T-Mobile',
                '791': 'T-Mobile',
                '792': 'T-Mobile',
                '793': 'T-Mobile',
                '794': 'T-Mobile',
                '795': 'T-Mobile',
                '796': 'T-Mobile',
                '797': 'EE',
                '798': 'EE',
                '799': 'EE',
            }
        },
    }

    def validate(self, mobile_number: str, country_code: str = 'IN') -> Dict:
        """Validate mobile number"""
        cleaned = re.sub(r'[^\d+]', '', str(mobile_number))
        # Strip leading + for digit-only matching
        cleaned_digits = cleaned.lstrip('+')

        if country_code not in self.COUNTRY_PATTERNS:
            return {'valid': False, 'error': f'Country {country_code} not supported'}

        info = self.COUNTRY_PATTERNS[country_code]

        if not re.match(info['pattern'], cleaned_digits):
            return {
                'valid': False,
                'error': f'Invalid format for {info["country_name"]}'
            }

        national_number = self._extract_national_number(cleaned_digits, country_code)
        risk = self._check_risk(national_number)
        network = self._get_network(national_number, country_code)

        return {
            'valid': True,
            'number': cleaned_digits,
            'national_number': national_number,
            'country': info['country_name'],
            'network': network,
            'risk_level': risk['level'],
            'is_safe': risk['is_safe'],
        }

    def _extract_national_number(self, digits: str, country_code: str) -> str:
        """
        Strip country dialing code to get the national subscriber number.
        Always returns the last N digits relevant to each country.
        """
        if country_code == 'IN':
            # Indian national numbers are always 10 digits
            return digits[-10:]

        elif country_code == 'US':
            # US national numbers are always 10 digits
            return digits[-10:]

        elif country_code == 'GB':
            # UK mobile national numbers are 10 digits starting with 7
            return digits[-10:]

        return digits

    def _check_risk(self, number: str) -> Dict:
        """
        Check for suspicious patterns in the national number.

        HIGH risk conditions:
        - All digits are identical  (e.g. 9999999999)
        - Number is a sequential run (e.g. 1234567890)
        """
        # All digits identical
        if len(set(number)) == 1:
            return {'level': 'HIGH', 'is_safe': False, 'reason': 'All digits identical'}

        # Sequential ascending or descending digits
        if number in '0123456789' * 2 or number in '9876543210' * 2:
            return {'level': 'HIGH', 'is_safe': False, 'reason': 'Sequential pattern'}

        return {'level': 'LOW', 'is_safe': True, 'reason': 'No suspicious pattern'}

    def _get_network(self, national_number: str, country: str) -> str:
        """
        Identify network provider from the national number.

        Matching strategy:
        - Longer prefixes are checked first (most-specific wins)
        - Falls back to shorter prefixes, then 'Unknown'
        """
        networks = self.COUNTRY_PATTERNS.get(country, {}).get('networks', {})

        if not networks:
            return 'Unknown'

        # Sort keys longest-first so more specific prefixes take priority
        sorted_prefixes = sorted(networks.keys(), key=len, reverse=True)

        for prefix in sorted_prefixes:
            if national_number.startswith(prefix):
                return networks[prefix]

        return 'Unknown'


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    validator = MobileValidator()

    print("=" * 60)
    print("MOBILE NUMBER VALIDATOR")
    print("=" * 60)

    test_cases = [
        # (number,        country, expected network)
        ("9876543210",   "IN",   "Airtel"),
        ("7012345678",   "IN",   "Airtel"),
        ("8012345678",   "IN",   "Jio"),
        ("6012345678",   "IN",   "Jio"),
        ("9999999999",   "IN",   "HIGH risk"),
        ("+12025550199", "US",   "AT&T"),
        ("+447700900123","GB",   "Vodafone"),
    ]

    for number, country, expected in test_cases:
        result = validator.validate(number, country)
        print(f"\nNumber  : {number}")
        print(f"Country : {country}  |  Expected network: {expected}")

        if result['valid']:
            safe_str = 'Yes ✓' if result['is_safe'] else 'No ✗'
            print(f"  ✓ VALID")
            print(f"  National : {result['national_number']}")
            print(f"  Network  : {result['network']}")
            print(f"  Risk     : {result['risk_level']}")
            print(f"  Safe     : {safe_str}")
        else:
            print(f"  ✗ INVALID — {result['error']}")