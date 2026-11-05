# Provider Probe Reference (Extended Coverage)

> **Authorization only.** These probes are read-only liveness checks for credentials found during an **authorized** assessment, bug-bounty scope, or internal secret-scanning triage. Never probe keys from systems you do not own or lack written permission to test. This companion reference complements, and does not duplicate, the providers already documented in the parent `api-key-leak-validation/SKILL.md`.

## Safety Rules For Every Probe

- Read-only only. Prefer identity/metadata endpoints; never create, update, charge, message, send, post, upload, delete, or deploy.
- No live secrets in plaintext output. Substitute from `$KEY` / shell variables, mask the value to the last four characters (`****1234`) in notes, reports, CI logs, screenshots, or chat.
- Default to one request, with a sleep/backoff before retries. Keep to two or three quick probes per provider.
- Store token in environment variables, not command history where possible (`HISTCONTROL=ignorespace`, `set +o history`).
- Prefer vendor test/sandbox credentials when the program provides them.
- If a vendor validation endpoint is POST-only, state that explicitly and verify the request does not mutate user data.
- Stop and quarantine keys that point outside assessment scope even when valid.

## Mutating (Do Not Naive-Call) Callouts

- **Slack incoming webhook:** use empty `{"text":""}`; a populated payload posts to the channel.
- **Zapier webhook URL:** any non-empty payload triggers the downstream Zap. Probe only with a clearly labelled disposable/test payload or use a vendor-specific webhook echo endpoint.
- **Heroku CLI/API:** some keyhacks examples `POST /apps`; that mutates account state. Use `GET /account` below instead.
- **Twilio:** `GET /Accounts` is read-only; sending SMS or creating keys is write.
- **Stripe:** use `GET /v1/balance` or `GET /v1/account`; never `POST /v1/charges`.
- **Telegram:** `getMe` is read-only; `sendMessage` mutates chat state.
- **Firebase Cloud Messaging:** sending a message is mutating; no safe liveness-only check is documented here, so FCM is intentionally omitted.
- **Razorpay:** account or payment list calls are read-only; refund/capture calls are write.

## Cloud & Infrastructure

### Google Cloud (Service Account Access Token)
```bash
export GC_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)"
curl -s -H "Authorization: Bearer $GC_ACCESS_TOKEN" https://www.googleapis.com/oauth2/v1/tokeninfo
```
- **Valid:** `200` with token audience, scope, and expiry fields.
- **Invalid:** `400`/`401` with `invalid_token`.
- **Scope probe:** tokeninfo does not expose IAM roles; inspect granted scopes.
- **Write risk:** token can access scoped cloud resources; treat as sensitive.

### Infura (Project API Key)
```bash
curl -s -X POST https://mainnet.infura.io/v3/$INFURA_KEY \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```
- **Valid:** JSON-RPC `result` with a block number.
- **Invalid:** error with code `-32602` or HTTP `401`/`403`.
- **Scope probe:** `eth_accounts` returns empty for non-archive/no-write keys.
- **Write risk:** methods such as transfer/unlock are not exercised; only `eth_blockNumber` is read-only.

### Azure Shared Access Signature (SAS Token)
```bash
curl -s -o /dev/null -w '%{http_code}' \
  "https://${STORAGEuenta}.blob.core.windows.net/${CONTAINE}/?${SAS_TOKEN}"
```
- **Valid:** `200` with XML blob list.
- **Invalid:** `403` with `AuthenticationFailed` or `Signature mismatch`.
- **Scope probe:** path and signed permission (`spr`, `sp`) disclose allowed verbs/resources.
- **Write risk:** TTL expiry limits abuse; a write permission SAS can mutate blobs.

### Azure Application Insights (Instrumentation + API Key)
```bash
curl -s "https://api.applicationinsights.io/v1/apps/$APP_ID/metrics/requests/count" \
  -H "x-api-key: $APP_INSIGHTS_KEY"
```
- **Valid:** JSON metric payload with timestamped values.
- **Invalid:** `401`/`403` with authentication or app errors.
- **Scope probe:** app IDs available only to key; metric discovery is read-only.
- **Write risk:** API key is read-only against Application Insights data exports.

