"""Transcript and Script Generator for video content.

This module provides the ScriptGenerator class for generating video scripts,
transcripts, and scene-specific scripts using LLM providers.
"""

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .providers.base import AIProvider, GenerationResult
from .providers.groq import GroqProvider
from .providers.ollama import OllamaProvider
from .providers.xai import XAIProvider
from .providers.byteplus import BytePlusProvider
from .providers.nvidia import NVIDIAProvider


class ScriptStyle(Enum):
    """Video script styles."""

    NARRATION = "narration"
    DIALOGUE = "dialogue"
    PRODUCT_DEMO = "product_demo"
    TUTORIAL = "tutorial"


@dataclass
class ScriptLine:
    """A single line of script with timing."""

    text: str
    start_time: float  # seconds
    end_time: float  # seconds
    speaker: Optional[str] = None
    scene_number: Optional[int] = None
    notes: Optional[str] = None


@dataclass
class SceneScript:
    """Script for a single scene."""

    scene_number: int
    title: str
    duration_seconds: float
    start_time: float
    end_time: float
    narration: Optional[str] = None
    dialogue_lines: list[ScriptLine] = field(default_factory=list)
    visual_description: Optional[str] = None
    audio_cue: Optional[str] = None
    text_overlays: list[str] = field(default_factory=list)


