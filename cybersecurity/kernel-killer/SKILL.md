---
name: kernel-killer
description: Linux and Windows kernel exploitation for privilege escalation. Use when finding kernel vulnerabilities, exploiting
  kernel drivers, or escalating privileges from user to root/system.
domain: cybersecurity
tags:
- cybersecurity
- kernel
- killer
- security
- threat-defense
---

# Kernel Killer

Kernel bugs = root access. One kernel exploit can give you full control of any system. These bugs are rare, hard to find, and pay $50k-$500k.

## When to Use

- Finding privilege escalation vulnerabilities
- Exploiting kernel drivers
- Analyzing kernel modules for bugs
- Escalating from user to root/system
- Breaking out of containers/sandboxes
- CTF kernel exploitation challenges

## The Process

1. **Scope and authorize** — confirm written authorization and define target boundaries
2. **Reconnaissance** — enumerate targets, services, and potential attack surfaces
3. **Exploitation** — attempt exploitation of identified vulnerabilities within scope
4. **Post-exploitation** — document access level, lateral movement, and data exposure
5. **Report and remediate** — compile findings with reproduction steps and fix recommendations
### 1. Kernel Reconnaissance

```bash
# Linux
uname -a
cat /proc/version
cat /boot/config-$(uname -r) | grep CONFIG_
lsmod  # loaded modules
cat /proc/modules

# Windows
systeminfo
wmic os get caption,version,buildnumber
driverquery
Get-WmiObject Win32_OperatingSystem
```

### 2. Kernel Vulnerability Classes

#### Stack Buffer Overflow
```c
// Kernel stack overflow
void vulnerable_ioctl(struct file *f, unsigned long arg) {
    char buf[64];
    copy_from_user(buf, (void *)arg, user_size);  // user_size not validated
    // Stack buffer overflow if user_size > 64
}

// Exploitation:
// 1. Overwrite return address on kernel stack
// 2. ROP chain to commit_creds(prepare_kernel_cred(0))
// 3. Return to userland with root
```

#### Heap Overflow (SLAB/SLUB)
```c
// Heap corruption in kernel
void vulnerable() {
    struct object *obj = kmalloc(64, GFP_KERNEL);
    copy_from_user(obj->data, user_buf, user_len);  // Overflow
    // Can corrupt adjacent heap objects
}

// Exploitation:
// 1. Spray heap with controlled objects
// 2. Overflow into adjacent object
// 3. Corrupt function pointer or privilege field
// 4. Trigger corrupted pointer → code execution
```

#### Use-After-Free
```c
// Kernel UAF
struct file_operations fops = {
    .read = vulnerable_read,
    .release = vulnerable_release,
};

int vulnerable_release(struct inode *i, struct file *f) {
    kfree(f->private_data);  // Free
    // But f->private_data still usable through other paths
}

// Exploitation:
// 1. Open device, trigger free
// 2. Spray heap to reclaim freed object
// 3. Overwrite with controlled data
// 4. Use original file descriptor → UAF → control flow hijack
```

#### Integer Overflow
```c
// Integer overflow in size calculation
size_t size = count * element_size;  // Overflow if large values
void *buf = kmalloc(size, GFP_KERNEL);
// If size wraps to small value, heap overflow on copy
```

### 3. Privilege Escalation Techniques

#### ret2usr (Linux < 5.x)
```c
// Allocate userland function at known address
void escalate() {
    commit_creds(prepare_kernel_cred(0));
}

// ROP chain returns to userland address
// Kernel executes userland code (if SMEP/SMAP disabled)
```

#### SMEP/SMAP Bypass
```c
// SMEP: Supervisor Mode Execution Prevention
// Can't execute userland pages from kernel mode

// Bypass: ROP in kernel text
// Find gadgets in kernel .text section
// Chain: pop rdi; ret → prepare_kernel_cred(0)
//        pop rdi; ret → commit_creds()
//        swapgs; iretq → return to userland

// SMAP: Supervisor Mode Access Prevention
// Can't access userland pages from kernel mode

// Bypass: Use kernel-only gadgets
// Modify CR4 register to disable SMAP
// Or use kernel data structures that reference userland
```