### Google Maps (API Key)
```bash
curl -s "https://maps.googleapis.com/maps/api/geocode/json?address=Test&key=$GMAPS_KEY" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('status'));print(d.get('error_message'))"
```
- **Valid:** `OK` or `ZERO_RESULTS`.
- **Invalid:** `REQUEST_DENIED` or `INVALID_REQUEST` for the key.
- **Scope probe:** abuse report may show enabled APIs under key restrictions.
- **Write risk:** none data mutation; may incur billable geocoding quota.

### Bing Maps (API Key)
```bash
curl -s "https://dev.virtualearth.net/REST/v1/Locations?q=Seattle,WA&key=$BING_KEY" \
  | python3 -m json.tool | head -20
```
- **Valid:** JSON with `statusCode: 200` and `authenticationResultCode: ValidCredentials`.
- **Invalid:** `authenticationResultCode` mentioning `InvalidCredentials` or quota exceeded.
- **Scope probe:** restricted key may allow only certain APIs.
- **Write risk:** no mutation; quota/billing risk remains.

### Loqate (API Key)
```bash
curl -s "http://api.addressy.com/Capture/Interactive/Find/v1.00/json3.ws?Key=$LOQATE_KEY&Text=BHAR&Limit=5&Countries=US"
```
- **Valid:** JSON with non-empty `Items` array.
- **Invalid:** error code such as `2` or `1001`.
- **Scope probe:** restricted keys return authorization failures.
- **Write risk:** read-only address lookup; billable quota risk.

### Ipstack (Access Key)
```bash
curl -s "https://api.ipstack.com/8.8.8.8?access_key=$IPSTACK_KEY" | python3 -m json.tool | head -20
```
- **Valid:** JSON with `ip`, `country_name`, and no `error`.
- **Invalid:** JSON with `success: false` and `error.code` of `101`, `104`, or `401`.
- **Scope probe:** many proxies required for higher precision; not tied to account.
- **Write risk:** read-only lookup; quota and billing risk.

### Mapbox (Access Token)
```bash
curl -s "https://api.mapbox.com/geocoding/v5/mapbox.places/Test.json?access_token=$MAPBOX_TOKEN" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('features'))"
```
- **Valid:** JSON with `features` array.
- **Invalid:** `401` or JSON with `message`.
- **Scope probe:** token scopes are encoded in the token (`pk`, `sk`, `tk`) and can be decoded.
- **Write risk:** secret tokens can mutate account resources; public tokens are safer to validate.

### Branch.IO (Key and Secret)
```bash
curl -s "https://api2.branch.io/v1/branch_key?branch_key=$BRANCH_KEY" | python3 -m json.tool | head -20
```
- **Valid:** JSON with app details or `default_link` information.
- **Invalid:** `400`/`401` with `Resource not found` or auth message.
- **Scope probe:** branch key scopes are visible in dashboard.
- **Write risk:** key plus secret can create links; secret can alter routing.

### Heroku (API Key)
```bash
curl -s "https://api.heroku.com/account" \
  -H "Authorization: Bearer $HEROKU_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3"
```
- **Valid:** JSON containing `email` and `id`.
- **Invalid:** `401` with `Invalid credentials`.
- **Scope probe:** `GET /apps` reveals owned apps but is read-only.
- **Write risk:** key can provision, deploy, and remove apps if misused.

## Developer & Code Platforms

### GitHub (OAuth Client ID and Client Secret)
```bash
curl -s -o /dev/null -w '%{http_code}' \
  "https://api.github.com/users/whatever?client_id=$GITHUB_CLIENT_ID&client_secret=$GITHUB_CLIENT_SECRET"
```
- **Valid:** `200` with higher rate limits.
- **Invalid or revoked secret:** `401` or `403` with client authentication failures.
- **Scope probe:** these credentials only increase rate limit; they do not grant user identity.
- **Write risk:** negligible map mutations; check quotas and billing.

