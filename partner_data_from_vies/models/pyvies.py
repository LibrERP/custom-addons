#!/usr/bin/env python3

from requests import post as requests_post
from bs4 import BeautifulSoup as Soup
from re import match as re_match

NoneType = type(None)


class Vies:
    # ISO 3166-1 alpha-2 country codes.
    EU_COUNTRY_CODES = set([
        'AT',  # Austria.
        'BE',  # Belgium.
        'BG',  # Bulgaria.
        'CY',  # Cyprus.
        'CZ',  # Czech Republic.
        'DE',  # Germany.
        'DK',  # Denmark.
        'EE',  # Estonia.
        'ES',  # Spain.
        'FI',  # Finland.
        'FR',  # France.
        'GB',  # United Kingdom.
        'EL',  # Greece.
        'HR',  # Croatia.
        'HU',  # Hungary.
        'IE',  # Ireland.
        'IT',  # Italy.
        'LT',  # Lithuania.
        'LU',  # Luxembourg.
        'LV',  # Latvia.
        'MT',  # Malta.
        'NL',  # Netherlands.
        'PL',  # Poland.
        'PT',  # Portugal.
        'RO',  # Romania.
        'SE',  # Sweden.
        'SI',  # Slovenia.
        'SK',  # Slovakia.
    ])

    COUNTRY_CODE_ALIASES = {
        'GR': 'EL',
    }

    def request(self, vat_id: (str, NoneType), country_code: (str, NoneType) = '', bypass_ratelimit: bool = False):
        allowed_arg_types = (NoneType, str)
        vat_re = r'^([0-9A-Za-z]{2,12})$'
        country_code_re = r'^([A-Z]{2})$'

        if not isinstance(vat_id, allowed_arg_types):
            raise TypeError('vat_id should be either str, or NoneType, not %s' % type(vat_id))
        elif not isinstance(country_code, allowed_arg_types):
            raise TypeError('country_code should be either str, or NoneType, not %s') % type(country_code)

        country_code = country_code or ''
        country_code = country_code.upper()

        if country_code in self.COUNTRY_CODE_ALIASES:
            country_code = self.COUNTRY_CODE_ALIASES[country_code]

        vat_id = vat_id.lstrip().rstrip().upper() if vat_id else ''
        vat_id = ''.join([c for c in vat_id if c not in '\n\t -'])

        request = ViesRequest(vat_id, country_code)

        if len(vat_id) < 2:
            request.error = 'vat_id (%s) should be at least 2 characters long' % vat_id
        elif country_code and vat_id[:2] == country_code:
            vat_id = vat_id[2:]
        elif not country_code:
            country_code, vat_id = vat_id[:2], vat_id[2:]

        if request.error:
            request.is_valid = False
            return request

        if not re_match(vat_re, vat_id):
            request.error = "vat_id '%s' doesn't match the pattern '%s'" % (vat_id, vat_re)
        elif not re_match(country_code_re, country_code):
            request.error = "country_code '%s' doesn't match the pattern '%s'" % (country_code, country_code_re)
        elif country_code not in self.EU_COUNTRY_CODES:
            request.error = 'unsupported country code: "%s"' % country_code

        if request.error:
            request.is_valid = False
            return request

        request.country_code = country_code
        request.vat_id = vat_id
        request.post(bypass_ratelimit)

        return request


class ViesRequest:
    RATELIMIT_RESPONSE = 'MS_UNAVAILABLE'
    url = 'http://ec.europa.eu/taxation_customs/vies/services/checkVatService'

    def __init__(self, vat_id: str, country_code: str):
        self.timeout = 10
        self.vat_id = vat_id
        self.country_code = country_code
        self.is_valid = None
        self.company_name = None
        self.company_address = None
        self.data = None
        self.response = None
        self.error = None

    def __str__(self):
        if self.is_valid is None:
            validity = 'not validated'
        elif self.is_valid:
            validity = 'valid'
        else:
            validity = 'invalid'

        country_code = self.country_code or ''
        vat_id = self.vat_id or ''

        ret = 'VAT number "%s%s" (%s)' % (country_code, vat_id, validity)
        if self.error:
            ret += ', error: %s' % self.error

        return ret

    @property
    def pretty(self):
        if self.response:
            return self.soup.prettify()

    def save_error(self):
        error_attr = self.soup.find('faultstring')
        if error_attr:
            self.error = error_attr.text

    def get_tag_text(self, name: str, optional: bool = False):
        tag = self.soup.find(name)
        if not tag:
            if not optional:
                self.is_valid = False
                self.save_error()
            return None
        else:
            return tag.text

    def validate(self, bypass_ratelimit=False):
        self.soup = Soup(self.response.text, 'xml')
        self.is_valid = self.get_tag_text('valid') == 'true'

        if bypass_ratelimit and self.error == self.RATELIMIT_RESPONSE:
            self.error = None
            self.is_valid = True
            return  # we will not get the company name and address from ratelimited response anyway

        self.company_name = self.get_tag_text('name', optional=True)
        if self.company_name:
            self.company_name = self.company_name.replace('---', '') or None

        self.company_address = self.get_tag_text('address', optional=True)
        if self.company_address:
            self.company_address = self.company_address.replace('---', '') or None

    def post(self, bypass_ratelimit: bool = False):
        # bypass_ratelimit is a switch to bypass the 1 minute API ban after sending the same data twice
        # API returns valid=False correctly for invalid requests, even when ratelimited
        # The idea is to exploit this behaviour by first sending the invalid request for the same country,
        # making sure that server returned the correct valid=False response,
        # and then continuing to check the real VAT ID, considering ratelimit error as success

        headers = {'Content-type': 'text/xml'}

        xml_request = '' \
                      '<?xml version="1.0" encoding="UTF-8"?>' \
                      '<SOAP-ENV:Envelope ' \
                      'xmlns:ns0="urn:ec.europa.eu:taxud:vies:services:checkVat:types" ' \
                      'xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" ' \
                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
                      'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">' \
                      '<SOAP-ENV:Header/>' \
                      '<ns1:Body>' \
                      '<ns0:checkVat>' \
                      '<ns0:countryCode>%s</ns0:countryCode>' \
                      '<ns0:vatNumber>%s</ns0:vatNumber>' \
                      '</ns0:checkVat>' \
                      '</ns1:Body>' \
                      '</SOAP-ENV:Envelope>'

        self.data = xml_request % (self.country_code, self.vat_id)

        if bypass_ratelimit:
            data = xml_request % (self.country_code, '1337')
            self.response = requests_post(
                url=self.url,
                data=data,
                headers=headers,
                timeout=self.timeout
            )

            self.validate()
            if self.error:
                return  # The server is down, do not try to send the real request

        self.response = requests_post(
            url=self.url,
            data=self.data,
            headers=headers,
            timeout=self.timeout
        )
        self.validate(bypass_ratelimit)
