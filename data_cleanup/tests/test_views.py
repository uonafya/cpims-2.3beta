from unittest import TestCase

from data_cleanup.views import validate_age


class TestAgeValidation(TestCase):
    def test_age_provided_is_okay(self):
        """An integer is acceptable"""
        self.assertTrue(validate_age(10))

    def test_age_provided_is_not_valid(self):
        """Anything which is not an integer is not acceptable."""
        self.assertFalse(validate_age('not_a_number'))

    def test_age_range_provided_is_okay(self):
        """Integer ranges are acceptable"""
        self.assertTrue(validate_age('10-20'))

    def test_age_range_provided_is_not_valid(self):
        """Non integer ranges are not acceptable."""
        self.assertFalse(validate_age('a-z'))

    def test_age_range_provided_with_spaces_is_okay(self):
        """Ranges with spaces in between are acceptable."""
        self.assertTrue(validate_age('10 - 100'))
