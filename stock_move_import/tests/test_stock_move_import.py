# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestStockMoveImport(TransactionCase):
    def test_action_open_move_import_returns_import_action(self):
        picking_type = self.env["stock.picking.type"].search([], limit=1)
        self.assertTrue(picking_type)

        picking = self.env["stock.picking"].create({
            "picking_type_id": picking_type.id,
            "location_id": picking_type.default_location_src_id.id,
            "location_dest_id": picking_type.default_location_dest_id.id,
        })

        action = picking.action_open_move_import()

        self.assertEqual(action["tag"], "import")
        self.assertEqual(action["params"]["active_model"], "stock.move")
        self.assertEqual(action["params"]["context"]["default_picking_id"], picking.id)
