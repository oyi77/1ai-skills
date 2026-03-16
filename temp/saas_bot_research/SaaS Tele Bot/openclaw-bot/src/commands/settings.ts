/**
 * Settings Command
 * 
 * Handles /settings command
 */

import { BotContext } from '@/types';

/**
 * Handle /settings command
 */
export async function settingsCommand(ctx: BotContext): Promise<void> {
  await ctx.reply(
    '⚙️ *Settings*\n\n' +
    'Configure your preferences:\n\n' +
    '*Language:* Bahasa Indonesia\n' +
    '*Notifications:* Enabled\n' +
    '*Auto-renewal:* Disabled\n\n' +
    'What would you like to change?',
    {
      parse_mode: 'Markdown',
      reply_markup: {
        inline_keyboard: [
          [{ text: '🌐 Change Language', callback_data: 'settings_language' }],
          [{ text: '🔔 Notifications', callback_data: 'settings_notifications' }],
          [{ text: '🔄 Auto-renewal', callback_data: 'settings_autorenewal' }],
        ],
      },
    }
  );

  ctx.session.state = 'SETTINGS_LANGUAGE';
}
