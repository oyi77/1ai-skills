/**
 * Start Command
 * 
 * Handles /start command - entry point for new users
 */

import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

/**
 * Handle /start command
 */
export async function startCommand(ctx: BotContext): Promise<void> {
  try {
    const user = ctx.from;
    
    if (!user) {
      await ctx.reply('❌ Unable to identify user. Please try again.');
      return;
    }

    logger.info(`User started bot: ${user.id} (${user.username || 'no username'})`);

    // Check if user exists in database
    // TODO: Implement user lookup
    const existingUser = false;

    if (existingUser) {
      // Welcome back message
      await ctx.reply(
        `👋 Welcome back, ${user.first_name}!\n\n` +
        `Ready to create some amazing videos? 🎬`,
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
    } else {
      // New user onboarding
      await ctx.reply(
        `🎉 Welcome to OpenClaw, ${user.first_name}!\n\n` +
        `I'm your AI video marketing assistant. I can help you create stunning videos for your business in minutes!\n\n` +
        `Here's what you get:\n` +
        `✨ 3 free trial credits\n` +
        `🎬 AI-powered video generation\n` +
        `📱 Multiple platform formats\n` +
        `👥 Referral rewards\n\n` +
        `Let's get started! 🚀`,
        {
          reply_markup: {
            keyboard: [
              [{ text: '🚀 Get Started' }],
            ],
            resize_keyboard: true,
          },
        }
      );

      // TODO: Create new user in database
    }

    // Update session state
    ctx.session.state = 'DASHBOARD';
    ctx.session.lastActivity = new Date();

  } catch (error) {
    logger.error('Error in start command:', error);
    await ctx.reply('❌ Something went wrong. Please try again later.');
  }
}
