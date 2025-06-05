odoo.define('web_clickable_many2many_tags.many2many_tags_clickable', function (require) {
"use strict";

var FieldMany2ManyTags = require('web.relational_fields').FieldMany2ManyTags;
var fieldRegistry = require('web.field_registry');

var ClickableMany2ManyTags = FieldMany2ManyTags.extend({

    _renderTags: function () {
        var self = this;
        var result = this._super.apply(this, arguments);

        // Add click handlers after rendering
        this.$('.badge').each(function() {
            var $badge = $(this);
            $badge.css({
                'cursor': 'pointer',
                'user-select': 'none'
            });

            $badge.off('click.custom_click').on('click.custom_click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // Get the record ID from the badge
                var recordData = $badge.data('record');
                if (recordData && recordData.id) {
                    self._openRecord(recordData.id);
                } else {
                    // Fallback: try to get ID from the badge text or data attributes
                    var recordId = $badge.data('id') ||
                                  $badge.find('.o_badge_text').data('id');
                    if (recordId) {
                        self._openRecord(recordId);
                    }
                }
            });
        });

        return result;
    },

    _openRecord: function (recordId) {
        var isReadonly = this.nodeOptions.readonly_popup || false;
        var actionOptions = {
            type: 'ir.actions.act_window',
            res_model: this.field.relation,
            res_id: recordId,
            views: [[false, 'form']],
            target: 'new',
            context: this.record.getContext(),
        };

        if (isReadonly) {
            actionOptions.flags = {
                mode: 'readonly'
            };
        }

        this.do_action(actionOptions);
    },
});

fieldRegistry.add('clickable_many2many_tags', ClickableMany2ManyTags);

return ClickableMany2ManyTags;
});