#### Dirty COW (CVE-2016-5195)
```c
// Race condition in copy-on-write
// Allows writing to read-only memory mappings
// Can overwrite /etc/passwd or SUID binaries

// Exploitation:
// 1. Memory-map read-only file
// 2. Write to mapping from one thread
// 3. madvise(MADV_DONTNEED) from another thread
// 4. Race condition allows write to underlying file
```

#### Dirty Pipe (CVE-2022-0847)
```c
// Overwrite arbitrary read-only files
// Pipe buffer flag PIPE_BUF_FLAG_CAN_MERGE not cleared

// Exploitation:
// 1. Create pipe
// 2. Fill pipe buffers with data
// 3. Drain pipe (flag not cleared)
// 4. Splice target file into pipe
// 5. Write to pipe → overwrites file data
// 6. Can overwrite SUID binary or /etc/passwd
```

### 4. Windows Kernel Exploitation

#### Kernel Pool Overflow
```
# Pool spraying to control layout
# Overflow into adjacent pool allocation
# Corrupt pool header → arbitrary read/write
# Target: win32k.sys, ntoskrnl.exe
```

#### Win32k Use-After-Free
```
# Common in window management
# TagWND, SURFOBJ, PEB structures
# Double-fetch from userland
# Race conditions in message handling
```

#### Token Stealing
```python
# Windows token stealing shellcode
# Find current process EPROCESS
# Copy SYSTEM process token
# Replace current process token

# EPROCESS chain:
# _KTHREAD → _KPROCESS → _EPROCESS
# ActiveProcessLinks → find SYSTEM
# Copy Token field
```

### 5. Container/Sandbox Escape

```bash
# Check for container escape vectors
# Mounted host filesystem
ls -la /proc/1/root/
cat /proc/1/cgroup

# Privileged container
capsh --print  # Check capabilities
# CAP_SYS_ADMIN, CAP_SYS_PTRACE = escape potential

# Kernel exploit from container
# If kernel is vulnerable, container escape possible
# Dirty Pipe, Dirty COW work from containers
```

### 6. Exploit Development Workflow

```
1. Trigger: Reproduce the bug reliably
2. Control: Demonstrate control of execution (RIP/EIP)
3. Stability: Exploit works without crashing
4. Privilege: Escalate to root/SYSTEM
5. Cleanup: Remove traces, restore state
```

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Exploiting production kernels without authorization
- Causing kernel panics on production systems
- Developing kernel exploits for malicious use
- Sharing kernel zero-days without responsible disclosure

## Verification

- Exploit works reliably (90%+ success rate)
- No kernel panics during exploitation
- Root/SYSTEM shell obtained
- Works on target kernel version
- Responsible disclosure completed

## Revenue Potential

| Target | Bug Type | Payout Range |
|--------|----------|--------------|
| Linux Kernel | Local Privesc | $50,000-$500,000 |
| Windows Kernel | Local Privesc | $50,000-$250,000 |
| Android Kernel | Local Privesc | $100,000-$1,000,000 |
| iOS Kernel | Sandbox Escape | $100,000-$500,000 |
| Container Escape | Kernel Bug | $10,000-$100,000 |
| Hypervisor Escape | VM Escape | $100,000-$500,000 |

## Tools

| Purpose | Tools |
|---------|-------|
| Debugging | GDB+KGDB, WinDbg, QEMU+GDB |
| Exploitation | pwntools, ROPgadget |
| Kernel modules | eBPF, LKM |
| Windows | WinDbg, IDA Pro, Ghidra |
| Sandboxing | Docker, QEMU, VirtualBox |

## Practice

- kernel-ctf (Google)
- HackTheBox (Kernel challenges)
- Exploit Education
- CVE reproduction (Linux, Android)

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