### GitLab (Runner Registration Token)
```bash
docker run --rm gitlab/gitlab-runner register \
  --non-interactive \
  --url https://gitlab.com/ \
  --registration-token "$RUNNER_TOKEN" \
  --executor shell \
  --name read-only-probe \
  --tag-list probe
```
- **Valid:** runner registration success message.
- **Invalid:** `403` or `invalid token` error.
- **Scope probe:** registration creates a runner record.
- **Write risk:** this probe **mutates** GitLab by registering a self-hosted runner. Prefer PAT validation instead, or clean up the registration immediately.

### CircleCI (Access Token)
```bash
curl -s "https://circleci.com/api/v1.1/me?circle-token=$CIRCLECI_TOKEN"
```
- **Valid:** JSON with `login`, `name`, and projects.
- **Invalid:** `401 Unauthorized`.
- **Scope probe:** `/projects` reveals admin/build capabilities.
- **Write risk:** token can trigger builds or manage contexts.

### Travis CI (API Token)
```bash
curl -s -H "Travis-API-Version: 3" \
  -H "Authorization: token $TRAVIS_TOKEN" \
  "https://api.travis-ci.org/repos"
```
- **Valid:** JSON list of repositories.
- **Invalid:** `401` or `403`.
- **Scope probe:** `/repos` implies repository and build visibility.
- **Write risk:** token can restart builds, deploy, or manage settings.

### Buildkite (Access Token)
```bash
curl -s -H "Authorization: Bearer $BUILDKITE_TOKEN" \
  "https://api.buildkite.com/v2/access-token"
```
- **Valid:** JSON with `scopes` and `uuid`.
- **Invalid:** `401` or `403` with `invalid_token`.
- **Scope probe:** scopes disclose repository and build access.
- **Write risk:** token can create builds or mutate pipelines.

### Visual Studio App Center (API Token)
```bash
curl -s -H "X-API-Token: $APP_CENTER_TOKEN" \
  "https://api.appcenter.ms/v0.1/apps"
```
- **Valid:** JSON array of app objects.
- **Invalid:** `401 Unauthorized`.
- **Scope probe:** returned apps reveal ownership and collaborators.
- **Write risk:** token can release, distribute, or manage apps.

### Cypress (Record Key)
```bash
curl -s -X POST "https://api.cypress.io/runs" \
  -H "Content-Type: application/json" \
  -d '{"recordKey":"'"$CYPRESS_KEY"'","projectId":"'"$PROJECT_ID"'"}'
```
- **Valid:** `200` with run record ID/details.
- **Invalid:** `401 Unauthorized` or `404 Project not found`.
- **Scope probe:** response may include run metadata.
- **Write risk:** this endpoint registers/runs a test execution path; use only approved project identifiers.

### SonarCloud (User Token)
```bash
curl -s -u "$SONARCLOUD_TOKEN:" "https://sonarcloud.io/api/authentication/validate"
```
- **Valid:** `{"valid":true}`.
- **Invalid:** `{"valid":false}` or `401`.
- **Scope probe:** token scope reveals project administration rights.
- **Write risk:** token can create or update projects and analysis settings.

### WakaTime (API Key)
```bash
curl -s "https://wakatime.com/api/v1/users/current?api_key=$WAKATIME_KEY"
```
- **Valid:** JSON with `data.email` and coding activity.
- **Invalid:** `401 Unauthorized`.
- **Scope probe:** response includes language and project statistics.
- **Write risk:** read-only API key should only read stats; higher scopes can mutate.

### Asana (Access Token)
```bash
curl -s -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/users/me"
```
- **Valid:** JSON with `gid` and `name`.
- **Invalid:** `401` with `Not Authorized`.
- **Scope probe:** `/workspaces` reveals workspace access.
- **Write risk:** token can create/modify tasks and projects.

