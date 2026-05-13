# Remotion Audio Rule

## Basic Audio

```tsx
import { Audio, staticFile } from 'remotion';

// Background music (loops by default if shorter than composition)
<Audio src={staticFile('background.mp3')} volume={0.3} />

// Narration audio (one-shot)
<Audio src={staticFile('narration.mp3')} />

// URL audio
<Audio src="https://example.com/audio.mp3" />
```

## Audio in Sequence (sync narration to scene)

```tsx
<Sequence from={0} durationInFrames={150}>
  <Audio src={staticFile('scene1-narration.mp3')} />
  <Scene1 />
</Sequence>
```

## Trim and Volume

```tsx
<Audio
  src={staticFile('audio.mp3')}
  startFrom={30}          // skip first 30 frames of audio
  endAt={90}              // stop at frame 90 of audio
  volume={0.5}            // 0 to 1
  playbackRate={1.0}      // speed (0.5 to 2.0)
/>
```

## Dynamic Volume (fade in/out)

```tsx
const frame = useCurrentFrame();
const volume = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
<Audio src={staticFile('music.mp3')} volume={volume} />
```

## Getting Audio Duration (for calculateMetadata)

```tsx
import { getAudioDurationInSeconds } from '@remotion/media-utils';

// Use in calculateMetadata to dynamically set composition duration
export const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const duration = await getAudioDurationInSeconds(staticFile(props.audioFile));
  return {
    durationInFrames: Math.ceil(duration * 30), // assuming 30fps
  };
};
```

## TTS Pipeline (Edge TTS — Free)

Install: `pip install edge-tts`

```python
# generate_tts.py
import asyncio
import edge_tts

async def generate_tts(text: str, output_path: str, voice: str = "en-US-JennyNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

asyncio.run(generate_tts("Hello, this is a narration.", "public/narration.mp3"))
```

Common voices:
- `en-US-JennyNeural` — female English
- `en-US-GuyNeural` — male English
- `id-ID-ArdiNeural` — male Indonesian (Bahasa)
- `id-ID-GadisNeural` — female Indonesian (Bahasa)
- `zh-CN-XiaoxiaoNeural` — Chinese female

## Audio-Video Sync Pattern (timing.json)

For narrated multi-scene videos, store audio timing in a JSON file:

```json
// public/timing.json
{
  "scenes": [
    { "id": "intro", "audioFile": "intro.mp3", "durationSeconds": 4.5 },
    { "id": "main", "audioFile": "main.mp3", "durationSeconds": 12.0 },
    { "id": "outro", "audioFile": "outro.mp3", "durationSeconds": 3.0 }
  ]
}
```

```tsx
// Use in calculateMetadata to set composition duration from audio
import timingData from '../public/timing.json';

const totalFrames = timingData.scenes.reduce(
  (acc, scene) => acc + Math.ceil(scene.durationSeconds * fps),
  0
);
```

## Azure TTS (High Quality, Bilingual)

```python
import azure.cognitiveservices.speech as speechsdk

def generate_azure_tts(text, output_file, voice="en-US-JennyNeural"):
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ["AZURE_SPEECH_KEY"],
        region=os.environ["AZURE_SPEECH_REGION"]
    )
    speech_config.speech_synthesis_voice_name = voice
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)
    synthesizer.speak_text_async(text).get()
```

## Audio Visualization (Waveform/Spectrum)

```tsx
import { useAudioData, visualizeAudio } from '@remotion/media-utils';

const audioData = useAudioData(staticFile('audio.mp3'));
if (!audioData) return null;

const visualization = visualizeAudio({
  fps,
  frame,
  audioData,
  numberOfSamples: 32,
});

return (
  <div style={{ display: 'flex', gap: 4 }}>
    {visualization.map((bar, i) => (
      <div
        key={i}
        style={{
          width: 10,
          height: bar * 200,
          backgroundColor: '#4f46e5',
        }}
      />
    ))}
  </div>
);
```
