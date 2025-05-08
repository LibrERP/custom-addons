odoo.define('muk_plus.list_view_fix', function (require) {
    'use strict';

    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer');

    // Patch the ListRenderer to add a class to tfoot
    ListRenderer.include({
        _renderFooter: function () {
            var $footer = this._super.apply(this, arguments);
            if ($footer) {
                $footer.addClass('muk_plus_footer');
            }
            return $footer;
        },
    });
});
