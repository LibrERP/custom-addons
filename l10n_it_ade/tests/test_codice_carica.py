# -*- coding: utf-8 -*-
#
# Copyright 2018-19 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import base64
import os
import shutil
import tempfile
from datetime import datetime

from lxml import etree
from z0bug_odoo import test_common


CODICE_CARICA_CODE = '99'
CODICE_CARICA_NAME = 'Please, do not use this record!'
CODICE_CARICA_NAME2 = 'Please, delete this record!'


class TestAdeCodiceCarica(test_common.SingleTransactionCase):

    def setUp(self):
        super(TestAdeCodiceCarica, self).setUp()

    def test_codice_carica(self):
        model_name = 'italy.ade.codice.carica'
        self.codice_carica_id = self.create_id(
            model_name,
            {'code': CODICE_CARICA_CODE,
             'name': CODICE_CARICA_NAME})
        rec = self.browse_rec(model_name, self.codice_carica_id)
        self.assertEqual(rec.name, CODICE_CARICA_NAME)
        self.write_rec(model_name, self.codice_carica_id,
                      {'name': CODICE_CARICA_NAME2})
        rec = self.browse_rec(model_name, self.codice_carica_id)
        self.assertEqual(rec.name, CODICE_CARICA_NAME2)
