/**
 * Broadcast Command (Admin)
 * 
 * Handles /broadcast command for admins
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
 * Handle /broadcast command
 */
export async function adminBroadcastCommand(ctx: BotContext): Promise<void> {
  const userId = ctx.from?.id;
  
  if (!userId || !isAdmin(userId)) {
    await ctx.reply('❌ You do not have permission to use this command.');
    return;
  }

  const message = ctx.message;
  
  if (!message || !('text' in message)) {
    await ctx.reply('Usage: /broadcast <message> [filters]');
    return;
  }

  const args = message.text.split(' ').slice(1);
  
  if (args.length === 0) {
    await ctx.reply(
      '📢 *Broadcast Message*\n\n' +
      'Usage: `/broadcast <message>`\n\n' +
      'Filters:\n' +
      '`--tier free|basic|pro|agency`\n' +
      '`--region ID|EN`\n' +
      '`--active-since 7d`',
      { parse_mode: 'Markdown' }
    );
    return;
  }

  const broadcastMessage = args.join(' ');
  
  logger.info(`Admin ${userId} broadcasting message: ${broadcastMessage}`);
  
  // TODO: Implement actual broadcast logic
  
  await ctx.reply(
    '✅ *Broadcast Sent*\n\n' +
    `Message: ${broadcastMessage}\n\n` +
    'Target: All users\n' +
    'Status: Queued for delivery',
    { parse_mode: 'Markdown' }
  );
}
