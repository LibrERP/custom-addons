{
    "name": "ITA - POS - Partner E-invoicing Fields",
    "summary": "Expose recipient PEC and SDI code for partners in POS loader",
    "version": "16.0.1.0.1",
    "category": "Point Of Sale",
    "author": "Codebeex srl",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_pos_fiscalcode",
        "l10n_it_fatturapa",
    ],
    "assets": {
        "point_of_sale.assets": [
            "l10n_it_partner_pos/static/src/js/pos_partner_details_edit.js",
            "l10n_it_partner_pos/static/src/pos.css",
            "l10n_it_partner_pos/static/src/xml/pos.xml",
        ],
    },
    "installable": True,
    "application": False,
}
