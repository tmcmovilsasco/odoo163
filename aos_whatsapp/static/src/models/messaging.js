/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { many } from '@mail/model/model_field';

registerPatch({
    name: 'Messaging',
    fields: {
        /**
         * All pinned whatsapps that are known.
         */
        pinnedWhatsapps: many('Thread', {
            inverse: 'messagingAsPinnedWhatsapp',
            readonly: true,
        }),
    },
});
