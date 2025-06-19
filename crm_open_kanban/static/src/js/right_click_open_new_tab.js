odoo.define('crm_open_kanban.right_click_only', function (require) {
    "use strict";

    const core = require('web.core');

    core.bus.on('DOM_updated', null, function () {
        document.querySelectorAll('.o_kanban_record').forEach(card => {
            if (card.dataset._patchedRightClick) return;
            card.dataset._patchedRightClick = true;

            card.addEventListener('contextmenu', function (e) {
                const link = card.querySelector('.right-click-hidden-link');
                if (!link) return;

                link.style.display = 'inline';
                link.style.position = 'fixed';
                link.style.left = e.clientX + 'px';
                link.style.top = e.clientY + 'px';
                link.click();
                link.style.display = 'none';
                e.preventDefault();
            });
        });
    });
});
