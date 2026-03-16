/**
 * Error Handler
 * 
 * Handles all bot errors
 */

import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

/**
 * Handle bot errors
 */
export async function errorHandler(err: Error, ctx: BotContext): Promise<void> {
  logger.error('Bot error:', {
    error: err.message,
    stack: err.stack,
    update: ctx.update,
  });

  try {
    // Notify user
    await ctx.reply(
      '❌ Oops! Something went wrong.\n\n' +
      'Our team has been notified. Please try again later or contact support.',
      {
        reply_markup: {
          inline_keyboard: [
            [{ text: '💬 Contact Support', callback_data: 'contact_support' }],
          ],
        },
      }
    );
  } catch (replyError) {
    logger.error('Failed to send error message:', replyError);
  }
}
