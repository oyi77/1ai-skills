/**
 * Referral Command
 * 
 * Handles /referral command
 */

import { BotContext } from '@/types';

/**
 * Handle /referral command
 */
export async function referralCommand(ctx: BotContext): Promise<void> {
  const username = ctx.from?.username || 'USER';
  const referralCode = `REF-${username.toUpperCase()}-X7K9`;
  const referralLink = `https://t.me/OpenClawBot?start=${referralCode}`;

  await ctx.reply(
    '👥 *Referral & Affiliate*\n\n' +
    'Invite friends and earn commission!\n\n' +
    `*Your Referral Code:* ${referralCode}\n\n` +
    '*Commission Structure:*\n' +
    '• Tier 1 (Direct): 10%\n' +
    '• Tier 2 (Indirect): 5%\n\n' +
    '*Your Stats:*\n' +
    '• Total Referrals: 0\n' +
    '• Total Commission: Rp 0\n' +
    '• Available for Withdrawal: Rp 0\n\n' +
    'Share your link and start earning!',
    {
      parse_mode: 'Markdown',
      reply_markup: {
        inline_keyboard: [
          [{ text: '📤 Share Link', url: `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=${encodeURIComponent('Join OpenClaw and create amazing AI videos!')}` }],
          [{ text: '📊 View Stats', callback_data: 'referral_stats' }],
          [{ text: '💸 Withdraw', callback_data: 'referral_withdraw' }],
        ],
      },
    }
  );

  ctx.session.state = 'REFERRAL_VIEW';
}
