/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';

registerPatch({
    name: 'Partner',
    fields: {
        /**
         * States the specific name of this partner in the context of whatsapp.
         * Either a string or undefined.
         */
        user_whatsapp_username: attr(),
    },
});
