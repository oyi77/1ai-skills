#!/usr/bin/env python3
"""Content Generator CLI - Command-line interface for content generation."""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from batch_processor import BatchJob, BatchProcessor, JobStatus
from scheduler import Schedule, Scheduler

from platforms.base import Platform, PLATFORM_SPECS

from providers.base import AIProvider, GenerationResult, ProviderType
from providers.ollama import OllamaProvider
from providers.groq import GroqProvider
from providers.nvidia import NVIDIAProvider

from cache import Cache
from cost_tracker import CostTracker
from state import StateManager

PROVIDERS = {
    "ollama": OllamaProvider,
    "groq": GroqProvider,
    "nvidia": NVIDIAProvider,
}


def get_provider(provider_name: str, api_key: Optional[str] = None) -> AIProvider:
    """Get provider instance by name."""
    provider_class = PROVIDERS.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider_name}")
    return provider_class(api_key=api_key or os.getenv("API_KEY"))


def get_platform_spec(platform_name: str) -> Platform:
    """Get platform enum by name."""
    platform_name = platform_name.upper()
    try:
        return Platform[platform_name]
    except KeyError:
        raise ValueError(f"Unknown platform: {platform_name}")


async def generate_content(
    prompt: str,
    platform: Optional[str] = None,
    template: Optional[str] = None,
    strategy: Optional[str] = None,
    output: Optional[str] = None,
    provider_name: str = "ollama",
):
    """Generate content from a prompt."""
    print(f"Generating content for prompt: {prompt[:50]}...")

    provider = get_provider(provider_name)

    full_prompt = prompt
    if template:
        full_prompt = f"[Template: {template}] {prompt}"
    if strategy:
        full_prompt = f"[Strategy: {strategy}] {full_prompt}"

    result = await provider.generate(full_prompt)

    result_dict = {
        "success": result.success,
        "data": result.data,
        "cost": result.cost,
        "provider": result.provider,
        "model": result.model,
        "metadata": result.metadata,
    }

    if platform:
        platform_spec = get_platform_spec(platform)
        spec = PLATFORM_SPECS[platform_spec]
        result_dict["platform_spec"] = {
            "platform": platform_spec.value,
            "aspect_ratio": spec.aspect_ratio,
            "resolution": spec.resolution,
            "format": spec.format,
        }

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result_dict, f, indent=2, default=str)
        print(f"Content saved to: {output}")

    return result_dict


async def batch_generate(
    prompts: list[str],
    platform: Optional[str] = None,
    template: Optional[str] = None,
    strategy: Optional[str] = None,
    output: Optional[str] = None,
    provider_name: str = "ollama",
    max_concurrent: int = 3,
):
    """Generate content for multiple prompts."""
    print(f"Processing {len(prompts)} prompts with max {max_concurrent} concurrent...")

    async def process_func(prompt: str):
        return await generate_content(
            prompt=prompt,
            platform=platform,
            template=template,
            strategy=strategy,
            provider_name=provider_name,
        )

    processor = BatchProcessor(max_concurrent=max_concurrent)

    jobs = await processor.process_batch(prompts, process_func)

    results = []
    for job in jobs:
        results.append(job.to_dict())

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Batch results saved to: {output}")

    summary = processor.get_batch_summary()
    print("\nBatch Summary:")
    print(f"  Total: {summary['total']}")
    print(f"  Completed: {summary['completed']}")
    print(f"  Failed: {summary['failed']}")

    return results


def schedule_content(
    prompt: str,
    platform: str,
    scheduled_time: datetime,
    output: Optional[str] = None,
):
    """Schedule content for later posting."""
    print(f"Scheduling content for {platform} at {scheduled_time}")

    scheduler = Scheduler()

    schedule = scheduler.schedule_post(
        post_id=f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        scheduled_time=scheduled_time,
        content=prompt,
        platform=platform,
    )

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(schedule.__dict__, f, indent=2, default=str)
        print(f"Schedule saved to: {output}")

    return schedule


async def post_content(
    prompt: str,
    platform: str,
    template: Optional[str] = None,
    strategy: Optional[str] = None,
    output: Optional[str] = None,
):
    """Post content directly to a platform."""
    print(f"Posting content to {platform}...")

    result = await generate_content(
        prompt=prompt,
        platform=platform,
        template=template,
        strategy=strategy,
    )

    output_data = {
        "generated_content": result,
        "platform": platform,
        "timestamp": datetime.now().isoformat(),
    }

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2, default=str)
        print(f"Post result saved to: {output}")

    return output_data


