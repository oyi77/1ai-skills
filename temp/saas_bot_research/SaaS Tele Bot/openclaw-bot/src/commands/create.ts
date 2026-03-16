/**
 * Create Command
 * 
 * Handles /create command
 */

import { BotContext } from '@/types';

/**
 * Handle /create command
 */
export async function createCommand(ctx: BotContext): Promise<void> {
  await ctx.reply(
    '🎬 *Create New Video*\n\n' +
    'Follow these steps to create your video:\n\n' +
    '1️⃣ Upload 1-5 photos of your product\n' +
    '2️⃣ Select your niche\n' +
    '3️⃣ Choose target platform\n' +
    '4️⃣ Add optional description/CTA\n' +
    '5️⃣ AI generates your video!\n\n' +
    'Ready? Upload your photos now! 📤',
    { 
      parse_mode: 'Markdown',
      reply_markup: {
        remove_keyboard: true,
      },
    }
  );

  ctx.session.state = 'CREATE_VIDEO_UPLOAD';
}
