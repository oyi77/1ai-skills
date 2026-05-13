# fin-compliance-kyc: AML, KYC & Multi-Jurisdiction Regulatory Framework

**REQUIRED SUB-SKILL:** Always active when giving investment recommendations.

---

## Global Regulatory Matrix

### United States
```
Regulators:
  → SEC (Securities and Exchange Commission): Equity, ETFs, mutual funds, bonds
  → CFTC (Commodity Futures Trading Commission): Futures, options on futures, swaps
  → FINRA: Broker-dealers, registered reps
  → OCC: National banks (trading book regulation)
  → FinCEN: AML/BSA compliance, crypto

Key Rules:
  → Regulation Best Interest (Reg BI): Broker duty to client
  → Investment Advisers Act: RIA fiduciary duty
  → Dodd-Frank: Swap reporting, Volcker Rule, stress testing
  → JOBS Act: Crowdfunding, Reg CF/A+ for small companies
  → Howey Test: Is a token a security? (investment of money in common enterprise expecting profits)
  → 40 Act Funds: Mutual funds, ETFs, closed-end funds

Leverage Limits:
  → Reg T (initial margin): 50% for equities
  → Pattern Day Trader: >4 round trips/5 days → $25,000 minimum
  → Crypto: No universal margin regulation (varies by exchange)
```

### European Union (MiFID II / EMIR / GDPR)
```
MiFID II (Markets in Financial Instruments Directive):
  → Best execution: Must demonstrate best outcome for clients
  → Product governance: Target market definition
  → Research unbundling: Cannot bundle with execution
  → Transaction reporting: T+1 to ARM/NCA
  → Appropriateness test: Complex products need suitability check
  → ESMA leverage limits: CFDs = 30:1 for major FX, 20:1 equities
  
EMIR (European Market Infrastructure Regulation):
  → OTC derivatives: Must report to trade repository
  → Clearing obligation: Standardized derivatives → central clearing
  → Margin requirements: VM + IM for bilateral uncleared trades

EU AI Act (2024):
  → High-risk AI systems in finance → conformity assessment required
  → Algorithm-generated advice = high risk → documentation, human oversight
```

### United Kingdom (FCA)
```
FCA Consumer Duty (2023):
  → Good outcomes for retail customers
  → Fair value: Reasonable relationship between cost and benefit
  → Consumer understanding: Communications clear and not misleading
  → Consumer support: Adequate support when needed

FCA Crypto Regulation:
  → Crypto asset firms must register with FCA (since 2020)
  → Financial promotions approval required (since 2023)
  → Stablecoin regulation incoming

Leverage Limits (Retail):
  → FX major pairs: 30:1
  → Equity indices: 20:1
  → Individual equities: 5:1
  → Crypto: 2:1
```

### Singapore (MAS)
```
Monetary Authority of Singapore:
  → Capital Markets Services (CMS) licence for investment advice
  → Recognized Market Operator (RMO) for exchanges
  → Digital Payment Token (DPT) licensing for crypto

MAS Crypto Framework:
  → Payment Services Act (PSA): DPT service providers must be licensed
  → Travel Rule: Crypto transfers must include sender/recipient info
  → Consumer protection: No leverage for retail crypto
  → Stablecoins: MAS regulatory framework (2023)

Accredited Investor threshold: >S$2M net assets or >S$300K income
```

### Indonesia (OJK / BAPPEBTI)
```
OJK (Otoritas Jasa Keuangan):
  → Regulates securities, banking, insurance
  → Capital market: IDX (Jakarta Stock Exchange)
  → Foreign ownership limits in certain sectors

BAPPEBTI (Commodity Futures Trading Regulatory Agency):
  → Crypto assets classified as commodities (not securities)
  → Licensed exchanges required for crypto trading
  → Spot crypto allowed; no derivatives for retail

Key Facts for Indonesian Investors:
  → IDR exposure: Sensitive to USD strength, current account
  → LQ45 Index: Top 45 most liquid IDX stocks
  → GoTo, Bukalapak, Bank Central Asia (BBCA) = major holdings
  → OJK approval needed for foreign fund distribution
```

