/**
 * Redis Configuration
 * 
 * Redis client initialization
 */

import Redis from 'ioredis';
import { logger } from '@/utils/logger';

// Redis client instance
export const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379', {
  retryStrategy: (times) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  },
  maxRetriesPerRequest: 3,
});

// Event handlers
redis.on('connect', () => {
  logger.info('✅ Redis connected');
});

redis.on('error', (error) => {
  logger.error('❌ Redis error:', error);
});

redis.on('reconnecting', () => {
  logger.warn('🔄 Redis reconnecting...');
});

/**
 * Initialize Redis connection
 */
export async function initializeRedis(): Promise<void> {
  try {
    // Test connection
    await redis.ping();
    logger.info('✅ Redis initialized successfully');
  } catch (error) {
    logger.error('❌ Redis initialization failed:', error);
    throw error;
  }
}

/**
 * Disconnect from Redis
 */
export async function disconnectRedis(): Promise<void> {
  await redis.quit();
  logger.info('Redis disconnected');
}
