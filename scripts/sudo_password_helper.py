#!/usr/bin/env python3
"""
Helper script to read password from PTY for sudo commands
"""
import sys
import pty
import sys
import os
import subprocess

def read_password(prompt):
    """Read password from PTY"""
    # Open PTY
    master_fd, slave_fd = pty.openpty()

    try:
        # Set slave as controlling terminal
        os.setsid()
        os.setctty()

        # Send prompt
        os.write(slave_fd, prompt.encode())

        # Switch slave to raw mode
        import tty
        old_settings = tty.tcgetattr(slave_fd)
        tty.setraw(slave_fd)

        # Read password
        password_bytes = b""
        while True:
            r, w, e = select.select([slave_fd], [], [], 0.1)
            if slave_fd in r:
                char = os.read(slave_fd, 1)
                
                # Check for Enter or Backspace
                if char == b'\r' or char == b'\n':
                    break
                elif char == b'\x7f':
                    password_bytes = password_bytes[:-1]
                    break
                elif char == b'\x03':
                    print("\n❌ Cancelled by user")
                    sys.exit(1)
                elif char == b'\x1b':
                    print("\n❌ Cancelled by user")
                    sys.exit(1)
                else:
                    password_bytes += char

        # Restore terminal settings
        tty.tcsetattr(slave_fd, old_settings)
        return password_bytes.decode('utf-8')

    finally:
        master_fd.close()
        slave_fd.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1:]
        password = read_password(f"[sudo] Password required for: {' '.join(command[:3])}{' ...) ")
        if password:
            # Add password to environment
            env = os.environ.copy()
            env['SUDO_ASKPASS'] = password
            try:
                subprocess.run(command, env=env)
                sys.exit(0)
            except subprocess.CalledProcessError as e:
                print(f"❌ Command failed with exit code {e.returncode}")
                sys.exit(e.returncode)
        else:
            print("❌ No password provided or cancelled")
            sys.exit(1)
    else:
        password = read_password("[sudo] Password: ")
        print("Password received:", "*" * len(password))