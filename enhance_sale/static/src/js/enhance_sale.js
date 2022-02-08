odoo.define('enhance_sale.on_add_record', function(require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');
    var pyUtils = require('web.py_utils');
    var core = require('web.core');
    var _t = core._t;
    var FieldChar = require('web.basic_fields').FieldChar;
    var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
    var fieldRegistry = require('web.field_registry');
    var FieldText = require('web.basic_fields').FieldText;

    var SaleListRenderer = ListRenderer.extend({

        _onAddRecord: function(ev) {
            // we don't want the browser to navigate to a the # url
            ev.preventDefault();

            // we don't want the click to cause other effects, such as unselecting
            // the row that we are creating, because it counts as a click on a tr
            ev.stopPropagation();

            // but we do want to unselect current row
            var self = this;
            this.unselectRow().then(function() {
                var context = ev.currentTarget.dataset.context;

                var pricelistId = self._getPricelistId();
                if (context && pyUtils.py_eval(context).open_product_configurator) {
                    self._rpc({
                        model: 'ir.model.data',
                        method: 'xmlid_to_res_id',
                        kwargs: {
                            xmlid: 'sale.sale_product_configurator_view_form'
                        },
                    }).then(function(res_id) {
                        self.do_action({
                            name: _t('Configure a product'),
                            type: 'ir.actions.act_window',
                            res_model: 'sale.product.configurator',
                            views: [
                                [res_id, 'form']
                            ],
                            target: 'new',
                            context: {
                                'default_pricelist_id': pricelistId
                            }
                        }, {
                            on_close: function(products) {
                                if (products && products !== 'special') {
                                    self.trigger_up('add_record', {
                                        context: self._productsToRecords(products),
                                        forceEditable: "bottom",
                                        allowWarning: true,
                                        onSuccess: function() {
                                            self.unselectRow();
                                        }
                                    });
                                }
                            }
                        });
                    });
                } else {
                    var saleOrderForm = self.getParent() && self.getParent().getParent();
                    var stateData = saleOrderForm && saleOrderForm.state && saleOrderForm.state.data;
                    var order_id = stateData.id;
                    if (order_id == null){
                        order_id = 0;
                    }
                    if (context == null) {
                        context = {
                            order_id: order_id
                        }
                    } else {
                        context = Object.assign(context, {
                            order_id: order_id
                        })
                    }
                    self.trigger_up('add_record', {
                        context: context && [context]
                    });
                }

            });
        },
        _getPricelistId: function() {
            var saleOrderForm = this.getParent() && this.getParent().getParent();
            var stateData = saleOrderForm && saleOrderForm.state && saleOrderForm.state.data;
            var pricelist_id = stateData.pricelist_id && stateData.pricelist_id.data && stateData.pricelist_id.data.id;

            return pricelist_id;
        }
    });

    var SectionAndNoteFieldOne2Many = FieldOne2Many.extend({
        /**
         * We want to use our custom renderer for the list.
         *
         * @override
         */
        _getRenderer: function() {
            if (this.view.arch.tag === 'tree') {
                return SaleListRenderer;
            }
            return this._super.apply(this, arguments);
        },
    });

    fieldRegistry.add('section_and_note_one2many', SectionAndNoteFieldOne2Many);

});
