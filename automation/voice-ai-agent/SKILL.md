---
name: voice-ai-agent
description: AI voice agent for handling incoming calls, appointment scheduling, lead qualification, and 24/7 customer service without human intervention.
---

# Voice AI Agent Skill

## Overview

Deploy AI voice agents to handle incoming calls, schedule appointments, qualify leads, and provide 24/7 customer service. Replace traditional receptionists with AI that never sleeps, never takes vacation, and costs a fraction of a human employee.

**Market**: $11.78B by 2026  
**ROI**: 391% average  
**Best For**: Small businesses, service providers, clinics, agencies

---

## When to Use

- Answer incoming calls 24/7
- Schedule appointments automatically
- Qualify leads in real-time
- Handle frequently asked questions
- Route calls to appropriate staff
- Collect caller information
- After-hours customer support

---

## When NOT to Use

- Complex emotional conversations
- Legal/medical advice requiring humans
- High-value negotiations
- Crisis situations

---

## Top Platforms

### Enterprise Grade
| Platform | Price | Best For |
|----------|-------|----------|
| Bland AI | From $0.01/min | Large scale |
| Vapi | $0.10/min | Developers |
| Retell | $0.15/min | Voice quality |
| Deepgram | Usage-based | Transcription |

### SMB Solutions
| Platform | Price | Best For |
|----------|-------|----------|
| OpenPhone AI | $15/user/mo | Small business |
| Google Voice AI | Included | Google ecosystem |
| Voiceflow | $50/mo | Custom agents |
| Bland AI | $0.05/min | Cost effective |

### Open Source
| Platform | Price | Best For |
|----------|-------|----------|
| LiveKit | Open source | Full control |
| Picovoice | Free tier | Privacy |
| Cartesia | Free tier | Real-time |

---

## Core Capabilities

### 1. Appointment Scheduling
- Calendar integration (Google, Calendly, Cal.com)
- Multi-timezone handling
- Conflict detection
- Confirmation SMS/email
- Reminder notifications

### 2. Lead Qualification
- Pre-qualification questions
- Budget assessment
- Needs identification
- Urgency detection
- CRM integration

### 3. FAQ Handling
- Product/service questions
- Pricing inquiries
- Hours/location
- Feature information
- Troubleshooting

### 4. Call Routing
- Department routing
- Priority escalation
- Voicemail capture
- Emergency handling

---

## Implementation

### Basic Setup (Bland AI)

```python
import bland

# Initialize client
client = bland.Client(api_key="your-api-key")

# Create voice agent
agent = client.agents.create(
    name="Receptionist",
    model="enhanced",
    voice_id="female-1",
    max_duration=300,
    transfer_phone_number="+1234567890"
)

# Handle incoming call
@app.route("/webhook", methods=["POST"])
def handle_call():
    response = client.responses.create(
        agent_id=agent.id,
        actions=[
            {"type": "say", "text": "Hello, thank you for calling..."},
            {"type": "collect", "field": "name"},
            {"type": "transfer", "to": "+1234567890"}
        ]
    )
    return response
```

### Calendar Integration

```python
# Book appointment
def book_appointment(date, time, customer_name, phone):
    event = calendar.events().insert(
        calendarId='primary',
        body={
            'summary': f'Appointment with {customer_name}',
            'start': {'dateTime': f'{date}T{time}:00'},
            'end': {'dateTime': f'{date}T{time}:30'}
        }
    ).execute()
    
    # Send confirmation
    send_sms(phone, f"Appointment confirmed for {date} at {time}")
```

---

## Use Cases by Industry

### Healthcare
- Appointment scheduling
- Prescription refills
- Insurance verification
- After-hours triage

### Real Estate
- Property inquiries
- Showing scheduling
- Pre-qualification
- Viewing confirmations

### Professional Services
- Consultation booking
- Quote requests
- Intake forms
- Client intake

### E-commerce
- Order status
- Returns processing
- Product questions
- Support escalation

---

## Integration with 1ai-skills

### Sales Pipeline

```
Incoming Call → Voice AI (qualify) → CRM → Sales Team → Close
```

### Customer Service

```
Call → Voice AI (FAQ) → Ticket → Human (if needed) → Resolve
```

### Skill Synergies

| Skill | Use Case |
|-------|----------|
| ai-lead-generation | Qualify leads |
| sales | Close deals |
| customer-support | Follow-up support |
| calendar-management | Scheduling |

---

## Pricing Models

### Per Minute
- $0.05-0.15/minute
- Pay for actual usage
- Best for low volume

### Monthly
- $50-500/month unlimited
- Predictable costs
- Best for high volume

### Hybrid
- Base fee + per minute
- Best of both worlds
- Most common

---

## Best Practices

### Do's
✅ Test extensively with diverse voices  
✅ Provide clear escalation paths  
✅ Keep responses under 30 seconds  
✅ Include fallback for failures  
✅ Monitor call quality metrics  
✅ Update knowledge base regularly  

### Don'ts
❌ Don't over-automate complex issues  
❌ Don't forget to update hours/holidays  
❌ Don't skip call recording review  
❌ Don't ignore caller feedback  

---

## Metrics to Track

| Metric | Target |
|--------|--------|
| Call completion rate | >95% |
| Appointment booked | >30% |
| Lead qualification | >50% |
| Customer satisfaction | >4/5 |
| Average handling time | <3 min |

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Platform comparisons
  - Implementation examples
  - Industry use cases

---

## Related Skills

- [ai-lead-generation](/skills/ai-lead-generation) - Lead qualification
- [sales](/skills/sales) - Close deals
- [customer-support](/skills/customer-support) - Support automation
