# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, _


def _onchange_eval(self, field_name, onchange, result):
    """ Apply onchange method(s) for field ``field_name`` with spec ``onchange``
        on record ``self``. Value assignments are applied on ``self``, while
        domain and warning messages are put in dictionary ``result``.
    """
    onchange = onchange.strip()

    def process(res):
        if not res:
            return
        if res.get('value'):
            res['value'].pop('id', None)
            self.update({key: val for key, val in res['value'].items() if key in self._fields})
        if res.get('domain'):
            result.setdefault('domain', {}).update(res['domain'])
        if res.get('action'):
            result.setdefault('action', {}).update(res['action'])

        if res.get('warning'):
            result['warnings'].add((
                res['warning'].get('title') or _("Warning"),
                res['warning'].get('message') or "",
            ))

    if onchange in ("1", "true"):
        for method in self._onchange_methods.get(field_name, ()):
            method_res = method(self)
            process(method_res)
        return

models.BaseModel._onchange_eval = _onchange_eval
