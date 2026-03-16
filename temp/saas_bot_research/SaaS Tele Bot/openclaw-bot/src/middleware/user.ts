/**
 * User Middleware
 * 
 * Loads user data from database
 */

import { Middleware } from 'telegraf';
import { BotContext, User } from '@/types';
import { prisma } from '@/config/database';
import { logger } from '@/utils/logger';

/**
 * User middleware
 */
export const userMiddleware: Middleware<BotContext> = async (ctx, next) => {
  const userId = ctx.from?.id;
  
  if (!userId) {
    return next();
  }

  try {
    // Load user from database
    const dbUser = await prisma.user.findUnique({
      where: { telegramId: userId },
    });

    if (dbUser) {
      // Map database user to context user
      ctx.user = {
        id: Number(dbUser.id),
        telegramId: Number(dbUser.telegramId),
        uuid: dbUser.uuid,
        username: dbUser.username || undefined,
        firstName: dbUser.firstName,
        lastName: dbUser.lastName || undefined,
        phoneNumber: dbUser.phoneNumber || undefined,
        tier: dbUser.tier as any,
        creditBalance: Number(dbUser.creditBalance),
        creditExpiresAt: dbUser.creditExpiresAt || undefined,
        referralCode: dbUser.referralCode || undefined,
        referredBy: dbUser.referredBy || undefined,
        referralTier: dbUser.referralTier,
        language: dbUser.language as any,
        notificationsEnabled: dbUser.notificationsEnabled,
        autoRenewal: dbUser.autoRenewal,
        isBanned: dbUser.isBanned,
        createdAt: dbUser.createdAt,
        updatedAt: dbUser.updatedAt,
        lastActivityAt: dbUser.lastActivityAt,
      };

      // Update last activity
      await prisma.user.update({
        where: { telegramId: userId },
        data: { lastActivityAt: new Date() },
      });
    }

  } catch (error) {
    logger.error('Error loading user:', error);
    // Continue even if user loading fails
  }

  return next();
};
