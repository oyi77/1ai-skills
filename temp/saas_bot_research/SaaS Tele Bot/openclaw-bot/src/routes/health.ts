/**
 * Health Check Routes
 * 
 * API endpoints for health monitoring
 */

import { FastifyInstance } from 'fastify';
import { prisma } from '@/config/database';
import { redis } from '@/config/redis';
import { getQueueStats } from '@/config/queue';

/**
 * Register health check routes
 */
export async function healthCheckRoutes(server: FastifyInstance): Promise<void> {
  // Basic health check
  server.get('/health', async () => {
    return {
      status: 'healthy',
      version: process.env.npm_package_version || '3.0.0',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'development',
    };
  });

  // Database health check
  server.get('/health/db', async () => {
    try {
      await prisma.$queryRaw`SELECT 1`;
      return {
        status: 'healthy',
        service: 'database',
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      server.log.error('Database health check failed:', error);
      return {
        status: 'unhealthy',
        service: 'database',
        error: 'Database connection failed',
        timestamp: new Date().toISOString(),
      };
    }
  });

  // Redis health check
  server.get('/health/redis', async () => {
    try {
      await redis.ping();
      return {
        status: 'healthy',
        service: 'redis',
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      server.log.error('Redis health check failed:', error);
      return {
        status: 'unhealthy',
        service: 'redis',
        error: 'Redis connection failed',
        timestamp: new Date().toISOString(),
      };
    }
  });

  // Queue health check
  server.get('/health/queue', async () => {
    try {
      const stats = await getQueueStats();
      return {
        status: 'healthy',
        service: 'queue',
        stats,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      server.log.error('Queue health check failed:', error);
      return {
        status: 'unhealthy',
        service: 'queue',
        error: 'Queue check failed',
        timestamp: new Date().toISOString(),
      };
    }
  });

  // Comprehensive health check
  server.get('/health/all', async () => {
    const checks = await Promise.allSettled([
      prisma.$queryRaw`SELECT 1`,
      redis.ping(),
      getQueueStats(),
    ]);

    const [dbCheck, redisCheck, queueCheck] = checks;

    const allHealthy = 
      dbCheck.status === 'fulfilled' &&
      redisCheck.status === 'fulfilled' &&
      queueCheck.status === 'fulfilled';

    return {
      status: allHealthy ? 'healthy' : 'degraded',
      timestamp: new Date().toISOString(),
      checks: {
        database: {
          status: dbCheck.status === 'fulfilled' ? 'healthy' : 'unhealthy',
        },
        redis: {
          status: redisCheck.status === 'fulfilled' ? 'healthy' : 'unhealthy',
        },
        queue: {
          status: queueCheck.status === 'fulfilled' ? 'healthy' : 'unhealthy',
          stats: queueCheck.status === 'fulfilled' ? queueCheck.value : null,
        },
      },
    };
  });
}
