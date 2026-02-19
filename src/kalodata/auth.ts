import type { KalodataConfig } from './types.js';

export interface AuthCredentials {
  session: string;
  cfClearance: string;
}

type EnvGetter = () => Record<string, string | undefined>;

let customEnvGetter: EnvGetter | null = null;

export function setEnvGetter(getter: EnvGetter): void {
  customEnvGetter = getter;
}

function getEnv(): Record<string, string | undefined> {
  if (customEnvGetter) {
    return customEnvGetter();
  }
  const g = globalThis as { process?: { env?: Record<string, string | undefined> } };
  if (g.process?.env) {
    return g.process.env;
  }
  return {};
}

/**
 * Parse raw cookies string and extract SESSION and cf_clearance
 * Accepts formats:
 * - "SESSION=abc123; cf_clearance=xyz789"
 * - "SESSION=abc123; other=value; cf_clearance=xyz789"
 */
export function parseCookies(cookies: string): AuthCredentials {
  const sessionMatch = cookies.match(/SESSION=([^;]+)/);
  const cfClearanceMatch = cookies.match(/cf_clearance=([^;]+)/);
  
  if (!sessionMatch || !cfClearanceMatch) {
    throw new Error(
      'Invalid cookies format. Expected: "SESSION=xxx; cf_clearance=yyy"\n' +
      'Please provide full cookies from Kalodata.com'
    );
  }
  
  return {
    session: sessionMatch[1].trim(),
    cfClearance: cfClearanceMatch[1].trim(),
  };
}

export function getCredentialsFromEnv(): AuthCredentials {
  const env = getEnv();
  
  // First: Check for raw KALODATA_COOKIES (new way)
  const rawCookies = env.KALODATA_COOKIES;
  if (rawCookies) {
    return parseCookies(rawCookies);
  }
  
  // Second: Check for individual session/cf_clearance (legacy)
  const session = env.KALODATA_SESSION;
  const cfClearance = env.KALODATA_CF_CLEARANCE;
  
  if (session && cfClearance) {
    return { session, cfClearance };
  }
  
  throw new Error(
    'Missing credentials. Set KALODATA_COOKIES with full cookie string,\n' +
    'or set both KALODATA_SESSION and KALODATA_CF_CLEARANCE'
  );
}

export function buildCookieHeader(credentials: AuthCredentials): string {
  return `SESSION=${credentials.session}; cf_clearance=${credentials.cfClearance}`;
}

export function createHeaders(config: KalodataConfig): Record<string, string> {
  return {
    accept: 'application/json, text/plain, */*',
    'content-type': 'application/json',
    country: config.country || 'ID',
    currency: config.currency || 'IDR',
    language: config.language || 'id-ID',
    cookie: buildCookieHeader({
      session: config.session || '',
      cfClearance: config.cfClearance || '',
    }),
    Referer: 'https://www.kalodata.com/product',
  };
}

export function validateConfig(config: Partial<KalodataConfig>): KalodataConfig {
  let session = config.session;
  let cfClearance = config.cfClearance;
  
  if (!session || !cfClearance) {
    if (config.cookies) {
      const parsed = parseCookies(config.cookies);
      session = session || parsed.session;
      cfClearance = cfClearance || parsed.cfClearance;
    } else {
      const envCreds = getCredentialsFromEnv();
      session = session || envCreds.session;
      cfClearance = cfClearance || envCreds.cfClearance;
    }
  }

  return {
    baseUrl: config.baseUrl || 'https://www.kalodata.com',
    cookies: config.cookies,
    session: session!,
    cfClearance: cfClearance!,
    country: config.country || 'ID',
    currency: config.currency || 'IDR',
    language: config.language || 'id-ID',
    timeout: config.timeout || 30000,
    maxRetries: config.maxRetries || 3,
    retryDelay: config.retryDelay || 1000,
  };
}
