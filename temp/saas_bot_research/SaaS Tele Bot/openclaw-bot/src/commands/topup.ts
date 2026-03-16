/**
 * Topup Command
 * 
 * Handles /topup command
 */

import { BotContext } from '@/types';

/**
 * Handle /topup command
 */
export async function topupCommand(ctx: BotContext): Promise<void> {
  await ctx.reply(
    '💰 *Top Up Credits*\n\n' +
    'Choose your package:\n\n' +
    '*Starter* - Rp 50.000\n' +
    '• 5 credits + 1 bonus\n' +
    '• Valid for 30 days\n\n' +
    '*Growth* - Rp 150.000\n' +
    '• 15 credits + 3 bonus\n' +
    '• Valid for 60 days\n' +
    '• Save 10%\n\n' +
    '*Scale* - Rp 500.000\n' +
    '• 60 credits + 15 bonus\n' +
    '• Valid for 90 days\n' +
    '• Save 20%\n\n' +
    '*Enterprise* - Rp 1.500.000\n' +
    '• 200 credits + 60 bonus\n' +
    '• Never expires\n' +
    '• Save 30%',
    {
      parse_mode: 'Markdown',
      reply_markup: {
        inline_keyboard: [
          [
            { text: 'Starter', callback_data: 'topup_starter' },
            { text: 'Growth', callback_data: 'topup_growth' },
          ],
          [
            { text: 'Scale', callback_data: 'topup_scale' },
            { text: 'Enterprise', callback_data: 'topup_enterprise' },
          ],
        ],
      },
    }
  );

  ctx.session.state = 'TOPUP_SELECT';
}
