/**
 * Subscription Command
 * 
 * Handles /subscription command
 */

import { BotContext } from '@/types';

/**
 * Handle /subscription command
 */
export async function subscriptionCommand(ctx: BotContext): Promise<void> {
  await ctx.reply(
    '⭐ *Subscription Plans*\n\n' +
    '*Current Plan:* Free\n\n' +
    '*Available Plans:*\n\n' +
    '*Lite* - Rp 99.000/month\n' +
    '• 20 credits/month\n' +
    '• Priority queue (1.5x)\n' +
    '• Basic support\n\n' +
    '*Pro* - Rp 199.000/month\n' +
    '• 50 credits/month\n' +
    '• All formats & ratios\n' +
    '• Multi-angle (3 variants)\n' +
    '• 1 free revision\n' +
    '• Priority queue (2x)\n\n' +
    '*Agency* - Rp 499.000/month\n' +
    '• 150 credits/month\n' +
    '• White-label export\n' +
    '• Bulk upload (20 files)\n' +
    '• API key access\n' +
    '• Team workspace (5 seats)',
    {
      parse_mode: 'Markdown',
      reply_markup: {
        inline_keyboard: [
          [{ text: '⭐ Upgrade to Lite', callback_data: 'subscribe_lite' }],
          [{ text: '⭐ Upgrade to Pro', callback_data: 'subscribe_pro' }],
          [{ text: '⭐ Upgrade to Agency', callback_data: 'subscribe_agency' }],
        ],
      },
    }
  );
}
