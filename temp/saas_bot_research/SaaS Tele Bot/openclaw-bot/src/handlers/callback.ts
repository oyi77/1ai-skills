/**
 * Callback Handler
 * 
 * Handles all callback queries (inline button clicks)
 */

import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

/**
 * Handle callback queries
 */
export async function callbackHandler(ctx: BotContext): Promise<void> {
  try {
    const callbackQuery = ctx.callbackQuery;
    
    if (!callbackQuery || !('data' in callbackQuery)) {
      return;
    }

    const data = callbackQuery.data;

    // Log callback
    logger.debug('Received callback:', {
      userId: ctx.from?.id,
      data,
    });

    // Answer callback to remove loading state
    await ctx.answerCbQuery();

    // Handle niche selection
    if (data.startsWith('niche_')) {
      const niche = data.replace('niche_', '');
      
      await ctx.editMessageText(
        `✅ Niche selected: ${niche.toUpperCase()}\n\n` +
        'Now, select your target platform:',
        {
          reply_markup: {
            inline_keyboard: [
              [
                { text: '📱 TikTok', callback_data: 'platform_tiktok' },
                { text: '📸 Instagram', callback_data: 'platform_instagram' },
              ],
              [
                { text: '▶️ YouTube', callback_data: 'platform_youtube' },
                { text: '💬 Facebook', callback_data: 'platform_facebook' },
              ],
            ],
          },
        }
      );
      ctx.session.state = 'CREATE_VIDEO_PLATFORM';
      return;
    }

    // Handle platform selection
    if (data.startsWith('platform_')) {
      const platform = data.replace('platform_', '');
      
      await ctx.editMessageText(
        `✅ Platform selected: ${platform.toUpperCase()}\n\n` +
        '📝 Optional: Add a brief description or CTA for your video:\n\n' +
        'Examples:\n' +
        '• "50% off this weekend!"\n' +
        '• "New menu launching soon"\n' +
        '• "Book now and get 20% discount"\n\n' +
        'Or click Skip to continue:',
        {
          reply_markup: {
            inline_keyboard: [
              [{ text: '⏭️ Skip', callback_data: 'brief_skip' }],
            ],
          },
        }
      );
      ctx.session.state = 'CREATE_VIDEO_BRIEF';
      return;
    }

    // Handle topup selection
    if (data.startsWith('topup_')) {
      const packageId = data.replace('topup_', '');
      
      const packages: Record<string, { name: string; price: number; credits: number }> = {
        starter: { name: 'Starter', price: 50000, credits: 5 },
        growth: { name: 'Growth', price: 150000, credits: 15 },
        scale: { name: 'Scale', price: 500000, credits: 60 },
        enterprise: { name: 'Enterprise', price: 1500000, credits: 200 },
      };

      const pkg = packages[packageId];
      
      if (pkg) {
        await ctx.editMessageText(
          `💳 ${pkg.name} Package\n\n` +
          `Price: Rp ${pkg.price.toLocaleString('id-ID')}\n` +
          `Credits: ${pkg.credits}\n\n` +
          'Select payment method:',
          {
            reply_markup: {
              inline_keyboard: [
                [{ text: '💳 Credit Card', callback_data: `payment_card_${packageId}` }],
                [{ text: '🏧 Bank Transfer', callback_data: `payment_bank_${packageId}` }],
                [{ text: '📱 QRIS', callback_data: `payment_qris_${packageId}` }],
                [{ text: '💰 E-Wallet', callback_data: `payment_ewallet_${packageId}` }],
              ],
            },
          }
        );
      }
      return;
    }

    // Handle create video
    if (data === 'create_video') {
      await ctx.editMessageText(
        '📤 Please upload 1-5 photos of your product:\n\n' +
        'Tips for best results:\n' +
        '• Use high-quality images\n' +
        '• Show the product clearly\n' +
        '• Good lighting helps a lot!'
      );
      ctx.session.state = 'CREATE_VIDEO_UPLOAD';
      return;
    }

    // Handle share referral
    if (data === 'share_referral') {
      const referralCode = `REF-${ctx.from?.username?.toUpperCase() || 'USER'}-X7K9`;
      const referralLink = `https://t.me/OpenClawBot?start=${referralCode}`;
      
      await ctx.editMessageText(
        '🔗 Your Referral Link\n\n' +
        `Code: ${referralCode}\n\n` +
        `Link: ${referralLink}\n\n` +
        'Share this link with your friends and earn 10% commission on their purchases!',
        {
          reply_markup: {
            inline_keyboard: [
              [{ text: '📤 Share Link', url: `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=${encodeURIComponent('Join OpenClaw and create amazing AI videos!')}` }],
            ],
          },
        }
      );
      return;
    }

    // Default: unknown callback
    await ctx.reply('❓ Unknown action. Please try again.');

  } catch (error) {
    logger.error('Error in callback handler:', error);
    await ctx.reply('❌ Something went wrong. Please try again later.');
  }
}
