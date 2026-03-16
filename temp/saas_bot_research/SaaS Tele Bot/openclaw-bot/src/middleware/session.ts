/**
 * Session Middleware
 * 
 * Manages user sessions using Redis
 */

import { Middleware } from 'telegraf';
import { BotContext, SessionData } from '@/types';
import { redis } from '@/config/redis';
import { logger } from '@/utils/logger';

const SESSION_TTL = 24 * 60 * 60; // 24 hours in seconds
const SESSION_PREFIX = 'session:';

/**
 * Get session key for user
 */
function getSessionKey(userId: number): string {
  return `${SESSION_PREFIX}${userId}`;
}

/**
 * Get session from Redis
 */
async function getSession(userId: number): Promise<SessionData | null> {
  try {
    const key = getSessionKey(userId);
    const data = await redis.get(key);
    
    if (data) {
      return JSON.parse(data);
    }
    
    return null;
  } catch (error) {
    logger.error('Error getting session:', error);
    return null;
  }
}

/**
 * Save session to Redis
 */
async function saveSession(userId: number, session: SessionData): Promise<void> {
  try {
    const key = getSessionKey(userId);
    await redis.setex(key, SESSION_TTL, JSON.stringify(session));
  } catch (error) {
    logger.error('Error saving session:', error);
  }
}

/**
 * Session middleware
 */
export const sessionMiddleware: Middleware<BotContext> = async (ctx, next) => {
  const userId = ctx.from?.id;
  
  if (!userId) {
    ctx.session = createDefaultSession();
    return next();
  }

  // Load session from Redis
  const session = await getSession(userId);
  
  if (session) {
    ctx.session = session;
  } else {
    ctx.session = createDefaultSession();
  }

  // Continue to next middleware
  await next();

  // Save session after processing
  await saveSession(userId, ctx.session);
};

/**
 * Create default session
 */
function createDefaultSession(): SessionData {
  return {
    state: 'START',
    stateData: {},
    lastActivity: new Date(),
  };
}