### Pendo (Integration Key)
```bash
curl -s -H "content-type: application/json" \
  -H "x-pendo-integration-key: $PENDO_KEY" \
  "https://app.pendo.io/api/v1/feature"
```
- **Valid:** JSON list of features.
- **Invalid:** `401`/`403`.
- **Scope probe:** metadata schema endpoint reveals instrumentation fields.
- **Write risk:** integration key can send event data and update Pendo content.

## Communication & Collaboration

### Twitter (API Key and API Secret)
```bash
curl -s -u "$TWITTER_API_KEY:$TWITTER_API_SECRET" \
  --data 'grant_type=client_credentials' \
  "https://api.twitter.com/oauth2/token"
```
- **Valid:** JSON with `access_token` and `token_type`.
- **Invalid:** `403` with `invalid_client` or `401`.
- **Scope probe:** returned bearer token scopes determine later access.
- **Write risk:** issuing tokens can enable further API use; avoid posting.

### Twitter (Bearer Token)
```bash
curl -s --request GET \
  --url https://api.twitter.com/1.1/account_activity/all/subscriptions/count.json \
  --header "authorization: Bearer $TWITTER_BEARER_TOKEN"
```
- **Valid:** JSON counts or `null` payload.
- **Invalid:** `401 Unauthorized`.
- **Scope probe:** response reveals subscription status.
- **Write risk:** account activity endpoint is read-only.

### HubSpot (API Key)
```bash
curl -s "https://api.hubapi.com/owners/v2/owners?hapikey=$HUBSPOT_KEY" \
  | python3 -c "import sys,json;print(len(json.load(sys.stdin))) if isinstance(json.load(open('/dev/stdin')),list) else 'n/a')"
```
- **Valid:** JSON list of owners or `[]`.
- **Invalid:** `401` or `403` with `INVALID_API_KEY`.
- **Scope probe:** contacts endpoint reveals CRM records.
- **Write risk:** API key can create, update, delete CRM records.

### Microsoft Teams (Incoming Webhook URL)
```bash
curl -s -H "Content-Type:application/json" \
  -d '{"text":""}' \
  "$TEAMS_WEBHOOK_URL"
```
- **Valid:** 200 or body `Summary or Text is required.`.
- **Invalid:** `Invalid webhook URL`, 400/404.
- **Scope probe:** no scope data; webhook points to a single channel.
- **Write risk:** a non-empty payload posts into the channel.

### PagerDuty (API Token)
```bash
curl -s -H "Authorization: Token token=$PAGERDUTY_TOKEN" \
  -H "Accept: application/vnd.pagerduty+json;version=2" \
  "https://api.pagerduty.com/schedules"
```
- **Valid:** JSON with `schedules` array.
- **Invalid:** `401`/`403` with `Invalid Authorization` field.
- **Scope probe:** endpoints reveal on-call, incidents, and services.
- **Write risk:** token can create incidents or alter schedules.

### Zapier (Webhook Token URL)
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"probe":"non-mutating-liveness-check","source":"api-key-leak-validation"}' \
  "$ZAPIER_WEBHOOK_URL"
```
- **Valid:** 200 with `success`.
- **Invalid:** 404 webhook not found or rejected body.
- **Scope probe:** none.
- **Write risk:** triggers downstream automation (mutating), even on empty/dummy payload.

## Email & Marketing

### Mailchimp (API Key)
```bash
export DC="${MAILCHIMP_KEY##*-}"
curl -s --user "anystring:$MAILCHIMP_KEY" \
  "https://$DC.api.mailchimp.com/3.0/" | python3 -m json.tool | head -20
```
- **Valid:** JSON with `_links` and API root metadata.
- **Invalid:** `401` with `Your API key may be invalid`.
- **Scope probe:** lists endpoint shows audience size.
- **Write risk:** key can send campaigns or alter audiences.

### Zendesk (API Token)
```bash
curl -s -u "$ZENDESK_EMAIL/token:$ZENDESK_TOKEN" \
  "https://${ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/users.json"