@dataclass
class GeneratedScript:
    """Complete generated script for a video."""

    title: str
    style: ScriptStyle
    total_duration_seconds: float
    full_script: str
    narration_script: str
    scene_scripts: list[SceneScript] = field(default_factory=list)
    dialogue_script: Optional[str] = None
    word_count: int = 0
    estimated_speaking_time: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class TranscriptResult:
    """Result of transcript generation."""

    success: bool
    transcript: str = ""
    language: str = "en"
    segments: list[ScriptLine] = field(default_factory=list)
    duration_seconds: float = 0.0
    speaker_segments: dict = field(default_factory=dict)
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class ScriptGenerator:
    """Generate scripts, transcripts, and scene scripts for videos.

    This class provides methods to generate video scripts from prompts,
    create transcripts from video content (simulated), and generate
    individual scene scripts.

    Attributes:
        provider: LLM provider for text generation
        default_style: Default script style to use
    """

    # Style-specific system prompts
    STYLE_PROMPTS = {
        ScriptStyle.NARRATION: """You are a professional voiceover narrator.
Create a compelling narration script for a video.
Focus on flowing, descriptive language that sounds natural when spoken.
Include pacing cues and emphasis hints where appropriate.""",
        ScriptStyle.DIALOGUE: """You are a screenwriter creating dialogue for a video.
Create realistic, engaging dialogue between characters.
Make each character distinct through their speech patterns and vocabulary.
Include stage directions and speaker labels.""",
        ScriptStyle.PRODUCT_DEMO: """You are a product marketing specialist.
Create a demonstrative script that showcases product features.
Balance technical accuracy with consumer-friendly language.
Include call-to-action elements and benefit highlights.""",
        ScriptStyle.TUTORIAL: """You are an educational content creator.
Create a clear, step-by-step tutorial script.
Break down complex concepts into digestible segments.
Include tips, warnings, and encouragement for the viewer.""",
    }

    # Words per minute for different speaking styles (for timing estimation)
    SPEAKING_RATES = {
        ScriptStyle.NARRATION: 150,
        ScriptStyle.DIALOGUE: 160,
        ScriptStyle.PRODUCT_DEMO: 140,
        ScriptStyle.TUTORIAL: 130,
    }

    def __init__(
        self,
        provider: Optional[AIProvider] = None,
        default_style: ScriptStyle = ScriptStyle.NARRATION,
    ):
        """Initialize the ScriptGenerator.

        Args:
            provider: LLM provider for text generation. If not provided,
                     will attempt to use Groq or Ollama based on availability.
            default_style: Default style for script generation
        """
        self.provider = provider
        self.default_style = default_style

        # Auto-initialize provider if not provided
        if self.provider is None:
            self.provider = self._auto_init_provider()

    def _auto_init_provider(self) -> Optional[AIProvider]:
        """Auto-initialize an LLM provider based on available API keys.

        Priority order:
        1. XAI (grok-2 - best for script generation)
        2. BytePlus (for video scripts)
        3. NVIDIA (for image-to-script)
        4. Groq (fast fallback)
        5. Ollama (local fallback)

        Returns:
            Initialized provider or None if no provider available
        """
        # Try XAI first (recommended for script generation)
        xai_key = os.environ.get("XAI_API_KEY")
        if xai_key:
            try:
                return XAIProvider(api_key=xai_key)
            except Exception:
                pass

        # Try BytePlus
        byteplus_key = os.environ.get("BYTEPLUS_API_KEY")
        if byteplus_key:
            try:
                return BytePlusProvider(api_key=byteplus_key)
            except Exception:
                pass

        # Try NVIDIA
        nvidia_key = os.environ.get("NVIDIA_API_KEY")
        if nvidia_key:
            try:
                return NVIDIAProvider(api_key=nvidia_key)
            except Exception:
                pass

        # Try Groq (fast text generation)
        groq_key = os.environ.get("GROQ_API_KEY")
        if groq_key:
            try:
                return GroqProvider(api_key=groq_key)
            except Exception:
                pass

        # Try Ollama (local fallback)
        try:
            ollama = OllamaProvider()
            # Check if Ollama is available
            if os.environ.get("OLLAMA_AVAILABLE", "").lower() == "true":
                return ollama
        except Exception:
            pass

        return None

    def set_provider(self, provider: AIProvider) -> None:
        """Manually set the LLM provider.

        Args:
            provider: The AIProvider instance to use
        """
        self.provider = provider

    @classmethod
    def with_provider(cls, provider: AIProvider, **kwargs) -> "ScriptGenerator":
        """Create a ScriptGenerator with a specific provider.

        Args:
            provider: The AIProvider to use
            **kwargs: Additional arguments for ScriptGenerator

        Returns:
            ScriptGenerator instance with the specified provider
        """
        generator = cls(**kwargs)
        generator.set_provider(provider)
        return generator

    async def generate_script(
        self,
        prompt: str,
        style: Optional[ScriptStyle] = None,
        duration_seconds: Optional[float] = None,
        target_word_count: Optional[int] = None,
        include_dialogue: bool = False,
        **kwargs,
    ) -> GeneratedScript:
        """Generate a complete video script from a prompt.

        Args:
            prompt: Description/topic for the video script
            style: Script style (narration, dialogue, product_demo, tutorial)
            duration_seconds: Target duration for the video
            target_word_count: Target word count for the script
            include_dialogue: Whether to include dialogue elements
            **kwargs: Additional provider-specific parameters

        Returns:
            GeneratedScript with full script content and timing
        """
        style = style or self.default_style

        # Build the prompt for script generation
        system_prompt = self.STYLE_PROMPTS.get(
            style, self.STYLE_PROMPTS[ScriptStyle.NARRATION]
        )

        # Create user prompt with requirements
        user_prompt = self._build_script_prompt(
            prompt=prompt,
            style=style,
            duration_seconds=duration_seconds,
            target_word_count=target_word_count,
            include_dialogue=include_dialogue,
        )

        # Generate using provider
        result = await self._generate_with_provider(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            **kwargs,
        )

        if not result.success:
            raise ValueError(
                f"Script generation failed: {result.metadata.get('error')}"
            )

        # Parse the generated script
        script_content = result.data
        return self._parse_generated_script(
            content=script_content,
            prompt=prompt,
            style=style,
            duration_seconds=duration_seconds,
            target_word_count=target_word_count,
        )

    def _build_script_prompt(
        self,
        prompt: str,
        style: ScriptStyle,
        duration_seconds: Optional[float],
        target_word_count: Optional[int],
        include_dialogue: bool,
    ) -> str:
        """Build the user prompt for script generation."""
        prompt_parts = [
            f"Create a video script for: {prompt}",
        ]

        if duration_seconds:
            prompt_parts.append(
                f"Target duration: approximately {duration_seconds} seconds"
            )

        if target_word_count:
            prompt_parts.append(f"Target word count: {target_word_count} words")
        elif duration_seconds:
            # Estimate word count from duration
            rate = self.SPEAKING_RATES.get(style, 150)
            words = int((duration_seconds / 60) * rate)
            prompt_parts.append(f"Target word count: approximately {words} words")

        if include_dialogue:
            prompt_parts.append("Include dialogue elements with speaker labels")

        prompt_parts.append("\nProvide the script in a clear, structured format.")

        return "\n".join(prompt_parts)

    async def _generate_with_provider(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs,
    ) -> GenerationResult:
        """Generate content using the provider."""
        if self.provider is None:
            return GenerationResult(
                success=False,
                data=None,
                cost=0.0,
                provider="none",
                model="",
                metadata={"error": "No LLM provider available"},
            )

        # Combine system and user prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        return await self.provider.generate(
            prompt=full_prompt,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048),
        )

    def _parse_generated_script(
        self,
        content: str,
        prompt: str,
        style: ScriptStyle,
        duration_seconds: Optional[float],
        target_word_count: Optional[int],
    ) -> GeneratedScript:
        """Parse generated content into a structured GeneratedScript."""
        # Extract title from first line if it's a heading
        lines = content.strip().split("\n")
        title = prompt
        if lines and lines[0].startswith("#"):
            title = lines[0].lstrip("#").strip()
            content = "\n".join(lines[1:])

        # Estimate duration if not provided
        word_count = len(content.split())
        if duration_seconds is None:
            rate = self.SPEAKING_RATES.get(style, 150)
            duration_seconds = (word_count / rate) * 60

        # Estimate speaking time
        rate = self.SPEAKING_RATES.get(style, 150)
        estimated_speaking_time = (word_count / rate) * 60

        return GeneratedScript(
            title=title,
            style=style,
            total_duration_seconds=duration_seconds or 0.0,
            full_script=content.strip(),
            narration_script=content.strip(),
            word_count=word_count,
            estimated_speaking_time=estimated_speaking_time,
            metadata={
                "prompt": prompt,
                "target_word_count": target_word_count,
            },
        )

    async def generate_scene_scripts(
        self,
        prompt: str,
        num_scenes: int = 5,
        style: Optional[ScriptStyle] = None,
        total_duration_seconds: float = 60.0,
        **kwargs,
    ) -> list[SceneScript]:
        """Generate individual scripts for each scene.

        Args:
            prompt: Description/topic for the video
            num_scenes: Number of scenes to generate
            style: Script style
            total_duration_seconds: Total video duration
            **kwargs: Additional provider-specific parameters

        Returns:
            List of SceneScript objects with timing and content
        """
        style = style or self.default_style
        scene_duration = total_duration_seconds / num_scenes

        # Build prompt for scene generation
        system_prompt = self.STYLE_PROMPTS.get(
            style, self.STYLE_PROMPTS[ScriptStyle.NARRATION]
        )
        user_prompt = f"""Create {num_scenes} distinct scene scripts for a video about: {prompt}

Total duration: {total_duration_seconds} seconds ({scene_duration:.1f} seconds per scene)

For each scene, provide:
1. Scene title
2. Visual description (what to show)
3. Narration/dialogue content
4. Audio cues (music, sound effects)
5. Any text overlays

Format as a structured list with scene numbers."""

        result = await self._generate_with_provider(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            **kwargs,
        )

        if not result.success:
            raise ValueError(
                f"Scene script generation failed: {result.metadata.get('error')}"
            )

        # Parse into SceneScript objects
        return self._parse_scene_scripts(
            content=result.data,
            num_scenes=num_scenes,
            scene_duration=scene_duration,
            style=style,
        )

    def _parse_scene_scripts(
        self,
        content: str,
        num_scenes: int,
        scene_duration: float,
        style: ScriptStyle,
    ) -> list[SceneScript]:
        """Parse generated content into SceneScript objects."""
        scene_scripts = []
        current_time = 0.0

        # Simple parsing - split by scene markers
        lines = content.strip().split("\n")
        current_scene = None
        scene_data = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect scene headers
            if line.lower().startswith("scene "):
                if current_scene is not None and scene_data:
                    scene_scripts.append(
                        self._create_scene_script(
                            scene_number=current_scene,
                            start_time=current_time,
                            duration=scene_duration,
                            data=scene_data,
                            style=style,
                        )
                    )
                    current_time += scene_duration

                # Extract scene number
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        current_scene = int(parts[1].strip(".:"))
                    except ValueError:
                        current_scene = len(scene_scripts) + 1

                scene_data = {}
                continue

            # Parse content lines
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()

                if "title" in key:
                    scene_data["title"] = value
                elif "visual" in key or "description" in key:
                    scene_data["visual_description"] = value
                elif "narration" in key or "script" in key or "content" in key:
                    scene_data["narration"] = value
                elif "audio" in key or "sound" in key:
                    scene_data["audio_cue"] = value
                elif "text" in key or "overlay" in key:
                    if "text_overlays" not in scene_data:
                        scene_data["text_overlays"] = []
                    scene_data["text_overlays"].append(value)

        # Add the last scene
        if current_scene is not None and scene_data:
            scene_scripts.append(
                self._create_scene_script(
                    scene_number=current_scene,
                    start_time=current_time,
                    duration=scene_duration,
                    data=scene_data,
                    style=style,
                )
            )

        # Ensure we have the requested number of scenes
        while len(scene_scripts) < num_scenes:
            scene_num = len(scene_scripts) + 1
            start_time = (scene_num - 1) * scene_duration
            scene_scripts.append(
                SceneScript(
                    scene_number=scene_num,
                    title=f"Scene {scene_num}",
                    duration_seconds=scene_duration,
                    start_time=start_time,
                    end_time=start_time + scene_duration,
                    narration=f"Content for scene {scene_num}",
                )
            )

        return scene_scripts[:num_scenes]

    def _create_scene_script(
        self,
        scene_number: int,
        start_time: float,
        duration: float,
        data: dict,
        style: ScriptStyle,
    ) -> SceneScript:
        """Create a SceneScript from parsed data."""
        return SceneScript(
            scene_number=scene_number,
            title=data.get("title", f"Scene {scene_number}"),
            duration_seconds=duration,
            start_time=start_time,
            end_time=start_time + duration,
            narration=data.get("narration"),
            visual_description=data.get("visual_description"),
            audio_cue=data.get("audio_cue"),
            text_overlays=data.get("text_overlays", []),
        )

    async def generate_transcript(
        self,
        video_path: str,
        language: str = "en",
        include_timestamps: bool = True,
        include_speakers: bool = False,
        **kwargs,
    ) -> TranscriptResult:
        """Generate transcript from video content.

        Note: This is a simulated implementation. In production, you would
        integrate with a speech-to-text service like Whisper, AssemblyAI,
        or Deepgram for actual transcription.

        Args:
            video_path: Path to the video file
            language: Expected language of speech
            include_timestamps: Whether to include timestamps in transcript
            include_speakers: Whether to attempt speaker identification
            **kwargs: Additional parameters

        Returns:
            TranscriptResult with transcript and timing information
        """
        # This is a placeholder/simulated implementation
        # In production, integrate with actual speech-to-text service

        # Simulate processing
        return TranscriptResult(
            success=True,
            transcript="[Transcript generation would require a speech-to-text service. "
            "Consider integrating AssemblyAI, Deepgram, or Whisper API.]",
            language=language,
            segments=[],
            duration_seconds=0.0,
            speaker_segments={},
            metadata={
                "video_path": video_path,
                "note": "Simulated - requires speech-to-text integration",
            },
        )

    def generate_transcript_from_script(
        self,
        script: GeneratedScript,
        include_timestamps: bool = True,
    ) -> TranscriptResult:
        """Generate a timed transcript from a generated script.

        This converts a GeneratedScript into a transcript format with
        timestamps based on the estimated speaking rate.

        Args:
            script: The GeneratedScript to convert
            include_timestamps: Whether to include timestamps

        Returns:
            TranscriptResult with segmented transcript
        """
        segments = []
        current_time = 0.0

        # Split script into segments (roughly 10-15 words per segment)
        words = script.narration_script.split()
        segment_size = 12  # words per segment
        rate = self.SPEAKING_RATES.get(script.style, 150)
        seconds_per_word = 60.0 / rate

        for i in range(0, len(words), segment_size):
            segment_words = words[i : i + segment_size]
            segment_text = " ".join(segment_words)
            segment_duration = len(segment_words) * seconds_per_word

            segments.append(
                ScriptLine(
                    text=segment_text,
                    start_time=current_time,
                    end_time=current_time + segment_duration,
                )
            )

            current_time += segment_duration

        # Build full transcript
        if include_timestamps:
            transcript_lines = []
            for seg in segments:
                start_min = int(seg.start_time // 60)
                start_sec = int(seg.start_time % 60)
                transcript_lines.append(f"[{start_min:02d}:{start_sec:02d}] {seg.text}")
            transcript = "\n".join(transcript_lines)
        else:
            transcript = script.narration_script

        return TranscriptResult(
            success=True,
            transcript=transcript,
            language="en",
            segments=segments,
            duration_seconds=current_time,
            metadata={
                "word_count": script.word_count,
                "style": script.style.value,
            },
        )

    def export_script(
        self,
        script: GeneratedScript,
        format: str = "txt",
    ) -> str:
        """Export script in various formats.

        Args:
            script: The script to export
            format: Export format (txt, srt, vtt, markdown)

        Returns:
            Formatted script content
        """
        if format == "txt":
            return self._export_txt(script)
        elif format == "srt":
            return self._export_srt(script)
        elif format == "vtt":
            return self._export_vtt(script)
        elif format == "markdown":
            return self._export_markdown(script)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_txt(self, script: GeneratedScript) -> str:
        """Export as plain text."""
        lines = [
            f"Title: {script.title}",
            f"Style: {script.style.value}",
            f"Duration: {script.total_duration_seconds:.1f}s",
            f"Word Count: {script.word_count}",
            "",
            "=" * 50,
            "SCRIPT",
            "=" * 50,
            "",
            script.full_script,
        ]

        if script.scene_scripts:
            lines.extend(
                [
                    "",
                    "=" * 50,
                    "SCENE BREAKDOWN",
                    "=" * 50,
                ]
            )
            for scene in script.scene_scripts:
                lines.extend(
                    [
                        f"\nScene {scene.scene_number}: {scene.title}",
                        f"Duration: {scene.duration_seconds:.1f}s",
                    ]
                )
                if scene.narration:
                    lines.append(f"Narration: {scene.narration}")

        return "\n".join(lines)

    def _export_srt(self, script: GeneratedScript) -> str:
        """Export as SRT subtitle format."""
        transcript_result = self.generate_transcript_from_script(
            script, include_timestamps=True
        )
        lines = []

        for i, seg in enumerate(transcript_result.segments, 1):
            lines.append(str(i))

            # Format timestamps
            start = self._format_srt_timestamp(seg.start_time)
            end = self._format_srt_timestamp(seg.end_time)
            lines.append(f"{start} --> {end}")

            lines.append(seg.text)
            lines.append("")

        return "\n".join(lines)

    def _format_srt_timestamp(self, seconds: float) -> str:
        """Format seconds to SRT timestamp (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def _export_vtt(self, script: GeneratedScript) -> str:
        """Export as WebVTT subtitle format."""
        transcript_result = self.generate_transcript_from_script(
            script, include_timestamps=True
        )
        lines = ["WEBVTT", ""]

        for seg in transcript_result.segments:
            start = self._format_vtt_timestamp(seg.start_time)
            end = self._format_vtt_timestamp(seg.end_time)
            lines.append(f"{start} --> {end}")
            lines.append(seg.text)
            lines.append("")

        return "\n".join(lines)

    def _format_vtt_timestamp(self, seconds: float) -> str:
        """Format seconds to VTT timestamp (HH:MM:SS.mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    def _export_markdown(self, script: GeneratedScript) -> str:
        """Export as Markdown with timing."""
        lines = [
            f"# {script.title}",
            "",
            f"**Style:** {script.style.value}",
            f"**Duration:** {script.total_duration_seconds:.1f} seconds",
            f"**Word Count:** {script.word_count}",
            "",
            "---",
            "",
            "## Full Script",
            "",
            script.full_script,
        ]

        if script.scene_scripts:
            lines.extend(
                [
                    "",
                    "---",
                    "",
                    "## Scene Breakdown",
                ]
            )
            for scene in script.scene_scripts:
                lines.extend(
                    [
                        f"### Scene {scene.scene_number}: {scene.title}",
                        "",
                        f"**Duration:** {scene.duration_seconds:.1f}s",
                        f"**Timing:** {scene.start_time:.1f}s - {scene.end_time:.1f}s",
                    ]
                )
                if scene.narration:
                    lines.append(f"\n**Narration:**\n{scene.narration}")
                if scene.visual_description:
                    lines.append(f"\n**Visual:**\n{scene.visual_description}")
                if scene.audio_cue:
                    lines.append(f"\n**Audio:**\n{scene.audio_cue}")
                lines.append("")

        return "\n".join(lines)


# Convenience functions


async def quick_script(
    prompt: str,
    duration_seconds: float = 60.0,
    style: ScriptStyle = ScriptStyle.NARRATION,
) -> GeneratedScript:
    """Quick script generation with default settings.

    Args:
        prompt: Video topic/description
        duration_seconds: Target video duration
        style: Script style

    Returns:
        Generated script
    """
    generator = ScriptGenerator()
    return await generator.generate_script(
        prompt=prompt,
        style=style,
        duration_seconds=duration_seconds,
    )


async def quick_transcript(video_path: str) -> TranscriptResult:
    """Quick transcript generation (simulated).

    Args:
        video_path: Path to video file

    Returns:
        Transcript result
    """
    generator = ScriptGenerator()
    return await generator.generate_transcript(video_path=video_path)
