// Counter Animation Component
// Animated number counter from start to end

import { useCurrentFrame, useVideoConfig, AbsoluteFill, Sequence } from 'remotion';

export const Counter = ({ start = 0, end, duration = 5, format = '#,###' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const totalFrames = duration * fps;
  
  const counterValue = interpolate(
    frame,
    [0, totalFrames],
    [start, end],
    { extrapolateRight: false }
  );
  
  // Format number
  const formattedValue = format.replace('#', counterValue);
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a2e' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
      }}>
        <h1 style={{
          fontSize: 150,
          fontWeight: 800,
          fontFamily: 'Arial, sans-serif',
          color: '#ffffff',
          textShadow: '0 4px 20px rgba(78, 205, 196, 0.5)',
        }}>
          {formattedValue}
        </h1>
      </div>
    </AbsoluteFill>
  );
};

import { interpolate } from 'remotion';

export default Counter;