```
- **Valid:** JSON with `users` array.
- **Invalid:** `401` or `403`.
- **Scope probe:** endpoints reveal ticket and user counts.
- **Write risk:** token can create or modify tickets and users.

### Zendesk (OAuth Access Token)
```bash
curl -s -H "Authorization: Bearer $ZENDESK_OAUTH_TOKEN" \
  "https://${ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets.json"
```
- **Valid:** JSON with `tickets` array.
- **Invalid:** `401` with OAuth token failure.
- **Scope probe:** `/tickets` and related endpoints disclose scope.
- **Write risk:** token can create, update, or delete support tickets.

### Freshdesk (API Key)
```bash
curl -s -u "$FRESHDESK_KEY:test" -X GET \
  "https://${FRESHDESK_DOMAIN}.freshdesk.com/api/v2/tickets"
```
- **Valid:** JSON list or `[]`.
- **Invalid:** `401` or `403`.
- **Scope probe:** `/tickets` endpoint confirms key access.
- **Write risk:** key can create or alter support records.

### ButterCMS (API Key)
```bash
curl -s "https://api.buttercms.com/v2/posts/?auth_token=$BUTTERCMS_KEY"
```
- **Valid:** JSON with `data` and pagination.
- **Invalid:** 401/403 or empty auth error.
- **Scope probe:** posts endpoint reveals blog content.
- **Write risk:** write or media token can alter CMS content.

## Payment Gateways

### PayPal (Client ID and Client Secret)
```bash
curl -s -u "$PAYPAL_CLIENT_ID:$PAYPAL_CLIENT_SECRET" \
  -H "Accept: application/json" \
  -d "grant_type=client_credentials" \
  "https://api.sandbox.paypal.com/v1/oauth2/token"
```
- **Valid:** JSON containing `access_token`.
- **Invalid:** `401` with `invalid_client`.
- **Scope probe:** token response may include granted scope.
- **Write risk:** credentials can invoice, payout, or refund depending on scope.

### Razorpay (Key ID and Key Secret)
```bash
curl -s -u "$RAZORPAY_KEY_ID:$RAZORPAY_KEY_SECRET" \
  "https://api.razorpay.com/v1/payments?count=1"
```
- **Valid:** JSON with `items` array.
- **Invalid:** `401 Unauthorized` or `400` authentication error.
- **Scope probe:** payments list indicates transactional data access.
- **Write risk:** credentials can capture or refund payments.

### Square (Access Token)
```bash
curl -s -H "Authorization: Bearer $SQUARE_TOKEN" \
  "https://connect.squareup.com/v2/locations"
```
- **Valid:** JSON with `locations` array.
- **Invalid:** 401 with error.
- **Scope probe:** locations and merchant identify account.
- **Write risk:** token may create orders, payments, or refunds.

## AI & Analytics

### Keen.io (API Key)
```bash
curl -s "https://api.keen.io/3.0/projects/$KEEN_PROJECT_ID/queries/extraction?event_collection=pageviews&timezone=UTC&latest=1" \
  -H "Authorization: $KEEN_API_KEY"
```
- **Valid:** JSON with `data` or empty extraction list.
- **Invalid:** 400/401/403 response.
- **Scope probe:** project-level extraction exposes analytics.
- **Write risk:** key can write event data and manage project.

### Amplitude (API Key and Secret Key)
```bash
curl -s "https://amplitude.com/api/2/export?start=20240101T00&end=20240101T23" \
  -u "$AMPLITUDE_API_KEY:$AMPLITUDE_SECRET_KEY" -o /tmp/amplitude.zip -w '%{http_code}'
```
- **Valid:** `200` and a ZIP archive.
- **Invalid:** `401` or `403`.
- **Scope probe:** export endpoint reveals project names and schemas.
- **Write risk:** ingestion or admin endpoints are write; avoid them.

### ABTasty (API Key)
```bash
curl -s -H "x-api-key: $ABTASTY_KEY" "https://api.abtasty.com/campaigns?limit=1"
```
- **Valid:** JSON list or metadata.
- **Invalid:** 401/403.
- **Scope probe:** campaigns endpoint indicates client or server API scope.
- **Write risk:** key can manage campaigns and flags.

### Iterable (API Key)
```bash
curl -s -H "Api-Key: $ITERABLE_KEY" \
  "https://api.iterable.com/api/campaigns?pageSize=1"
