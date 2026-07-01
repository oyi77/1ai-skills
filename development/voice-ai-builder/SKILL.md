---
name: voice-ai-builder
description: Build voice-based AI agents for phone calls, meetings, customer support, and sales qualification using Vapi,
  Bland, and Retell. Use when building voice-based ai agents for phone calls, meetings, customer support,.
domain: development
tags:
- ai-agent
- api
- builder
- coding
- software-engineering
- testing
- voice
---


## Overview

Build and deploy AI voice agents that handle phone calls, meetings, customer support, and sales qualification. The voice AI market (Vapi, Bland, Retell) is exploding — solo operators sell voice agent services to local businesses for $500-$2000/month per agent. This skill covers the full lifecycle: platform selection, agent design, call flow scripting, deployment, monitoring, and cost management.

## Required Tools

- **Platform SDK**: Vapi (`@vapi-ai/web`), Bland API, or Retell SDK (`retell-sdk`)
- **LLM Provider**: OpenAI, Anthropic, or custom model endpoint
- **Telephony**: Twilio (for custom phone numbers), or platform-provided numbers
- **Monitoring**: Platform dashboards + custom logging via webhook callbacks
- **Node.js 18+** for SDK usage
- **API keys** for chosen platform

## Capabilities

- Design voice agents for inbound/outbound calls
- Script multi-turn conversation flows with branching logic
- Handle interruptions, barge-in, and natural pauses
- Integrate with CRM (HubSpot, Salesforce) for call logging
- Transfer calls to human agents when needed
- Record and transcribe calls for quality assurance
- Manage phone numbers and SIP trunking
- Monitor call quality, latency, and cost per call
- A/B test different voice personas and scripts

## When to Use
**Trigger phrases:**
- "voice ai builder"
- "Build voice-based AI agents for phone calls, meetings, customer support, and sal"


- Client wants AI to handle inbound support calls
- Sales team needs AI-qualified leads before human handoff
- Appointment booking via phone without human receptionist
- Outbound calling campaigns for lead qualification
- Local business wants 24/7 phone coverage
- Survey or feedback collection via voice

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The voice-ai-builder workflow follows a standard pipeline pattern.

Core flow:
```
# voice-ai-builder primary flow
input = prepare(raw_data)
result = process(input, config={agents, based, bland, build, builder})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Platform Selection

```
USE_CASE = "customer_support" | "sales_qualification" | "appointment_booking" | "outbound_campaign"

if USE_CASE == "customer_support":
    PLATFORM = "vapi"          # Best for complex multi-turn, interruption handling
elif USE_CASE == "sales_qualification":
    PLATFORM = "retell"        # Best for natural conversation, lower latency
elif USE_CASE == "outbound_campaign":
    PLATFORM = "bland"         # Best for high-volume outbound, batch calling
elif USE_CASE == "appointment_booking":
    PLATFORM = "vapi"          # Best tool/function calling for calendar integration
```

### Agent Design (Vapi Example)

```javascript
import Vapi from "@vapi-ai/web";

const vapi = new Vapi(process.env.VAPI_API_KEY);

const agent = {
  name: "Support Agent",
  model: {
    provider: "openai",
    model: "gpt-4o",
    temperature: 0.7,
    systemMessage: `You are a helpful support agent for {company_name}.
      - Be concise and professional
      - If you cannot help, offer to transfer to a human
      - Never make up information about products or pricing`,
    functions: [
      {
        name: "lookup_order",
        description: "Look up order status by order number",
        parameters: {
          type: "object",
          properties: {
            orderNumber: { type: "string", description: "Order number" }
          },
          required: ["orderNumber"]
        }
      },
      {
        name: "transfer_to_human",
        description: "Transfer call to human agent",
        parameters: {
          type: "object",
          properties: {
            reason: { type: "string", description: "Transfer reason" }
          }
        }
      }
    ]
  },
  voice: {
    provider: "11labs",
    voiceId: "rachel",  // Professional female voice
    stability: 0.5,
    similarityBoost: 0.75
  },
  firstMessage: "Hi! Thanks for calling {company_name}. How can I help you today?",
  endCallMessage: "Thanks for calling! Have a great day.",
  silenceTimeoutSeconds: 30,
  maxDurationSeconds: 600,  // 10 min max call
  recordingEnabled: true,
  transcriptionEnabled: true
};

