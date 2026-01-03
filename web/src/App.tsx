import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { PlayerProvider } from './contexts/PlayerContext'
import { useKeyboardShortcuts } from './hooks/useKeyboardShortcuts'
import Navigation from './components/Navigation'
import VoiceControl from './components/VoiceControl'
import MiniPlayer from './components/MiniPlayer'
import Dashboard from './pages/Dashboard'
import Playlists from './pages/Playlists'
import Player from './pages/Player'
import Explorer from './pages/Explorer'
import Recommendations from './pages/Recommendations'
import Favorites from './pages/Favorites'
import Settings from './pages/Settings'
import AIFeatures from './pages/AIFeatures'

function AppContent() {
  useKeyboardShortcuts();
  
  return (
    <div className="flex min-h-screen bg-black">
      <Navigation />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/playlists" element={<Playlists />} />
          <Route path="/player" element={<Player />} />
          <Route path="/explorer" element={<Explorer />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/favorites" element={<Favorites />} />
          <Route path="/ai-features" element={<AIFeatures />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
      <MiniPlayer />
      <VoiceControl />
    </div>
  );
}

function App() {
  return (
    <PlayerProvider>
      <Router>
        <AppContent />
      </Router>
    </PlayerProvider>
  )
}

export default App