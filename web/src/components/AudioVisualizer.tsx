import { useEffect, useRef, useState } from 'react';
import { usePlayer } from '../contexts/PlayerContext';

export default function AudioVisualizer() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const { isPlaying } = usePlayer();
  const [isEnabled, setIsEnabled] = useState(true);

  useEffect(() => {
    if (!canvasRef.current || !isPlaying || !isEnabled) {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      return;
    }

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    let barCount = 50;
    const bars: number[] = new Array(barCount).fill(0);

    const animate = () => {
      if (!ctx || !canvas) return;

      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update bars with pseudo-random animation
      bars.forEach((_, index) => {
        bars[index] = Math.random() * canvas.height * 0.7 + canvas.height * 0.15;
      });

      // Draw bars
      const barWidth = canvas.width / barCount;
      bars.forEach((height, index) => {
        const x = index * barWidth;
        const hue = (index / barCount) * 120 + 120; // Green to Cyan gradient
        
        // Draw bar
        ctx.fillStyle = `hsla(${hue}, 70%, 50%, 0.8)`;
        ctx.fillRect(x, canvas.height - height, barWidth - 2, height);
        
        // Add glow effect
        ctx.fillStyle = `hsla(${hue}, 70%, 60%, 0.3)`;
        ctx.fillRect(x, canvas.height - height - 5, barWidth - 2, 5);
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isPlaying, isEnabled]);

  if (!isPlaying) {
    return null;
  }

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        className="w-full h-24 rounded-lg bg-black/30"
        style={{ display: isEnabled ? 'block' : 'none' }}
      />
      <button
        onClick={() => setIsEnabled(!isEnabled)}
        className="absolute top-2 right-2 text-xs text-zinc-400 hover:text-white transition-colors"
      >
        {isEnabled ? '🎨 Hide' : '🎨 Show'} Visualizer
      </button>
    </div>
  );
}
