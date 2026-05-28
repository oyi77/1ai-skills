// Kinetic Typography Component
// Word-by-word animation with scale-in effect

import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export const KineticTypo = ({ text, fontSize = 80, fontWeight = 800, colors = ['#FF6B6B', '#4ECDC4'] }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  
  const words = text.split(' ');
  const wordsCount = words.length;
  
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100%',
      background: `linear-gradient(135deg, ${colors[0]}, ${colors[1]})`,
    }}>
      {words.map((word, index) => {
        const wordDelay = (durationInFrames / wordsCount) * index;
        const wordDuration = durationInFrames / wordsCount;
        
        const scale = interpolate(
          frame,
          [wordDelay, wordDelay + wordDuration],
          [0, 1],
          { extrapolateRight: false }
        );
        
        const opacity = interpolate(
          frame,
          [wordDelay, wordDelay + wordDuration * 0.2],
          [0, 1],
          { extrapolateRight: false }
        );
        
        return (
          <h1
            key={index}
            style={{
              fontSize,
              fontWeight,
              fontFamily: 'Arial, sans-serif',
              color: 'white',
              transform: `scale(${scale})`,
              opacity,
              margin: '0 10px',
              textShadow: `0 4px 20px rgba(0,0,0,0.3)`,
            }}
          >
            {word}
          </h1>
        );
      })}
    </div>
  );
};

export default KineticTypo;
