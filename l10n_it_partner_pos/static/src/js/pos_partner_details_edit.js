odoo.define("l10n_it_partner_pos.PartnerDetailsEdit", function (require) {
    "use strict";

    const PartnerDetailsEdit = require("point_of_sale.PartnerDetailsEdit");
    const Registries = require("point_of_sale.Registries");

    const PosPartnerDetailsEditPatch = (Base) =>
        class extends Base {
            setup() {
                super.setup();
                this.changes.pec_destinatario = this.props.partner.pec_destinatario || false;
                this.changes.codice_destinatario = this.props.partner.codice_destinatario || false;
            }

            captureChange(event) {
                super.captureChange(event);
                if (!event || !event.target) {
                    return;
                }
                const { name, value } = event.target;
                if (name === "pec_destinatario" || name === "codice_destinatario") {
                    this.changes[name] = value || false;
                }
            }
        };

    Registries.Component.extend(PartnerDetailsEdit, PosPartnerDetailsEditPatch);

    return PartnerDetailsEdit;
});