### Japan (JFSA)
```
Financial Services Agency:
  → Financial Instruments and Exchange Act (FIEA)
  → Crypto: Classified as Crypto Asset Exchange Service Provider (CAESP)
  → Registration required for crypto exchanges
  → Stablecoins: Banking law applies (bank or trust company only)

Leverage Limits:
  → Retail FX: 25:1
  → Crypto: 2:1 (retail)
```

---

## AML/KYC Framework

### Customer Due Diligence (CDD) Levels
```
Simplified CDD (Low Risk):
  → Listed companies, regulated financial institutions
  → Verify identity + beneficial ownership
  → Annual review

Standard CDD (Normal Risk):
  → Individuals, private companies
  → Verify: Name, DOB, address, ID document
  → Beneficial ownership: >25% threshold
  → Source of funds verification
  → Periodic review (every 2 years)

Enhanced Due Diligence (High Risk):
  → PEPs (Politically Exposed Persons)
  → High-risk jurisdictions (FATF greylist/blacklist)
  → Complex/unusual transaction patterns
  → Senior management approval required
  → Ongoing monitoring + annual review
```

### FATF Risk Indicators
```
High-risk jurisdictions (FATF blacklist/greylist):
  → Currently monitored: Check FATF website for current list
  → Examples: North Korea, Iran (blacklist); various EM (greylist)
  → Action: Enhanced DD, senior management approval, potential refusal

Suspicious transaction indicators:
  → Round number transactions ($10,000 exactly)
  → Structured transactions below CTR threshold ($9,999 × multiple)
  → Transactions inconsistent with business type/size
  → Geographic mismatch (funds from high-risk jurisdiction)
  → Crypto mixing services (Tornado Cash, etc.)
  → Rapid movement through multiple accounts
```

### Crypto Compliance
```
Travel Rule (FATF Recommendation 16):
  → For transfers >$1,000 USD/equivalent
  → Must transmit: Originator name, account, address
  → Must transmit: Beneficiary name, account
  → Applies to Virtual Asset Service Providers (VASPs)

Crypto Red Flags:
  → Wallet interacted with sanctioned address
  → Funds through mixing services (Tornado Cash)
  → High-risk exchange (no KYC)
  → Self-hosted wallet for large sums (>$10K)
  → Chain-hopping (rapid conversion across blockchains)

Tools: Chainalysis KYT, TRM Labs, Elliptic
```

---

## Investment Restriction Checklist

Before any recommendation, verify:
- [ ] Asset is legal to own/trade in user's jurisdiction
- [ ] No OFAC/UN/EU sanctions apply to issuer
- [ ] Appropriate investor classification met (retail/professional/institutional)
- [ ] Required licenses for advice (if applicable) are in scope
- [ ] Position doesn't require Form 13F/Schedule 13D filing (>5% public company)
- [ ] No material non-public information (MNPI) risk
- [ ] Short selling rules (locate requirement, naked short ban)
- [ ] Margin/leverage within regulatory limits for jurisdiction
- [ ] Crypto assets comply with local digital asset regulations
- [ ] Tax reporting obligations disclosed (FBAR, FATCA, CRS for offshore)

---

## Disclaimer Template (Always Append to Recommendations)

> ⚠️ **REGULATORY DISCLAIMER:** This analysis is for informational and educational purposes only
> and does not constitute investment advice, financial advice, trading advice, or any other sort
> of advice. All content is provided as-is. Past performance is not indicative of future results.
> All investments involve risk, including potential total loss of capital. Please consult a licensed
> financial advisor, legal counsel, and tax professional before making any investment decisions.
> Regulations vary by jurisdiction. Ensure compliance with local laws and regulations. This
> analysis was prepared without knowledge of your personal financial situation.
