/**
 * Handlers Module
 * 
 * Registers all event handlers
 */

import { Telegraf } from 'telegraf';
import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

// Import handlers
import { messageHandler } from './message';
import { callbackHandler } from './callback';
import { errorHandler } from './error';

/**
 * Setup all event handlers
 */
export function setupHandlers(bot: Telegraf<BotContext>): void {
  logger.info('Registering event handlers...');

  // Message handler
  bot.on('message', messageHandler);

  // Callback query handler
  bot.on('callback_query', callbackHandler);

  // Error handler
  bot.catch(errorHandler);

  logger.info('Event handlers registered successfully');
}
