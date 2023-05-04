odoo.define('web_show_sum_header.list_renderer', function (require) {
    'use strict';

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        /**
     * Render the main header for the list view.  It is basically just a <thead>
     * with the name of each fields
     *
     * @private
     * @param {boolean} isGrouped
     * @returns {jQueryElement} a <thead> element
     */
    _renderHeader: function (isGrouped) {
        var $tr = $('<tr>')
            .append(_.map(this.columns, this._renderHeaderCell.bind(this)));
        if (this.hasSelectors) {
            $tr.prepend(this._renderSelector('th'));
        }

        var aggregates = {};
        _.each(this.columns, function (column) {
            if ('aggregate' in column) {
                aggregates[column.attrs.name] = column.aggregate;
            }
        });

        var thead = $('<thead>').append($tr);
        if (Object.keys(aggregates).length > 0) {
            var $cells = this._renderAggregateCells(aggregates, false);
            if (this.hasSelectors) {
                $cells.unshift($('<td>'));
            }

            var tr_append = $('<tr>').css({
              "cursor": "default",
              "color": "#4c4c4c",
              "background-color": "#eee",
              "font-weight": "bold",
              "border-top": "2px solid #cacaca",
              "border-bottom": "1px solid #cacaca"
            });

            return thead.append(tr_append.append($cells));
        } else {
            return thead;
        }
    },
    });

});