/**
 * Profile Command
 * 
 * Handles /profile command
 */

import { BotContext } from '@/types';

/**
 * Handle /profile command
 */
export async function profileCommand(ctx: BotContext): Promise<void> {
  const user = ctx.from;
  
  if (!user) {
    await ctx.reply('❌ Unable to load profile. Please try again.');
    return;
  }

  await ctx.reply(
    '👤 *Your Profile*\n\n' +
    `*Name:* ${user.first_name} ${user.last_name || ''}\n` +
    `*Username:* @${user.username || 'N/A'}\n` +
    `*ID:* ${user.id}\n\n` +
    '*Account Info:*\n' +
    '• Tier: Free\n' +
    '• Credits: 3\n' +
    '• Videos Created: 0\n\n' +
    '*Referral Info:*\n' +
    `• Code: REF-${user.username?.toUpperCase() || 'USER'}-X7K9\n` +
    '• Total Referrals: 0\n' +
    '• Commission Earned: Rp 0',
    {
      parse_mode: 'Markdown',
      reply_markup: {
        inline_keyboard: [
          [{ text: '⚙️ Settings', callback_data: 'settings' }],
          [{ text: '📜 Transaction History', callback_data: 'transaction_history' }],
        ],
      },
    }
  );
}
