odoo.define('sale_management_template.section_and_note_patch', function (require) {
    'use strict';

    /**
     * Extends section_and_note_one2many to keep checkbox columns (preselected/check)
     * visible and functional on section/note rows.
     */

    var pyUtils = require('web.py_utils');
    var core = require('web.core');
    var _t = core._t;
    var FieldChar = require('web.basic_fields').FieldChar;
    var FieldText = require('web.basic_fields').FieldText;
    var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
    var fieldRegistry = require('web.field_registry');
    var ListRenderer = require('web.ListRenderer');

    var SectionAndNoteListRenderer = ListRenderer.extend({
        _renderBodyCell: function (record, node, index, options) {
            var $cell = this._super.apply(this, arguments);

            var isSection = record.data.display_type === 'line_section';
            var isNote = record.data.display_type === 'line_note';

            if (!isSection && !isNote) {
                return $cell;
            }

            // Checkbox columns to keep visible on section/note rows
            var allowedNames = ['preselected', 'check'];
            var allowedCount = this.columns ? this.columns.filter(function (col) {
                return allowedNames.indexOf(col.attrs.name) !== -1;
            }).length : 0;

            // No checkbox columns? Fall back to stock section/note behavior
            if (!allowedCount) {
                if (node.attrs.widget === 'handle') {
                    return $cell;
                }
                if (node.attrs.name === 'name') {
                    var nbrCols = this._getNumberOfCols();
                    if (this.handleField) nbrCols--;
                    if (this.addTrashIcon) nbrCols--;
                    $cell.attr('colspan', nbrCols);
                } else {
                    $cell.addClass('o_hidden');
                }
                return $cell;
            }

            // Keep handle visible
            if (node.attrs.widget === 'handle') {
                return $cell;
            }

            // Span description across remaining columns
            if (node.attrs.name === 'name') {
                var cols = this._getNumberOfCols();
                if (this.handleField) cols--;
                if (this.addTrashIcon) cols--;
                cols -= allowedCount;
                $cell.attr('colspan', cols);
                return $cell;
            }

            // Keep checkbox columns visible
            if (allowedNames.indexOf(node.attrs.name) !== -1) {
                return $cell;
            }

            // Hide all other columns
            return $cell.addClass('o_hidden');
        },

        _renderRow: function (record, index) {
            var $row = this._super.apply(this, arguments);
            if (record.data.display_type) {
                $row.addClass('o_is_' + record.data.display_type);
            }
            return $row;
        },

        _renderView: function () {
            var def = this._super.apply(this, arguments);
            this.$el.find('> table').addClass('o_section_and_note_list_view');
            return def;
        },

        _onAddRecord: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();

            var self = this;
            this.unselectRow().then(function () {
                var context = ev.currentTarget.dataset.context;
                var pricelistId = self._getPricelistId();

                if (context && pyUtils.py_eval(context).open_product_configurator) {
                    self._rpc({
                        model: 'ir.model.data',
                        method: 'xmlid_to_res_id',
                        kwargs: {xmlid: 'sale.sale_product_configurator_view_form'},
                    }).then(function (res_id) {
                        self.do_action({
                            name: _t('Configure a product'),
                            type: 'ir.actions.act_window',
                            res_model: 'sale.product.configurator',
                            views: [[res_id, 'form']],
                            target: 'new',
                            context: {'default_pricelist_id': pricelistId}
                        }, {
                            on_close: function (products) {
                                if (products && products !== 'special') {
                                    self.trigger_up('add_record', {
                                        context: self._productsToRecords(products),
                                        forceEditable: "bottom",
                                        allowWarning: true,
                                        onSuccess: function () {
                                            self.unselectRow();
                                        }
                                    });
                                }
                            }
                        });
                    });
                } else {
                    self.trigger_up('add_record', {context: context && [context]});
                }
            });
        },

        _getPricelistId: function () {
            var saleOrderForm = this.getParent() && this.getParent().getParent();
            var stateData = saleOrderForm && saleOrderForm.state && saleOrderForm.state.data;
            return stateData && stateData.pricelist_id && stateData.pricelist_id.data && stateData.pricelist_id.data.id;
        },

        _productsToRecords: function (products) {
            var records = [];
            _.each(products, function (product) {
                var record = {
                    default_product_id: product.product_id,
                    default_product_uom_qty: product.quantity
                };

                if (product.no_variant_attribute_values) {
                    var default_product_no_variant_attribute_values = [];
                    _.each(product.no_variant_attribute_values, function (attribute_value) {
                        default_product_no_variant_attribute_values.push([4, parseInt(attribute_value.value)]);
                    });
                    record.default_product_no_variant_attribute_values = default_product_no_variant_attribute_values;
                }

                if (product.product_custom_attribute_values) {
                    var default_custom_attribute_values = [];
                    _.each(product.product_custom_attribute_values, function (attribute_value) {
                        default_custom_attribute_values.push([0, 0, {
                            attribute_value_id: attribute_value.attribute_value_id,
                            custom_value: attribute_value.custom_value
                        }]);
                    });
                    record.default_product_custom_attribute_values = default_custom_attribute_values;
                }

                records.push(record);
            });
            return records;
        }
    });

    var SectionAndNoteFieldText = function (parent, name, record, options) {
        var isSection = record.data.display_type === 'line_section';
        var Constructor = isSection ? FieldChar : FieldText;
        return new Constructor(parent, name, record, options);
    };

    var SectionAndNoteFieldOne2Many = FieldOne2Many.extend({
        _getRenderer: function () {
            if (this.view.arch.tag === 'tree') {
                return SectionAndNoteListRenderer;
            }
            return this._super.apply(this, arguments);
        }
    });

    fieldRegistry.add('section_and_note_one2many', SectionAndNoteFieldOne2Many);
    fieldRegistry.add('section_and_note_text', SectionAndNoteFieldText);
});
