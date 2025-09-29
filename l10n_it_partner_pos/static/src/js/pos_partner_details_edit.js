odoo.define("l10n_it_partner_pos.PartnerDetailsEdit", function (require) {
    "use strict";

    const PartnerDetailsEdit = require("point_of_sale.PartnerDetailsEdit");
    const Registries = require("point_of_sale.Registries");

    const PosPartnerDetailsEditPatch = (Base) =>
        class extends Base {
            setup() {
                super.setup();
                const partner = this.props.partner || {};
                this.changes.fiscalcode = partner.fiscalcode || false;
                this.changes.pec_destinatario = partner.pec_destinatario || false;
                this.changes.codice_destinatario = partner.codice_destinatario || false;
                this.changes.electronic_invoice_subjected = Object.prototype.hasOwnProperty.call(
                    partner,
                    "electronic_invoice_subjected"
                )
                    ? partner.electronic_invoice_subjected
                    : false;
                this.changes.electronic_invoice_obliged_subject = Object.prototype.hasOwnProperty.call(
                    partner,
                    "electronic_invoice_obliged_subject"
                )
                    ? partner.electronic_invoice_obliged_subject
                    : false;
                this._syncElectronicInvoiceFlags();
            }

            captureChange(event) {
                super.captureChange(event);
                if (!event || !event.target) {
                    return;
                }
                const { name, value } = event.target;
                if (
                    name === "fiscalcode" ||
                    name === "pec_destinatario" ||
                    name === "codice_destinatario"
                ) {
                    this.changes[name] = value || false;
                    if (name !== "fiscalcode") {
                        this._syncElectronicInvoiceFlags();
                    }
                }
            }

            _syncElectronicInvoiceFlags() {
                const codice = (this.changes.codice_destinatario || "").trim();
                const pec = (this.changes.pec_destinatario || "").trim();
                const enabled = Boolean(codice && pec);
                this.changes.electronic_invoice_subjected = enabled;
                this.changes.electronic_invoice_obliged_subject = enabled;
            }
        };

    Registries.Component.extend(PartnerDetailsEdit, PosPartnerDetailsEditPatch);

    return PartnerDetailsEdit;
});