```
- **Valid:** JSON with campaign list.
- **Invalid:** `401 Unauthorized`.
- **Scope probe:** user and template endpoints reveal account data.
- **Write risk:** key can send messages and modify campaigns.

### YouTube Data (API Key)
```bash
curl -s "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=dQw4w9WgXcQ&key=$YOUTUBE_KEY" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('valid' if d.get('items') else d.get('error',{}).get('message'))"
```
- **Valid:** JSON `items` array.
- **Invalid:** error about `API key not valid`.
- **Scope probe:** listed items limited by key application restrictions.
- **Write risk:** none data mutation; quota and billing risk.

### LinkedIn OAuth (Client ID and Client Secret)
```bash
curl -s -X POST "https://www.linkedin.com/oauth/v2/accessToken" \
  -d "grant_type=client_credentials" \
  -d "client_id=$LINKEDIN_ID" \
  -d "client_secret=$LINKEDIN_SECRET"
```
- **Valid:** JSON with `access_token`.
- **Invalid:** JSON error with `invalid_client`.
- **Scope probe:** access token capabilities depend on approved scopes.
- **Write risk:** client credentials met all linked-in network APIs; avoid application submitted data.

### Help Scout (OAuth Access Token)
```bash
curl -s -X POST "https://api.helpscout.net/v2/oauth2/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$HELP_SCOUT_ID" \
  -d "client_secret=$HELP_SCOUT_SECRET"
```
- **Valid:** JSON with `token_type`, `access_token`, `expires_in`.
- **Invalid:** `unauthorized_client` or `invalid_client`.
- **Scope probe:** returned token scopes determine mailbox API access.
- **Write risk:** client can create and modify conversation messages.

## Search & Maps

### Algolia (Application ID and API Key)
```bash
curl -s -H "X-Algolia-API-Key: $ALGOLIA_KEY" \
  "https://$ALGOLIA_APP_ID.algolia.net/1/indexes/*/queries" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -d '{"requests":[{"indexName":"test","params":"query=foo"}]}'
```
- **Valid:** JSON with `results` array.
- **Invalid:** `403` with `Invalid Application-Id or API key`.
- **Scope probe:** restricted API keys expose only permitted indexes and operations.
- **Write risk:** admin keys can mutate records and settings; search keys should not.

## Monitoring & Observability

### New Relic (NerdGraph Personal API Key)
```bash
curl -s -X POST https://api.newrelic.com/graphql \
  -H "Content-Type: application/json" -H "Api-Key: $NEWRELIC_KEY" \
  -d '{"query":"{actor{user{email name}}}"}'
```
- **Valid:** JSON with actor.user data.
- **Invalid:** `401` or GraphQL with `Unauthorized`.
- **Scope probe:** additional queries can reveal account IDs and apps.
- **Write risk:** API key can manage entities and delete data.

### New Relic (REST API Key)
```bash
curl -s -X GET 'https://api.newrelic.com/v2/applications.json' \
  -H "X-Api-Key: $NEWRELIC_REST_KEY"
```
- **Valid:** JSON with `applications` array.
- **Invalid:** `401 Unauthorized`.
- **Scope probe:** application and metric visibility.
- **Write risk:** key can alter alerts/locations/labels.

### OpsGenie (API Key)
```bash
curl -s -H "Authorization: GenieKey $OPSGENIE_KEY" \
  "https://api.opsgenie.com/v2/alerts?limit=1"
```
- **Valid:** JSON with `data` array.
- **Invalid:** 401/403.
- **Scope probe:** alerts API reveals responders and teams.
- **Write risk:** key can create alerts, close incidents, or manage teams.

### Grafana (Access Token)
```bash
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "http://$GRAFANA_HOST/api/user"
```
- **Valid:** JSON with `login` and `orgId`.
- **Invalid:** 401.
- **Scope probe:** `/orgs`, `/datasources` reveal instance data.
- **Write risk:** token can create, read, or delete dashboards/data sources.

### Shodan (API Key)
```bash
curl -s "https://api.shodan.io/notifier?key=$SHODAN_KEY" \
  | python3 -m json.tool | head -20
