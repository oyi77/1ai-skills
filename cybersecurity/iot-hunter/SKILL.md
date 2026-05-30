---
name: iot-hunter
description: IoT and embedded device security testing — firmware analysis, hardware interfaces, protocol exploitation. Use when testing IoT devices, extracting firmware, analyzing embedded systems, or finding hardware vulnerabilities.
---

# IoT Hunter

IoT devices are everywhere and most are insecure. Default credentials, unencrypted protocols, exposed debug interfaces. This skill covers finding and exploiting IoT vulnerabilities.

## When to Use

- Security assessment of IoT/embedded devices
- Firmware reverse engineering
- Hardware security testing
- Protocol analysis (MQTT, CoAP, Zigbee, BLE)
- Smart home/industrial IoT testing

## The Process

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### 1. Device Reconnaissance

```bash
# Network discovery
nmap -sn 192.168.1.0/24
arp-scan -l

# Service enumeration
nmap -sV -p- target

# Common IoT ports
22 (SSH), 23 (Telnet), 80 (HTTP), 443 (HTTPS)
1883 (MQTT), 8883 (MQTTS), 5683 (CoAP)
445 (SMB), 554 (RTSP), 161 (SNMP)
8080, 8443 (alternative web)
```

### 2. Firmware Analysis

#### Firmware Extraction
```bash
# Download from vendor website
# Intercept OTA update
# Dump from flash chip (physical)

# SPI flash dump
flashrom -p ch341a_spi -r firmware.bin

# UART bootloader
# Connect to UART pins (TX, RX, GND)
screen /dev/ttyUSB0 115200
# Interrupt boot, dump firmware
```

#### Firmware Analysis
```bash
# Extract filesystem
binwalk -e firmware.bin
firmwalker extracted/

# Look for:
# Hardcoded credentials
grep -r "password\|passwd\|admin\|root" extracted/
# Private keys
find extracted/ -name "*.pem" -o -name "*.key"
# URLs and API endpoints
grep -r "http\|api\|server" extracted/
# Command injection points
grep -r "system\|exec\|popen\|eval" extracted/
```

### 3. Hardware Interfaces

#### UART
```bash
# Find UART pins with multimeter/logic analyzer
# TX: transmits data (fluctuating voltage)
# RX: receives data
# GND: ground
# VCC: power (3.3V or 5V)

# Connect with USB-to-UART adapter
screen /dev/ttyUSB0 115200

# Common baud rates: 9600, 38400, 57600, 115200
# Try each until you get readable output
```

#### JTAG/SWD
```bash
# Debug interface for microcontrollers
# Can read/write flash, set breakpoints, dump memory

# Tools: OpenOCD, J-Link, Bus Pirate
openocd -f interface/stlink-v2.cfg -f target/stm32f1x.cfg

# Dump firmware via JTAG
dump_image firmware.bin 0x08000000 0x100000
```

#### SPI/I2C
```bash
# Flash chip interfaces
# SPI: 4 wires (MISO, MOSI, SCK, CS)
# I2C: 2 wires (SDA, SCL)

# Read flash with Bus Pirate
flashrom -p buspirate_spi:dev=/dev/ttyUSB0 -r firmware.bin
```

### 4. Protocol Analysis

#### MQTT
```bash
# Subscribe to all topics (if no auth)
mosquitto_sub -h broker -t '#' -v

# Common topics:
# /device/+/status
# /device/+/command
# /device/+/config
# /gateway/+/data

# If authenticated:
mosquitto_sub -h broker -t '#' -u admin -P password -v
```

#### CoAP
```bash
# CoAP is HTTP for constrained devices
# GET /.well-known/core (discover resources)
coap-client -m get coap://target/.well-known/core

# Common resources:
# /sensors
# /actuators
# /config
```

#### BLE (Bluetooth Low Energy)
```bash
# Scan for BLE devices
hcitool lescan

# Connect and enumerate services
gatttool -b MAC --primary
gatttool -b MAC --characteristics

# Read/write characteristics
gatttool -b MAC --char-read -a 0x0001
gatttool -b MAC --char-write -a 0x0001 -n 01
```

#### Zigbee
```bash
# Capture with KillerBee or Zigbee sniffer
# Analyze with Wireshark (Zigbee dissector)

# Common attacks:
# Replay captured packets
# Inject commands
# Extract network key (if weak)
```

### 5. Web Interface Testing

```bash
# Default credentials
admin:admin
root:root
admin:password
admin:(blank)
root:(blank)

# Try all common default credential lists
hydra -l admin -P /usr/share/wordlists/rockyou.txt target http-get /

# Command injection in web interface
# Test all input fields:
; ls
| whoami
$(cat /etc/passwd)
`id`
```

### 6. Common IoT Vulnerabilities

```
# Default credentials (most common)
# Unencrypted protocols (HTTP, Telnet, FTP)
# Command injection (web interface, API)
# Buffer overflow (firmware)
# Hardcoded credentials
# No authentication on APIs
# Insecure OTA updates
# Exposed debug interfaces (UART, JTAG)
# Weak/no encryption on wireless protocols
# No secure boot
```

### 7. Smart Home Specific

```bash
# Smart speakers
# Voice command injection
# Audio replay attacks
# API abuse

# Smart cameras
# RTSP stream access (default creds)
# Cloud API abuse
# Firmware backdoor

# Smart locks
# BLE replay attacks
# Zigbee command injection
# API authentication bypass
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Accessing other people's IoT devices
- Disrupting critical infrastructure
- Extracting personal data from devices
- Physical tampering without authorization
- Testing medical/industrial devices without safety measures

## Verification

- All findings demonstrated on actual device
- Default credentials tested and documented
- Firmware analysis results documented
- Protocol vulnerabilities demonstrated
- Physical access requirements documented

## Revenue Potential

| Target | Bug Type | Payout Range |
|--------|----------|--------------|
| Smart home devices | Default creds, API abuse | $500-$5,000 |
| Industrial IoT | Protocol vulnerabilities | $5,000-$50,000 |
| Router/Network | Firmware bugs, RCE | $5,000-$25,000 |
| Smart cameras | Stream access, cloud abuse | $1,000-$10,000 |
| Medical devices | Critical vulnerabilities | $10,000-$100,000 |
| Automotive | CAN bus, ECU exploitation | $10,000-$100,000 |

## Tools

| Purpose | Tools |
|---------|-------|
| Firmware | binwalk, firmwalker, FACT |
| Hardware | Bus Pirate, J-Link, flashrom |
| Protocol | Wireshark, mosquitto, KillerBee |
| Scanning | nmap, masscan |
| Debug | screen, minicom, OpenOCD |
| Analysis | Ghidra, radare2 |

## References

- OWASP IoT Security Verification Standard
- IoT Village (DEF CON)
- HackTheBox IoT challenges
- Firmwaresecurity.com
