/**
 * Database Configuration
 * 
 * Prisma client initialization
 */

import { PrismaClient } from '@prisma/client';
import { logger } from '@/utils/logger';

// Prisma client instance
export const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' 
    ? ['query', 'info', 'warn', 'error']
    : ['error'],
});

/**
 * Initialize database connection
 */
export async function initializeDatabase(): Promise<void> {
  try {
    // Test connection
    await prisma.$connect();
    logger.info('✅ Database connected successfully');
  } catch (error) {
    logger.error('❌ Database connection failed:', error);
    throw error;
  }
}

/**
 * Disconnect from database
 */
export async function disconnectDatabase(): Promise<void> {
  await prisma.$disconnect();
  logger.info('Database disconnected');
}
