# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-01-23
#    Author : Fabio Colognesi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import json
from werkzeug.urls import url_decode

from odoo.addons.web.controllers import main as report
from odoo import http
from odoo.tools import html_escape
from odoo.tools.safe_eval import safe_eval
from odoo.http import content_disposition, dispatch_rpc, request, \
                        serialize_exception


class ReportController(report.ReportController):

    @http.route()
    def report_routes(self, reportname, docids=None, converter=None, **data):
        """
            Routes report on Zebra interface orinter
        """
        if converter == 'zpl2':
            report = request.env['ir.actions.report']._get_report_from_name(
                reportname)
            context = dict(request.env.context)

            if docids:
                docids = [int(i) for i in docids.split(',')]
            if data.get('options'):
                data.update(json.loads(data.pop('options')))
            if data.get('context'):
                # Ignore 'lang' here, because the context in data is the one
                # from the webclient *but* if the user explicitely wants to
                # change the lang, this mechanism overwrites it.
                data['context'] = json.loads(data['context'])
                if data['context'].get('lang'):
                    del data['context']['lang']
                context.update(data['context'])

            xml = report.with_context(context).render_qweb_zpl2(docids,
                                                               data=data)[0]
            xmlhttpheaders = [('Content-Type', 'text/plain'),
                              ('Content-Length', len(xml))]
            return request.make_response(xml, headers=xmlhttpheaders)
        else:
            return super(ReportController, self).report_routes(
                reportname, docids, converter, **data)

    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        """
            This function extends standard one managing 'qweb-zpl2' requests
        """
        requestcontent = json.loads(data)
        url, report_type = requestcontent[0], requestcontent[1]
        if report_type == 'qweb-zpl2':
            try:
                reportname = url.split('/report/zpl2/')[1].split('?')[0]
                extension = 'txt'

                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')

                if docids:
                    # Generic report:
                    response = self.report_routes(
                        reportname, docids=docids, converter='zpl2')
                else:
                    # Particular report:
                    # decoding the args represented in JSON
                    if (len(url.split('?')) > 1):
                        data = url_decode(url.split('?')[1]).items()
                        response = self.report_routes(
                            reportname, converter='zpl2', **dict(data))
                    else:
                        response = self.report_routes(
                            reportname, converter='zpl2')

                report = request.env['ir.actions.report']._get_report_from_name(reportname)
                filename = "%s.%s" % (report.name, extension)

                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)
                    if report.print_report_name and not len(obj) > 1:
                        report_name = safe_eval(report.print_report_name, {'object': obj, 'time': time})
                        filename = "%s.%s" % (report_name, extension)
                response.headers.add('Content-Disposition', content_disposition(filename))
                response.set_cookie('fileToken', token)
                return response

            except Exception as e:
                se = serialize_exception(e)
                error = {
                    'code': 200,
                    'message': "Odoo Server Error",
                    'data': se
                }
                return request.make_response(html_escape(json.dumps(error)))
        else:
            return super(ReportController, self).report_download(data, token)
