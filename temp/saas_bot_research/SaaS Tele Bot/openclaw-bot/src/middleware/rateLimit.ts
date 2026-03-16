/**
 * Rate Limit Middleware
 * 
 * Implements rate limiting per user
 */

import { Middleware } from 'telegraf';
import { BotContext } from '@/types';
import { redis } from '@/config/redis';
import { logger } from '@/utils/logger';

// Rate limit configuration
const RATE_LIMIT_WINDOW = 60; // 1 minute in seconds
const RATE_LIMIT_MAX = 30; // Max 30 messages per minute
const RATE_LIMIT_PREFIX = 'ratelimit:';

/**
 * Rate limit middleware
 */
export const rateLimitMiddleware: Middleware<BotContext> = async (ctx, next) => {
  const userId = ctx.from?.id;
  
  if (!userId) {
    return next();
  }

  // Skip rate limiting for admin users
  const adminIds = process.env.ADMIN_TELEGRAM_IDS?.split(',').map(id => parseInt(id.trim())) || [];
  if (adminIds.includes(userId)) {
    return next();
  }

  try {
    const key = `${RATE_LIMIT_PREFIX}${userId}`;
    
    // Get current count
    const current = await redis.get(key);
    const count = current ? parseInt(current) : 0;

    if (count >= RATE_LIMIT_MAX) {
      logger.warn('Rate limit exceeded:', { userId, count });
      
      await ctx.reply(
        '⏳ Whoa there! You\'re sending messages too fast.\n\n' +
        'Please slow down and try again in a moment.'
      );
      
      return;
    }

    // Increment counter
    const pipeline = redis.pipeline();
    pipeline.incr(key);
    pipeline.expire(key, RATE_LIMIT_WINDOW);
    await pipeline.exec();

  } catch (error) {
    logger.error('Rate limit error:', error);
    // Continue even if rate limiting fails
  }

  return next();
};
