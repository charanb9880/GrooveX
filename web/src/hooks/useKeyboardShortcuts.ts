import { useEffect } from 'react';
import { usePlayer } from '../contexts/PlayerContext';
import { useNavigate } from 'react-router-dom';

export function useKeyboardShortcuts() {
  const player = usePlayer();
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Ignore if typing in an input field
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      // Space - Play/Pause
      if (e.code === 'Space') {
        e.preventDefault();
        player.togglePlayPause();
        showToast('⏯️ Play/Pause');
      }

      // Arrow Right - Next
      if (e.code === 'ArrowRight') {
        e.preventDefault();
        player.next();
        showToast('⏭️ Next Track');
      }

      // Arrow Left - Previous
      if (e.code === 'ArrowLeft') {
        e.preventDefault();
        player.previous();
        showToast('⏮️ Previous Track');
      }

      // Arrow Up - Volume Up
      if (e.code === 'ArrowUp') {
        e.preventDefault();
        player.increaseVolume();
        showToast(`🔊 Volume: ${Math.round(player.volume * 100)}%`);
      }

      // Arrow Down - Volume Down
      if (e.code === 'ArrowDown') {
        e.preventDefault();
        player.decreaseVolume();
        showToast(`🔉 Volume: ${Math.round(player.volume * 100)}%`);
      }

      // M - Mute/Unmute
      if (e.code === 'KeyM') {
        e.preventDefault();
        player.setVolume(player.volume > 0 ? 0 : 0.7);
        showToast(player.volume > 0 ? '🔇 Muted' : '🔊 Unmuted');
      }

      // P - Go to Player
      if (e.code === 'KeyP') {
        e.preventDefault();
        navigate('/player');
        showToast('🎵 Player');
      }

      // H - Go Home
      if (e.code === 'KeyH') {
        e.preventDefault();
        navigate('/');
        showToast('🏠 Home');
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [player, navigate]);
}

// Toast notification helper
function showToast(message: string) {
  const existingToast = document.querySelector('.keyboard-toast');
  if (existingToast) {
    existingToast.remove();
  }

  const toast = document.createElement('div');
  toast.className = 'keyboard-toast fixed top-20 right-6 bg-zinc-900 border border-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 animate-pulse';
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s';
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 1500);
}
