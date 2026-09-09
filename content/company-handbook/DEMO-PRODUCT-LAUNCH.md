# Demo: Product Launch Video, End to End

One request chains the full kingdom: Vilona → Content → Video → Marketing → Sales.

## The request

> "Vilona, launch our new Vitamin C serum — video, social posts, and email."

## The chain

### 1. Vilona triages (vilona-gm)

Intake: deliverable = launch package; audience = beauty buyers; departments = content + marketing.
Recall: `brain_search("beauty launch past campaigns")` for precedent.
Route: brief Content Director (assets) → Marketing Director (distribution). Sales on standby for enablement.

### 2. Content Director coordinates (content-director)

Splits one brief into three parallel director briefs with shared brand tokens:
- Video Director → 15s product ad (9:16)
- Image Director → thumbnail + 3 social crops
- Copy → hook, ad copy, CTA, email subject lines

Contract first: same palette, same CTA ("Link di Bio"), same deadline.

### 3. Video Director renders (video-director)

Routes to `hyperframes-product-launch-video` (agent-generated, precise timing).
Render path: `1ai-content` → `POST /video/ad-hyperframes` → `services/hyperframes` → `hyperframes render` → MP4.

```bash
curl -X POST http://localhost:8767/video/ad-hyperframes \
  -H 'Content-Type: application/json' \
  -d '{"title":"Serum Vitamin C","category":"beauty","image_url":"https://example.com/serum.jpg"}'
```

### 4. Marketing Director distributes (marketing-director)

Takes video + images + copy from Content:
- Paid: cut 15s → 6s hook variant for Meta Ads (`1ai-ads`)
- Organic: schedule 3 posts via `1ai-social`
- Email: nurture sequence via `1ai-content`

### 5. Sales Director converts (sales-director)

Takes leads from Marketing:
- Score and route via `1ai-affiliate`
- Pipeline tracking via `1ai-career`
- Results saved to brain for next launch

## Verification

- [ ] Vilona brief written, brain recalled
- [ ] All three directors briefed with shared tokens
- [ ] Video MP4 renders and plays
- [ ] Marketing assets scheduled
- [ ] Sales pipeline receiving leads
- [ ] Post-mortem saved to brain (`company-handbook` protocol)