```
- **Valid:** JSON with notifier list; account plan visible.
- **Invalid:** 401/403.
- **Scope probe:** `/account/profile` reveals credits and plan.
- **Write risk:** read-only search API; quotas and credits are main risk.

## CMS & Commerce

### Contentful (Content Delivery or Management Token)
```bash
curl -s "https://cdn.contentful.com/spaces/$CONTENTFUL_SPACE/entries?access_token=$CONTENTFUL_TOKEN&limit=1" \
  | python3 -m json.tool | head -20
```
- **Valid:** JSON with `items` array.
- **Invalid:** 401 with `The access token you provided is invalid`.
- **Scope probe:** space and environment IDs reveal access shape.
- **Write risk:** CMA/preview tokens can mutate or expose drafts.

### Bazaarvoice (Conversations Passkey)
```bash
curl -s --insecure "https://which-cpv-api.bazaarvoice.com/clientInfo?conversationspasskey=$BAZAARVOICE_PASSKEY" \
  | python3 -m json.tool | head -20
```
- **Valid:** JSON with `companyName`.
- **Invalid:** error body and no `companyName`.
- **Scope probe:** clientInfo response reveals site configuration.
- **Write risk:** write-capable tokens can submit reviews; this probe is read.

### WeGlot (API Key)
```bash
curl -s -X POST "https://api.weglot.com/translate" \
  -H "Content-Type: application/json" \
  -d '{"api_key":"'"$WEGLOT_KEY"'","bot":0,"l_from":"en","l_to":"fr","request_url":"https://example.com","words":[{"t":1,"w":"hello"}]}'
```
- **Valid:** translation response with translated words.
- **Invalid:** JSON with `error` and `invalid_api_key`.
- **Scope probe:** account scope reflected in billing response.
- **Write risk:** translation API allows content conversion but not account mutation.

### Salesforce (Access Token)
```bash
curl -s "https://${INSTANCE}.salesforce.com/services/data/v20.0/" \
  -H "Authorization: Bearer $SALESFORCE_TOKEN"
```
- **Valid:** JSON with resource definitions.
- **Invalid:** `401` or `INVALID_SESSION_ID`.
- **Scope probe:** SOQL/read endpoints disclose object and data access.
- **Write risk:** OAuth scopes may include object write/modify.

## Databases & BaaS

### Dropbox (Access Token)
```bash
curl -s -X POST "https://api.dropboxapi.com/2/users/get_current_account" \
  -H "Authorization: Bearer $DROPBOX_TOKEN"
```
- **Valid:** JSON with `account_id` and `email`.
- **Invalid:** `401` with `{"error_summary":"invalid_access_token"}`.
- **Scope probe:** app permissions reflected in user response.
- **Write risk:** token can read, write, or delete stored files depending on scope.

## CI/CD & Hosting

### WPEngine (API Credentials)
```bash
curl -s -u "$WPENGINE_USER:$WPENGINE_PASS" \
  "https://wpengineapi.com/v1/accounts"
```
- **Valid:** JSON list of accounts/sites or permissions.
- **Invalid:** 401/403.
- **Scope probe:** sites and accounts list discloses account model.
- **Write risk:** credentials can redeploy, back up, or modify WP Engine installs.

## Auth & Identity

### DeviantArt (Client Secret)
```bash
curl -s "https://www.deviantart.com/oauth2/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$DA_CLIENT_ID" \
  -d "client_secret=$DA_CLIENT_SECRET"
```
- **Valid:** JSON with `access_token`.
- **Invalid:** `invalid_client`.
- **Scope probe:** granted client credentials scope.
- **Write risk:** depending on scopes, may post or interact with accounts.

### DeviantArt (Access Token)
```bash
curl -s "https://www.deviantart.com/api/v1/oauth2/placebo" \
  -d "access_token=$DA_ACCESS_TOKEN"
