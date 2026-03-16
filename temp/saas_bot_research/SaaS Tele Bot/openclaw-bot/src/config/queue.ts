/**
 * Queue Configuration
 * 
 * BullMQ queue initialization
 */

import { Queue, Worker, Job } from 'bullmq';
import { redis } from './redis';
import { logger } from '@/utils/logger';

// Queue instances
export const videoQueue = new Queue('video-generation', {
  connection: redis,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 5000,
    },
    removeOnComplete: 100,
    removeOnFail: 500,
  },
});

export const paymentQueue = new Queue('payment-processing', {
  connection: redis,
  defaultJobOptions: {
    attempts: 5,
    backoff: {
      type: 'fixed',
      delay: 10000,
    },
    removeOnComplete: 100,
    removeOnFail: 500,
  },
});

export const notificationQueue = new Queue('notifications', {
  connection: redis,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 1000,
    },
    removeOnComplete: 50,
    removeOnFail: 100,
  },
});

/**
 * Initialize queues
 */
export async function initializeQueue(): Promise<void> {
  try {
    // Setup event handlers
    videoQueue.on('completed', (job) => {
      logger.info(`Video job completed: ${job.id}`);
    });

    videoQueue.on('failed', (job, err) => {
      logger.error(`Video job failed: ${job?.id}`, err);
    });

    paymentQueue.on('completed', (job) => {
      logger.info(`Payment job completed: ${job.id}`);
    });

    paymentQueue.on('failed', (job, err) => {
      logger.error(`Payment job failed: ${job?.id}`, err);
    });

    logger.info('✅ Queues initialized successfully');
  } catch (error) {
    logger.error('❌ Queue initialization failed:', error);
    throw error;
  }
}

/**
 * Add video generation job
 */
export async function addVideoJob(data: unknown): Promise<Job> {
  return videoQueue.add('generate', data, {
    priority: 1,
  });
}

/**
 * Add payment processing job
 */
export async function addPaymentJob(data: unknown): Promise<Job> {
  return paymentQueue.add('process', data, {
    priority: 0, // Highest priority
  });
}

/**
 * Add notification job
 */
export async function addNotificationJob(data: unknown): Promise<Job> {
  return notificationQueue.add('send', data, {
    priority: 2,
  });
}

/**
 * Get queue stats
 */
export async function getQueueStats(): Promise<{
  video: { waiting: number; active: number; completed: number; failed: number };
  payment: { waiting: number; active: number; completed: number; failed: number };
  notification: { waiting: number; active: number; completed: number; failed: number };
}> {
  const [videoWaiting, videoActive, videoCompleted, videoFailed] = await Promise.all([
    videoQueue.getWaitingCount(),
    videoQueue.getActiveCount(),
    videoQueue.getCompletedCount(),
    videoQueue.getFailedCount(),
  ]);

  const [paymentWaiting, paymentActive, paymentCompleted, paymentFailed] = await Promise.all([
    paymentQueue.getWaitingCount(),
    paymentQueue.getActiveCount(),
    paymentQueue.getCompletedCount(),
    paymentQueue.getFailedCount(),
  ]);

  const [notificationWaiting, notificationActive, notificationCompleted, notificationFailed] = await Promise.all([
    notificationQueue.getWaitingCount(),
    notificationQueue.getActiveCount(),
    notificationQueue.getCompletedCount(),
    notificationQueue.getFailedCount(),
  ]);

  return {
    video: {
      waiting: videoWaiting,
      active: videoActive,
      completed: videoCompleted,
      failed: videoFailed,
    },
    payment: {
      waiting: paymentWaiting,
      active: paymentActive,
      completed: paymentCompleted,
      failed: paymentFailed,
    },
    notification: {
      waiting: notificationWaiting,
      active: notificationActive,
      completed: notificationCompleted,
      failed: notificationFailed,
    },
  };
}
