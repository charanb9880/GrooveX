import { useState, useEffect, useRef } from 'react';
import { lyricsService, Lyrics, LyricLine } from '../services/lyrics';

interface LyricsDisplayProps {
  songId: string;
  songTitle: string;
  artist: string;
  currentTime?: number;
  isPlaying?: boolean;
}

export default function LyricsDisplay({
  songId,
  songTitle,
  artist,
  currentTime = 0,
  isPlaying = false,
}: LyricsDisplayProps) {
  const [lyrics, setLyrics] = useState<Lyrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentLineIndex, setCurrentLineIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);
  const currentLineRef = useRef<HTMLDivElement>(null);

  // Fetch lyrics when song changes
  useEffect(() => {
    loadLyrics();
  }, [songId]);

  // Update current line based on playback time
  useEffect(() => {
    if (lyrics && isPlaying) {
      const lineInfo = lyricsService.getCurrentLine(currentTime);
      setCurrentLineIndex(lineInfo.index);
      
      // Auto-scroll to current line
      if (currentLineRef.current && containerRef.current) {
        const container = containerRef.current;
        const currentLine = currentLineRef.current;
        const containerHeight = container.clientHeight;
        const lineTop = currentLine.offsetTop;
        const lineHeight = currentLine.clientHeight;
        
        // Scroll to center the current line
        const scrollTarget = lineTop - containerHeight / 2 + lineHeight / 2;
        container.scrollTo({
          top: scrollTarget,
          behavior: 'smooth',
        });
      }
    }
  }, [currentTime, lyrics, isPlaying]);

  const loadLyrics = async () => {
    setIsLoading(true);
    try {
      const fetchedLyrics = await lyricsService.fetchLyrics(songId, songTitle, artist);
      setLyrics(fetchedLyrics);
      lyricsService.setCurrentLyrics(fetchedLyrics);
    } catch (error) {
      console.error('Failed to load lyrics:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="card p-6 flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <svg className="animate-spin h-8 w-8 text-green-500 mx-auto mb-3" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <p className="text-zinc-400">Loading lyrics...</p>
        </div>
      </div>
    );
  }

  if (!lyrics) {
    return (
      <div className="card p-6 flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <svg className="w-16 h-16 text-zinc-600 mx-auto mb-3" fill="currentColor" viewBox="0 0 20 20">
            <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z" />
          </svg>
          <p className="text-zinc-400 mb-2">No lyrics available</p>
          <p className="text-zinc-600 text-sm">Lyrics not found for this song</p>
        </div>
      </div>
    );
  }

  const linesWithState = lyricsService.getAllLines(currentTime);

  return (
    <div className="card overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-zinc-800 bg-gradient-to-r from-green-500/10 to-blue-500/10">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold text-white mb-1">{songTitle}</h3>
            <p className="text-zinc-400 text-sm">{artist}</p>
          </div>
          <div className="text-right">
            <span className="inline-block px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-medium border border-green-500/30">
              Synced Lyrics
            </span>
          </div>
        </div>
      </div>

      {/* Lyrics Container */}
      <div
        ref={containerRef}
        className="relative overflow-y-auto scroll-smooth"
        style={{ maxHeight: '500px' }}
      >
        <div className="p-8 space-y-6">
          {linesWithState.map((line, index) => {
            const isCurrent = index === currentLineIndex;
            const isPast = line.isPast;
            const isFuture = !isCurrent && !isPast;

            return (
              <div
                key={index}
                ref={isCurrent ? currentLineRef : null}
                className={`transition-all duration-300 transform ${
                  isCurrent
                    ? 'scale-110'
                    : 'scale-100'
                }`}
              >
                <p
                  className={`text-lg leading-relaxed transition-all duration-300 ${
                    isCurrent
                      ? 'text-white font-bold text-2xl bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent'
                      : isPast
                      ? 'text-zinc-500'
                      : 'text-zinc-400'
                  }`}
                  style={{
                    textAlign: line.text.startsWith('♪') ? 'center' : 'left',
                    fontStyle: line.text.startsWith('♪') ? 'italic' : 'normal',
                  }}
                >
                  {line.text}
                </p>
                
                {/* Progress bar for current line */}
                {isCurrent && isPlaying && line.endTime && (
                  <div className="mt-2 w-full bg-zinc-800 rounded-full h-1 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-green-500 to-blue-500 h-full rounded-full transition-all duration-100"
                      style={{
                        width: `${
                          ((currentTime - line.time) / (line.endTime - line.time)) * 100
                        }%`,
                      }}
                    />
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Gradient Overlays for visual effect */}
        <div className="absolute top-0 left-0 right-0 h-12 bg-gradient-to-b from-zinc-900 to-transparent pointer-events-none" />
        <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-zinc-900 to-transparent pointer-events-none" />
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-zinc-800 bg-zinc-900/50">
        <div className="flex items-center justify-between text-xs text-zinc-500">
          <span>
            Line {currentLineIndex + 1} of {lyrics.lines.length}
          </span>
          <span>Source: {lyrics.source}</span>
        </div>
      </div>
    </div>
  );
}
