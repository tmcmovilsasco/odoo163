/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';

registerPatch({
    name: 'NotificationListView',
    fields: {
        filteredChannels: {
            compute() {
                if (this.filter === 'whatsapp') {
                    return this.messaging.models['Channel'].all(channel =>
                        channel.channel_type === 'whatsapp' &&
                        channel.thread.isPinned
                    );
                }
                return this._super();
            },
        },
    },
});
