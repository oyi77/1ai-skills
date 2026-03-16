/**
 * Support Command
 * 
 * Handles /support command
 */

import { BotContext } from '@/types';

/**
 * Handle /support command
 */
export async function supportCommand(ctx: BotContext): Promise<void> {
  await ctx.reply(
    '🆘 *Help & Support*\n\n' +
    '*Frequently Asked Questions:*\n\n' +
    '*Q: How do I create a video?*\n' +
    'A: Use /create command and follow the steps.\n\n' +
    '*Q: How long does video generation take?*\n' +
    'A: Usually 2-5 minutes depending on queue.\n\n' +
    '*Q: What formats are supported?*\n' +
    'A: TikTok, Instagram, YouTube, Facebook, Twitter.\n\n' +
    '*Q: How do credits work?*\n' +
    'A: 1 credit = 1 video (30s, 5 scenes)\n\n' +
    'Need more help? Contact us!',
    {
      parse_mode: 'Markdown',
      reply_markup: {
        inline_keyboard: [
          [{ text: '💬 Chat Support', url: 'https://t.me/openclaw_support' }],
          [{ text: '📖 View Tutorial', callback_data: 'view_tutorial' }],
          [{ text: '🐛 Report Bug', callback_data: 'report_bug' }],
        ],
      },
    }
  );

  ctx.session.state = 'SUPPORT_CHAT';
}
