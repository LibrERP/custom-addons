"""
Disable openerp related imports in utils.py before running tests
"""

from utils import BaseImport


def test_conversion():
    to_str = BaseImport.to_string

    values = {
        '234': '234',
        '2,23': '2.23',
        '2.234,78': '2234.78',
        '2.33': '2.33',
        '3,678.98': '3678.98',
        '0.98': '0.98',
        '0,98': '0.98',
        '0,085': '0.085',
        '00,085': '00,085',
        '00.085': '00.085',
        '02.085': '02.085',
        '02,085': '02,085',
        '.': '.',
        ',': ',',
        'L00df': 'L00df'
    }

    for value, result in values.items():
        assert to_str(value) == result, "{} is not {}".format(value, result)


if __name__ == '__main__':
    test_conversion()