// Start call
const call = await vapi.start(agent);
```

### Call Flow Scripting

```javascript
// Define call flow states
const CALL_FLOW = {
  greeting: {
    message: "Hi! How can I help you today?",
    next: "intent_detection"
  },
  intent_detection: {
    // LLM determines intent from user speech
    routes: {
      "order_inquiry": "order_lookup",
      "complaint": "complaint_handling",
      "general_question": "faq",
      "human_request": "transfer"
    }
  },
  order_lookup: {
    message: "Let me look that up for you. What's your order number?",
    function: "lookup_order",
    next: "order_result"
  },
  order_result: {
    message: "Your order {order.status} and is expected to arrive on {order.delivery_date}.",
    next: "anything_else"
  },
  transfer: {
    message: "Let me connect you with a team member.",
    function: "transfer_to_human",
    endCall: false
  },
  anything_else: {
    message: "Is there anything else I can help with?",
    routes: {
      "yes": "intent_detection",
      "no": "goodbye"
    }
  },
  goodbye: {
    message: "Thanks for calling! Have a great day.",
    endCall: true
  }
};
```

### Outbound Campaign (Bland)

```javascript
// Batch outbound calls via Bland
const BATCH_CALLS = [
  { phone: "+1234567890", variables: { name: "John", company: "Acme" } },
  { phone: "+0987654321", variables: { name: "Jane", company: "Beta" } }
];

for (const contact of BATCH_CALLS) {
  await fetch("https://api.bland.ai/v1/calls", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.BLAND_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      phone_number: contact.phone,
      task: `Hi ${contact.variables.name}, this is an AI assistant calling about ${contact.variables.company}. Would you be interested in a quick demo?`,
      voice: "josh",
      reduce_latency: true,
      record: true,
      webhook: "https://your-server.com/call-callback"
    })
  });
}
```

### Deployment & Monitoring

```bash
# Deploy webhook server for call events
# Express.js server handling Vapi webhooks
app.post("/webhook/vapi", (req, res) => {
  const { event, call } = req.body;

  switch (event) {
    case "call-start":
      log("Call started", call.id, call.customer.number);
      break;
    case "call-end":
      log("Call ended", call.id, call.duration, call.cost);
      metrics.recordCall(call);
      break;
    case "function-call":
      handleFunctionCall(call.function_name, call.parameters);
      break;
  }
  res.sendStatus(200);
});

# Monitor metrics
# Cost per call: $0.05-$0.15/min (Vapi) or $0.09/min (Bland)
# Target: < 500ms latency, < 2% transfer rate for simple queries
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `ELEVENLABS_QUOTA` | Voice synthesis quota exceeded | Switch to fallback voice provider or queue calls |
| `CALL_TIMEOUT` | User silent for 30+ seconds | Play prompt "Are you still there?" then end call |
| `FUNCTION_TIMEOUT` | External API call took >5s | Return "Let me look into that" and retry once |
| `HIGH_LATENCY` | Response time > 2s | Switch to faster model (gpt-4o-mini) or reduce context |
| `TRANSCRIPTION_FAIL` | STT couldn't process audio | Ask caller to repeat, log audio for review |
| `TRANSFER_FAIL` | Human agent unavailable | Take message, promise callback within 1 hour |

## Common Patterns

Proven patterns for voice-ai-builder usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Sales Qualification Flow
1. Greet and establish rapport (5 seconds)
2. Ask qualifying questions (budget, timeline, authority, need)
3. Score lead based on answers
4. If qualified: book meeting via calendar API
5. If not qualified: thank and end gracefully
6. Log to CRM with qualification score

### Appointment Booking Pattern
1. Ask what service they need
2. Check availability via calendar API
3. Offer 2-3 time slots
4. Confirm booking and send confirmation SMS
5. Add to calendar and CRM

### Cost Management
- Use `gpt-4o-mini` for simple FAQ (90% cheaper)
- Cache common responses to avoid LLM calls
- Set max call duration to prevent runaway costs
- Monitor cost-per-outcome (not just cost-per-call)
- Target: $0.10-$0.30 per successful resolution

### Multi-Language Support
- Detect language from first utterance
- Switch LLM system prompt to detected language
- Use multilingual voice models (11labs supports 29 languages)
- Maintain language-specific call flow templates

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |