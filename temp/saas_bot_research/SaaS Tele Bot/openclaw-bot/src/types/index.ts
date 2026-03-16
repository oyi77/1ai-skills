/**
 * Type Definitions
 * 
 * Centralized TypeScript type definitions
 */

import { Context } from 'telegraf';

// =============================================================================
// USER TYPES
// =============================================================================

export type UserTier = 'free' | 'basic' | 'pro' | 'agency';

export type UserLanguage = 'id' | 'en';

export interface User {
  id: number;
  telegramId: number;
  uuid: string;
  username?: string;
  firstName: string;
  lastName?: string;
  phoneNumber?: string;
  tier: UserTier;
  creditBalance: number;
  creditExpiresAt?: Date;
  referralCode?: string;
  referredBy?: string;
  referralTier: number;
  language: UserLanguage;
  notificationsEnabled: boolean;
  autoRenewal: boolean;
  isBanned: boolean;
  createdAt: Date;
  updatedAt: Date;
  lastActivityAt: Date;
}

// =============================================================================
// BOT CONTEXT
// =============================================================================

export interface BotContext extends Context {
  session: SessionData;
  user?: User;
}

export interface SessionData {
  state: BotState;
  stateData: Record<string, unknown>;
  lastActivity: Date;
}

export type BotState =
  | 'START'
  | 'ONBOARDING'
  | 'ONBOARDING_LANGUAGE'
  | 'ONBOARDING_TERMS'
  | 'DASHBOARD'
  | 'CREATE_VIDEO_UPLOAD'
  | 'CREATE_VIDEO_NICHE'
  | 'CREATE_VIDEO_PLATFORM'
  | 'CREATE_VIDEO_BRIEF'
  | 'CREATE_VIDEO_CONFIRM'
  | 'CREATE_VIDEO_PROCESSING'
  | 'TOPUP_SELECT'
  | 'TOPUP_PAYMENT'
  | 'TOPUP_CONFIRM'
  | 'REFERRAL_VIEW'
  | 'REFERRAL_WITHDRAW'
  | 'PROFILE_VIEW'
  | 'SETTINGS_LANGUAGE'
  | 'SETTINGS_NOTIFICATIONS'
  | 'SUPPORT_CHAT';

// =============================================================================
// VIDEO TYPES
// =============================================================================

export type VideoStatus = 'processing' | 'completed' | 'failed' | 'expired';

export type VideoPlatform = 'tiktok' | 'instagram' | 'youtube' | 'facebook' | 'twitter' | 'linkedin';

export type VideoNiche = 
  | 'fnb'
  | 'beauty'
  | 'retail'
  | 'services'
  | 'professional'
  | 'hospitality';

export interface VideoParams {
  niche: VideoNiche;
  platform: VideoPlatform;
  duration: number;
  scenes: number;
  images: string[];
  brief?: string;
  angles?: number;
}

// =============================================================================
// PAYMENT TYPES
// =============================================================================

export type TransactionStatus = 'pending' | 'processing' | 'success' | 'failed' | 'expired' | 'refunded';

export type TransactionType = 'topup' | 'subscription' | 'refund' | 'bonus' | 'adjustment';

export type PaymentGateway = 'midtrans' | 'tripay';

export interface TopupPackage {
  id: string;
  name: string;
  nameId: string;
  priceIdr: number;
  credits: number;
  bonus: number;
  expiryDays: number | null;
  savingsPercent: number;
}

// =============================================================================
// REFERRAL TYPES
// =============================================================================

export type CommissionStatus = 'pending' | 'available' | 'withdrawn';

export interface ReferralStats {
  totalReferrals: number;
  tier1Referrals: number;
  tier2Referrals: number;
  totalCommission: number;
  pendingCommission: number;
  availableCommission: number;
  withdrawnCommission: number;
}

// =============================================================================
// API RESPONSE TYPES
// =============================================================================

export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    requestId: string;
    timestamp: string;
  };
}

// =============================================================================
// ERROR TYPES
// =============================================================================

export class BotError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public details?: unknown
  ) {
    super(message);
    this.name = 'BotError';
  }
}

export class ValidationError extends BotError {
  constructor(message: string, details?: unknown) {
    super(message, 'VALIDATION_ERROR', 400, details);
    this.name = 'ValidationError';
  }
}

export class InsufficientCreditsError extends BotError {
  constructor(message: string = 'Insufficient credits') {
    super(message, 'INSUFFICIENT_CREDITS', 402);
    this.name = 'InsufficientCreditsError';
  }
}

export class RateLimitError extends BotError {
  constructor(message: string = 'Rate limit exceeded') {
    super(message, 'RATE_LIMIT_EXCEEDED', 429);
    this.name = 'RateLimitError';
  }
}
