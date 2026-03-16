/**
 * Middleware Module
 * 
 * Registers all bot middleware
 */

import { Telegraf } from 'telegraf';
import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

// Import middleware
import { sessionMiddleware } from './session';
import { rateLimitMiddleware } from './rateLimit';
import { userMiddleware } from './user';
import { loggingMiddleware } from './logging';

/**
 * Setup all middleware
 */
export function setupMiddleware(bot: Telegraf<BotContext>): void {
  logger.info('Registering middleware...');

  // Session middleware (must be first)
  bot.use(sessionMiddleware);

  // Logging middleware
  bot.use(loggingMiddleware);

  // Rate limiting middleware
  bot.use(rateLimitMiddleware);

  // User middleware (load user from database)
  bot.use(userMiddleware);

  logger.info('Middleware registered successfully');
}
