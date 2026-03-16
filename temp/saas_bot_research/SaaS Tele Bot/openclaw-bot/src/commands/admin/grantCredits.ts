/**
 * Grant Credits Command (Admin)
 * 
 * Handles /grant_credits command for admins
 */

import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

/**
 * Check if user is admin
 */
function isAdmin(userId: number): boolean {
  const adminIds = process.env.ADMIN_TELEGRAM_IDS?.split(',').map(id => parseInt(id.trim())) || [];
  return adminIds.includes(userId);
}

/**
 * Handle /grant_credits command
 */
export async function adminGrantCreditsCommand(ctx: BotContext): Promise<void> {
  const userId = ctx.from?.id;
  
  if (!userId || !isAdmin(userId)) {
    await ctx.reply('❌ You do not have permission to use this command.');
    return;
  }

  const message = ctx.message;
  
  if (!message || !('text' in message)) {
    await ctx.reply('Usage: /grant_credits <user_id> <amount> <reason>');
    return;
  }

  const args = message.text.split(' ').slice(1);
  
  if (args.length < 3) {
    await ctx.reply(
      '💰 *Grant Credits*\n\n' +
      'Usage: `/grant_credits <user_id> <amount> <reason>`\n\n' +
      'Example:\n' +
      '`/grant_credits 123456789 10 "Bonus for referral"`',
      { parse_mode: 'Markdown' }
    );
    return;
  }

  const targetUserId = args[0];
  const amount = parseFloat(args[1]);
  const reason = args.slice(2).join(' ');
  
  if (isNaN(amount) || amount <= 0) {
    await ctx.reply('❌ Invalid amount. Please enter a positive number.');
    return;
  }

  logger.info(`Admin ${userId} granting ${amount} credits to user ${targetUserId}. Reason: ${reason}`);
  
  // TODO: Implement actual credit grant logic
  
  await ctx.reply(
    '✅ *Credits Granted*\n\n' +
    `User ID: ${targetUserId}\n` +
    `Amount: ${amount} credits\n` +
    `Reason: ${reason}\n\n` +
    'The user has been notified.',
    { parse_mode: 'Markdown' }
  );
}
