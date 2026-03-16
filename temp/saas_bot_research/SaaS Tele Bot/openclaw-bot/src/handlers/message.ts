/**
 * Message Handler
 * 
 * Handles all incoming messages
 */

import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

/**
 * Handle incoming messages
 */
export async function messageHandler(ctx: BotContext): Promise<void> {
  try {
    const message = ctx.message;
    
    if (!message) {
      return;
    }

    // Log message
    logger.debug('Received message:', {
      userId: ctx.from?.id,
      chatId: ctx.chat?.id,
      text: 'text' in message ? message.text : '[non-text]',
    });

    // Handle text messages
    if ('text' in message) {
      const text = message.text;

      // Handle menu buttons
      switch (text) {
        case '🎬 Create Video':
        case '🚀 Get Started':
          await ctx.reply(
            '📤 Please upload 1-5 photos of your product:\n\n' +
            'Tips for best results:\n' +
            '• Use high-quality images\n' +
            '• Show the product clearly\n' +
            '• Good lighting helps a lot!',
            {
              reply_markup: {
                remove_keyboard: true,
              },
            }
          );
          ctx.session.state = 'CREATE_VIDEO_UPLOAD';
          return;

        case '💰 Top Up':
          await ctx.reply(
            '💳 Choose your package:\n\n' +
            '• Starter: Rp 50.000 (5 credits + 1 bonus)\n' +
            '• Growth: Rp 150.000 (15 credits + 3 bonus)\n' +
            '• Scale: Rp 500.000 (60 credits + 15 bonus)\n' +
            '• Enterprise: Rp 1.500.000 (200 credits + 60 bonus)',
            {
              reply_markup: {
                inline_keyboard: [
                  [
                    { text: 'Starter', callback_data: 'topup_starter' },
                    { text: 'Growth', callback_data: 'topup_growth' },
                  ],
                  [
                    { text: 'Scale', callback_data: 'topup_scale' },
                    { text: 'Enterprise', callback_data: 'topup_enterprise' },
                  ],
                ],
              },
            }
          );
          return;

        case '📁 My Videos':
          await ctx.reply(
            '📁 Your Videos\n\n' +
            'Here you can find all your generated videos.\n\n' +
            'No videos yet? Create your first one! 🎬',
            {
              reply_markup: {
                inline_keyboard: [
                  [{ text: '🎬 Create New Video', callback_data: 'create_video' }],
                ],
              },
            }
          );
          return;

        case '👤 Profile':
          await ctx.reply(
            '👤 Your Profile\n\n' +
            'Name: ' + (ctx.from?.first_name || 'Unknown') + '\n' +
            'Tier: Free\n' +
            'Credits: 3\n' +
            'Referral Code: REF-' + (ctx.from?.username?.toUpperCase() || 'USER') + '-X7K9\n\n' +
            'Share your referral code and earn 10% commission!',
            {
              reply_markup: {
                inline_keyboard: [
                  [{ text: '🔗 Share Referral', callback_data: 'share_referral' }],
                  [{ text: '⚙️ Settings', callback_data: 'settings' }],
                ],
              },
            }
          );
          return;

        default:
          // Unknown command
          await ctx.reply(
            '❓ I didn\'t understand that.\n\n' +
            'Use the menu below or type /help for assistance.',
            {
              reply_markup: {
                keyboard: [
                  [{ text: '🎬 Create Video' }, { text: '💰 Top Up' }],
                  [{ text: '📁 My Videos' }, { text: '👤 Profile' }],
                ],
                resize_keyboard: true,
              },
            }
          );
      }
    }

    // Handle photo uploads
    if ('photo' in message) {
      if (ctx.session.state === 'CREATE_VIDEO_UPLOAD') {
        await ctx.reply(
          '✅ Photo received!\n\n' +
          'Now, please select your niche:',
          {
            reply_markup: {
              inline_keyboard: [
                [
                  { text: '🍔 F&B', callback_data: 'niche_fnb' },
                  { text: '💄 Beauty', callback_data: 'niche_beauty' },
                ],
                [
                  { text: '🛍️ Retail', callback_data: 'niche_retail' },
                  { text: '🔧 Services', callback_data: 'niche_services' },
                ],
                [
                  { text: '🏢 Professional', callback_data: 'niche_professional' },
                  { text: '🏨 Hospitality', callback_data: 'niche_hospitality' },
                ],
              ],
            },
          }
        );
        ctx.session.state = 'CREATE_VIDEO_NICHE';
        return;
      }
    }

  } catch (error) {
    logger.error('Error in message handler:', error);
    await ctx.reply('❌ Something went wrong. Please try again later.');
  }
}
