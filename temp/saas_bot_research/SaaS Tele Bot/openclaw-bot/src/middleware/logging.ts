/**
 * Logging Middleware
 * 
 * Logs all incoming updates
 */

import { Middleware } from 'telegraf';
import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

/**
 * Logging middleware
 */
export const loggingMiddleware: Middleware<BotContext> = async (ctx, next) => {
  const startTime = Date.now();
  
  // Log incoming update
  logger.info('Incoming update', {
    updateId: ctx.update.update_id,
    userId: ctx.from?.id,
    username: ctx.from?.username,
    chatId: ctx.chat?.id,
    type: getUpdateType(ctx),
  });

  // Process update
  await next();

  // Log completion
  const duration = Date.now() - startTime;
  logger.info('Update processed', {
    updateId: ctx.update.update_id,
    duration: `${duration}ms`,
  });
};

/**
 * Get update type
 */
function getUpdateType(ctx: BotContext): string {
  if (ctx.message) {
    if ('text' in ctx.message) return 'text';
    if ('photo' in ctx.message) return 'photo';
    if ('video' in ctx.message) return 'video';
    if ('document' in ctx.message) return 'document';
    return 'message';
  }
  
  if (ctx.callbackQuery) return 'callback_query';
  if (ctx.inlineQuery) return 'inline_query';
  if (ctx.chosenInlineResult) return 'chosen_inline_result';
  
  return 'unknown';
}
