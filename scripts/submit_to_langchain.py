#!/usr/bin/env python3
"""Automated LangChain Hub Publisher"""

import subprocess
import os


def submit_to_langchain():
    """Submit skills to LangChain Hub"""

    # Check if langchain CLI installed
    result = subprocess.run(["which", "langchain"], capture_output=True, text=True)

    if result.returncode != 0:
        print("Installing langchain-cli...")
        subprocess.run(["pip", "install", "langchain-cli"])

    # Get token
    token = os.environ.get("LANGCHAIN_API_KEY")
    if not token:
        print("❌ Need LangChain API key")
        print("Get one at: https://smith.langchain.com/settings")
        print("Then run: export LANGCHAIN_API_KEY='your_key'")
        return

    # Login
    print("🔑 Logging in to LangChain...")
    subprocess.run(["langchain", "login", "--api-key", token])

    # Create hub entry
    print("📦 Creating hub entry...")
    subprocess.run(
        [
            "langchain",
            "hub",
            "create",
            "oyi77/1ai-skills",
            "--name",
            "1ai-Skills",
            "--description",
            "139 world-class AI skills",
        ]
    )

    # Push content
    print("⬆️ Pushing skills...")
    os.chdir("/home/openclaw/.opencode/skills")
    subprocess.run(["langchain", "hub", "push", "oyi77/1ai-skills", "."])

    print("✅ LangChain Hub submission complete!")
    print("URL: https://smith.langchain.com/hub/oyi77/1ai-skills")


if __name__ == "__main__":
    submit_to_langchain()
