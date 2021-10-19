odoo.define('extend_report.ReportActionManager', function (require) {
"use strict";

    var ActionManager = require('web.ActionManager');

    ActionManager.include({
        _executeReportAction: function (action, options) {
            if (action.report_type === 'qweb-zpl2') {
                return this._triggerDownload(action, options, 'zpl2');
            }
            return this._super(action, options);
        },

        /**
        * Generates an object containing the report's urls (as value) for every
        * qweb-type we support (as key). It's convenient because we may want to use
        * another report's type at some point (for example, when `qweb-pdf` is not
        * available).
        *
        * @override
        * @param {Object} action
        * @returns {Object}
        */
        _makeReportUrls: function (action) {
            // var reportUrls = {
            //    html: '/report/html/' + action.report_name,
            //    pdf: '/report/pdf/' + action.report_name,
            //    text: '/report/text/' + action.report_name,
            //    zpl2: '/report/zpl2/' + action.report_name,
            //};

            var reportUrls = this._super.apply(this, arguments);
            reportUrls.zpl2 = '/report/zpl2/' + action.report_name

            // We may have to build a query string with `action.data`. It's the place
            // were report's using a wizard to customize the output traditionally put
            // their options.
            //if (_.isUndefined(action.data) || _.isNull(action.data) ||
            //    (_.isObject(action.data) && _.isEmpty(action.data))) {
            //    if (action.context.active_ids) {
            //        var activeIDsPath = '/' + action.context.active_ids.join(',');
            //        reportUrls = _.mapObject(reportUrls, function (value) {
            //            return value += activeIDsPath;
            //        });
            //    }
            //} else {
            //    var serializedOptionsPath = '?options=' + encodeURIComponent(JSON.stringify(action.data));
            //    serializedOptionsPath += '&context=' + encodeURIComponent(JSON.stringify(action.context));
            //    reportUrls = _.mapObject(reportUrls, function (value) {
            //        return value += serializedOptionsPath;
            //    });
            //}
            return reportUrls;
        },
        
    });
});