def parse_time(time_str: str) -> datetime:
    """Parse time string into datetime."""
    try:
        return datetime.fromisoformat(time_str)
    except ValueError:
        pass

    if time_str.startswith("+"):
        value = int(time_str[1:-1])
        unit = time_str[-1]
        now = datetime.now()

        if unit == "m":
            return now + timedelta(minutes=value)
        elif unit == "h":
            return now + timedelta(hours=value)
        elif unit == "d":
            return now + timedelta(days=value)

    raise ValueError(f"Invalid time format: {time_str}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Content Generator CLI - Generate, schedule, and post content"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    generate_parser = subparsers.add_parser(
        "generate", help="Generate content from a prompt"
    )
    generate_parser.add_argument("--prompt", "-p", required=True, help="Content prompt")
    generate_parser.add_argument(
        "--platform",
        choices=["tiktok", "youtube", "instagram", "facebook"],
        help="Target platform",
    )
    generate_parser.add_argument("--template", "-t", help="Template to use")
    generate_parser.add_argument("--strategy", "-s", help="Content strategy")
    generate_parser.add_argument("--output", "-o", help="Output file path")
    generate_parser.add_argument(
        "--provider", default="ollama", help="LLM provider (default: ollama)"
    )

    batch_parser = subparsers.add_parser(
        "batch", help="Generate content for multiple prompts"
    )
    batch_parser.add_argument(
        "--prompts", "-p", nargs="+", required=True, help="List of prompts"
    )
    batch_parser.add_argument(
        "--platform",
        choices=["tiktok", "youtube", "instagram", "facebook"],
        help="Target platform",
    )
    batch_parser.add_argument("--template", "-t", help="Template to use")
    batch_parser.add_argument("--strategy", "-s", help="Content strategy")
    batch_parser.add_argument("--output", "-o", help="Output file path")
    batch_parser.add_argument(
        "--provider", default="ollama", help="LLM provider (default: ollama)"
    )
    batch_parser.add_argument(
        "--max-concurrent",
        "-c",
        type=int,
        default=3,
        help="Max concurrent jobs (default: 3)",
    )

    schedule_parser = subparsers.add_parser(
        "schedule", help="Schedule content for later posting"
    )
    schedule_parser.add_argument("--prompt", "-p", required=True, help="Content prompt")
    schedule_parser.add_argument(
        "--platform",
        required=True,
        choices=["tiktok", "youtube", "instagram", "facebook"],
        help="Target platform",
    )
    schedule_parser.add_argument(
        "--time",
        "-t",
        required=True,
        help="Scheduled time (ISO format or +1h, +30m, etc.)",
    )
    schedule_parser.add_argument(
        "--output", "-o", help="Output file path for schedule info"
    )

    post_parser = subparsers.add_parser(
        "post", help="Generate and post content to a platform"
    )
    post_parser.add_argument("--prompt", "-p", required=True, help="Content prompt")
    post_parser.add_argument(
        "--platform",
        required=True,
        choices=["tiktok", "youtube", "instagram", "facebook"],
        help="Target platform",
    )
    post_parser.add_argument("--template", "-t", help="Template to use")
    post_parser.add_argument("--strategy", "-s", help="Content strategy")
    post_parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "generate":
            result = asyncio.run(
                generate_content(
                    prompt=args.prompt,
                    platform=args.platform,
                    template=args.template,
                    strategy=args.strategy,
                    output=args.output,
                    provider_name=args.provider,
                )
            )
            print("\nGenerated Content:")
            print(json.dumps(result, indent=2, default=str))

        elif args.command == "batch":
            results = asyncio.run(
                batch_generate(
                    prompts=args.prompts,
                    platform=args.platform,
                    template=args.template,
                    strategy=args.strategy,
                    output=args.output,
                    provider_name=args.provider,
                    max_concurrent=args.max_concurrent,
                )
            )
            print(f"\nProcessed {len(results)} prompts")

        elif args.command == "schedule":
            scheduled_time = parse_time(args.time)
            schedule = schedule_content(
                prompt=args.prompt,
                platform=args.platform,
                scheduled_time=scheduled_time,
                output=args.output,
            )
            print(f"\nContent scheduled for: {schedule.scheduled_time}")

        elif args.command == "post":
            result = asyncio.run(
                post_content(
                    prompt=args.prompt,
                    platform=args.platform,
                    template=args.template,
                    strategy=args.strategy,
                    output=args.output,
                )
            )
            print("\nPost Result:")
            print(json.dumps(result, indent=2, default=str))

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
