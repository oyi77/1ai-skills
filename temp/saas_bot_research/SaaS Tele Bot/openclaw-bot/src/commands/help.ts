/**
 * Help Command
 * 
 * Handles /help command
 */

import { BotContext } from '@/types';

/**
 * Handle /help command
 */
export async function helpCommand(ctx: BotContext): Promise<void> {
  await ctx.reply(
    '🆘 *Help & Support*\n\n' +
    '*Available Commands:*\n' +
    '/start - Start the bot\n' +
    '/create - Create a new video\n' +
    '/topup - Top up credits\n' +
    '/referral - Referral & affiliate\n' +
    '/videos - My videos\n' +
    '/profile - My profile\n' +
    '/subscription - Subscription plans\n' +
    '/settings - Settings\n' +
    '/support - Get help\n' +
    '/help - Show this help\n\n' +
    '*Quick Tips:*\n' +
    '• Upload 1-5 clear photos of your product\n' +
    '• Choose the right niche for better results\n' +
    '• Select your target platform\n' +
    '• Add a brief description or CTA (optional)\n\n' +
    'Need more help? Contact support: @openclaw_support',
    { parse_mode: 'Markdown' }
  );
}
