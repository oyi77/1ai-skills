/**
 * Webhook Routes
 * 
 * API endpoints for external webhooks
 */

import { FastifyInstance } from 'fastify';
import { Telegraf } from 'telegraf';
import { BotContext } from '@/types';
import { logger } from '@/utils/logger';
import crypto from 'crypto';

interface WebhookOptions {
  bot: Telegraf<BotContext>;
}

/**
 * Register webhook routes
 */
export async function webhookRoutes(server: FastifyInstance, options: WebhookOptions): Promise<void> {
  const { bot } = options;

  // Telegram webhook
  server.post('/webhook/telegram', async (request, reply) => {
    try {
      // Verify webhook secret
      const secret = request.headers['x-telegram-bot-api-secret-token'];
      if (secret !== process.env.WEBHOOK_SECRET) {
        logger.warn('Invalid webhook secret');
        return reply.status(401).send({ error: 'Unauthorized' });
      }

      // Process update
      await bot.handleUpdate(request.body as any);
      
      return { ok: true };
    } catch (error) {
      logger.error('Telegram webhook error:', error);
      return reply.status(500).send({ error: 'Internal server error' });
    }
  });

  // Midtrans webhook
  server.post('/webhooks/midtrans', async (request, reply) => {
    try {
      const body = request.body as any;
      
      // Verify signature
      const signature = request.headers['x-signature'] as string;
      const expectedSignature = crypto
        .createHash('sha512')
        .update(`${body.order_id}${body.status_code}${body.gross_amount}${process.env.MIDTRANS_SERVER_KEY}`)
        .digest('hex');

      if (signature !== expectedSignature) {
        logger.warn('Invalid Midtrans signature');
        return reply.status(401).send({ error: 'Invalid signature' });
      }

      // Process payment notification
      logger.info('Midtrans webhook received:', body);
      
      // TODO: Process payment status update
      
      return { ok: true };
    } catch (error) {
      logger.error('Midtrans webhook error:', error);
      return reply.status(500).send({ error: 'Internal server error' });
    }
  });

  // Tripay webhook
  server.post('/webhooks/tripay', async (request, reply) => {
    try {
      const body = request.body as any;
      
      // Verify signature
      const signature = request.headers['x-signature'] as string;
      const expectedSignature = crypto
        .createHmac('sha256', process.env.TRIPAY_PRIVATE_KEY || '')
        .update(JSON.stringify(body))
        .digest('hex');

      if (signature !== expectedSignature) {
        logger.warn('Invalid Tripay signature');
        return reply.status(401).send({ error: 'Invalid signature' });
      }

      // Process payment notification
      logger.info('Tripay webhook received:', body);
      
      // TODO: Process payment status update
      
      return { ok: true };
    } catch (error) {
      logger.error('Tripay webhook error:', error);
      return reply.status(500).send({ error: 'Internal server error' });
    }
  });
}
