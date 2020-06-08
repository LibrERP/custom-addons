"""
    Copyright (C) 2020 Didotech S.r.l. (<http://www.didotech.com/>).

    python3 -m venv pyvenv3
    . pyvenv3/bin/activate
    pip install pytest
    pip install --upgrade pip
    pip install odoo-client-lib

    pytest -q test_vies.py

    config.py:

    from dataclasses import dataclass


    @dataclass
    class Config:
        hostname: str
        protocol: str
        port: int
        username: str
        password: str
        database: str


    @dataclass
    class Partner:  # Partner should be present in remote db
        vat: str
        country_id: int
        state_id: int

"""

from conftest import odoo_c
from config import partners


class TestVies:

    def test_vies_data(self) -> None:
        partner_model = odoo_c.env('res.partner')
        for partner in partners:
            partner_ids = partner_model.search([('vat', '=', partner.vat)])
            result = partner_model.get_vies_data(partner_ids)
            assert result['country_id'] == partner.country_id
            assert result.get('state_id', False) == partner.state_id

    def test_vies(self) -> None:
        partner_model = odoo_c.env('res.partner')
        for partner in partners:
            result = partner_model.vies_data(False, partner.vat)
            assert result['country_id'] == partner.country_id
            assert result.get('state_id', False) == partner.state_id