```
- **Valid:** `{"status":"success"}`.
- **Invalid:** `{"status":"error"}` or `401`.
- **Scope probe:** placebo verifies token without app context required.
- **Write risk:** token scope determines any further action.

### Google reCAPTCHA (Secret Key)
```bash
curl -s -X POST "https://www.google.com/recaptcha/api/siteverify" \
  -d "secret=$RECAPTCHA_SECRET" \
  -d "response=dummy-response-value"
```
- **Valid shape:** JSON with `success` field (false due dummy response can mean key is accepted syntactically).
- **Invalid key:** response typically includes `success: false` with `error-codes` such as `invalid-input-secret`.
- **Scope probe:** no scoping beyond site registration.
- **Write risk:** secret should only validate captcha responses; abuse can consume verification quota.

### PivotalTracker (API Token)
```bash
curl -s "https://www.pivotaltracker.com/services/v5/me" \
  -H "X-TrackerToken: $PIVOTAL_TOKEN"
```
- **Valid:** JSON with user and project memberships.
- **Invalid:** 401/403.
- **Scope probe:** membership list reveals projects.
- **Write risk:** token can read and modify stories, iterations, and releases.

## Media & CDN

### Instagram (Basic Display Access Token)
```bash
curl -s "https://graph.instagram.com/me?fields=id,username&access_token=$INSTAGRAM_TOKEN"
```
- **Valid:** JSON with `id` and `username`.
- **Invalid:** error with `OAuthException` or token expired.
- **Scope probe:** granted fields limited by OAuth permissions.
- **Write risk:** token can publish or manage content only with publish scopes.

### Instagram (Graph API Access Token)
```bash
curl -s "https://graph.facebook.com/v8.0/me/accounts?access_token=$INSTAGRAM_GRAPH_TOKEN"
```
- **Valid:** JSON with page list.
- **Invalid:** error response with `OAuthException`.
- **Scope probe:** account list reveals pages/IG accounts.
- **Write risk:** token can publish to pages or manage accounts.

### Spotify (Access Token)
```bash
curl -s -H "Authorization: Bearer $SPOTIFY_TOKEN" \
  "https://api.spotify.com/v1/me"
```
- **Valid:** JSON with `id` and `display_name`.
- **Invalid:** 401 with `Invalid access token`.
- **Scope probe:** granted scopes visible through profile.
- **Write risk:** scopes may allow reading private playlists or modifying content per granted permissions.

### Delighted (API Key)
```bash
curl -s -u "$DELIGHTED_KEY:" \
  "https://api.delighted.com/v1/metrics.json" | python3 -m json.tool | head -20
```
- **Valid:** JSON with NPS metrics.
- **Invalid:** 401/403.
- **Scope probe:** metrics reveal satisfaction data.
- **Write risk:** token can create surveys or modify campaigns.

## Attribution

Coverage pattern and many provider endpoint concepts informed by:

- `streaak/keyhacks` — unlicensed (no LICENSE file found at review time; README-only distribution). This companion document was independently written from official API documentation, not copied from that repository. Where an upstream example would mutate state, this document replaces it with a read-only endpoint or marks the operation as write-risk.
- Official vendor API documentation linked inline where upstream provided links.

## Porting Checklist For A New Provider

1. Verify endpoint in official vendor docs.
2. Confirm method is non-mutating (`GET` or a read-only query). Mark `Write risk: mutates` for anything that creates, updates, sends, executes, or charges.
3. Record exact valid response signature (`JSON field`, `HTTP status`, `scope header`) and exact invalid signature (`401`, `403`, error-code).
4. Keep command fully parameterized with shell variables, never embed a live secret.
5. Add category grouping plus one `### Provider (credential type)` entry.
6. Mask all live values to last four characters in notes and report artifacts.
7. Add provider to up-stream question/ticket if safe liveness check cannot be found.
8. Keep commands POSIX `bash` compatible and rate-limit aware.
