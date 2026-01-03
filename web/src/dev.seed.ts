// Demo data loader for PlayWise Music Engine
// This file can be used to load sample data into the system

interface SongData {
  title: string;
  artist: string;
  duration: number;
  genre?: string;
  subgenre?: string;
  mood?: string;
}

// Sample songs data
export const sampleSongs: SongData[] = [
  {
    title: "Bohemian Rhapsody",
    artist: "Queen",
    duration: 354,
    genre: "Rock",
    subgenre: "Classic Rock",
    mood: "Epic"
  },
  {
    title: "Imagine",
    artist: "John Lennon",
    duration: 183,
    genre: "Pop",
    subgenre: "Soft Rock",
    mood: "Peaceful"
  },
  {
    title: "Billie Jean",
    artist: "Michael Jackson",
    duration: 293,
    genre: "Pop",
    subgenre: "Dance Pop",
    mood: "Groovy"
  },
  {
    title: "Smells Like Teen Spirit",
    artist: "Nirvana",
    duration: 301,
    genre: "Rock",
    subgenre: "Grunge",
    mood: "Rebellious"
  },
  {
    title: "Like a Rolling Stone",
    artist: "Bob Dylan",
    duration: 373,
    genre: "Folk",
    subgenre: "Folk Rock",
    mood: "Reflective"
  },
  {
    title: "I Can't Get No Satisfaction",
    artist: "The Rolling Stones",
    duration: 227,
    genre: "Rock",
    subgenre: "Blues Rock",
    mood: "Energetic"
  },
  {
    title: "What's Going On",
    artist: "Marvin Gaye",
    duration: 227,
    genre: "R&B",
    subgenre: "Soul",
    mood: "Conscious"
  },
  {
    title: "Respect",
    artist: "Aretha Franklin",
    duration: 195,
    genre: "R&B",
    subgenre: "Soul",
    mood: "Empowering"
  },
  {
    title: "Good Vibrations",
    artist: "The Beach Boys",
    duration: 225,
    genre: "Pop",
    subgenre: "Psychedelic Pop",
    mood: "Happy"
  },
  {
    title: "Johnny B. Goode",
    artist: "Chuck Berry",
    duration: 155,
    genre: "Rock",
    subgenre: "Rock and Roll",
    mood: "Energetic"
  },
  {
    title: "Hey Jude",
    artist: "The Beatles",
    duration: 431,
    genre: "Rock",
    subgenre: "Classic Rock",
    mood: "Uplifting"
  },
  {
    title: "Purple Haze",
    artist: "Jimi Hendrix",
    duration: 173,
    genre: "Rock",
    subgenre: "Psychedelic Rock",
    mood: "Trippy"
  },
  {
    title: "London Calling",
    artist: "The Clash",
    duration: 200,
    genre: "Rock",
    subgenre: "Punk Rock",
    mood: "Rebellious"
  },
  {
    title: "Dancing Queen",
    artist: "ABBA",
    duration: 231,
    genre: "Pop",
    subgenre: "Disco",
    mood: "Joyful"
  },
  {
    title: "Hotel California",
    artist: "Eagles",
    duration: 391,
    genre: "Rock",
    subgenre: "Classic Rock",
    mood: "Mysterious"
  },
  {
    title: "Stairway to Heaven",
    artist: "Led Zeppelin",
    duration: 482,
    genre: "Rock",
    subgenre: "Hard Rock",
    mood: "Epic"
  },
  {
    title: "Sweet Child O' Mine",
    artist: "Guns N' Roses",
    duration: 356,
    genre: "Rock",
    subgenre: "Hard Rock",
    mood: "Passionate"
  },
  {
    title: "Born to Run",
    artist: "Bruce Springsteen",
    duration: 270,
    genre: "Rock",
    subgenre: "Heartland Rock",
    mood: "Energetic"
  },
  {
    title: "Superstition",
    artist: "Stevie Wonder",
    duration: 245,
    genre: "R&B",
    subgenre: "Funk",
    mood: "Groovy"
  },
  {
    title: "Blinding Lights",
    artist: "The Weeknd",
    duration: 200,
    genre: "Pop",
    subgenre: "Synth-pop",
    mood: "Energetic"
  }
];

// Function to load demo data
export async function loadDemoData(): Promise<void> {
  // In a real implementation, this would make API calls to load the data
  console.log("Loading demo data...");
  console.log(`Loaded ${sampleSongs.length} sample songs`);
  
  // Simulate API calls
  for (const song of sampleSongs) {
    console.log(`Adding song: ${song.title} by ${song.artist}`);
    // In a real implementation, you would call:
    // await addSongToPlaylist('main', song);
  }
  
  console.log("Demo data loaded successfully!");
}

// Button component for loading demo data
export function LoadDemoDataButton(): string {
  return `
    <button 
      onclick="loadDemoData()" 
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Load Demo Data
    </button>
  `;
}