// Voice Commands Service using Web Speech API

export interface VoiceCommand {
  command: string;
  action: () => void;
  keywords: string[];
}

export class VoiceCommandService {
  private recognition: any;
  private isListening: boolean = false;
  private commands: Map<string, VoiceCommand> = new Map();
  private onCommandCallback?: (command: string, transcript: string) => void;
  private onErrorCallback?: (error: string) => void;
  private onStatusCallback?: (status: string) => void;
  private autoRestart: boolean = true;
  private lastRestartTime: number = 0;

  constructor() {
    // Check if Web Speech API is available
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      console.warn('Web Speech API not supported in this browser');
      return;
    }

    this.recognition = new SpeechRecognition();
    
    // Optimized settings for faster response
    this.recognition.continuous = true;
    this.recognition.interimResults = true; // Enable interim results for faster feedback
    this.recognition.lang = 'en-US';
    this.recognition.maxAlternatives = 1; // Reduce processing time
    
    this.setupEventHandlers();
    this.registerDefaultCommands();
  }

  private setupEventHandlers() {
    if (!this.recognition) return;

    this.recognition.onstart = () => {
      this.isListening = true;
      this.onStatusCallback?.('🎤 Listening...');
    };

    this.recognition.onend = () => {
      this.isListening = false;
      
      // Auto-restart if still supposed to be listening
      if (this.autoRestart && Date.now() - this.lastRestartTime > 1000) {
        this.lastRestartTime = Date.now();
        setTimeout(() => {
          if (this.autoRestart) {
            try {
              this.recognition.start();
            } catch (e) {
              console.log('Recognition already started');
            }
          }
        }, 100);
      } else {
        this.onStatusCallback?.('Stopped');
      }
    };

    this.recognition.onresult = (event: any) => {
      const last = event.results.length - 1;
      const result = event.results[last];
      const transcript = result[0].transcript.toLowerCase().trim();
      
      // Process both interim and final results for faster response
      if (result.isFinal) {
        console.log('Final voice input:', transcript);
        this.processCommand(transcript);
      } else {
        // Show interim results
        console.log('Interim:', transcript);
        this.onStatusCallback?.(`Hearing: "${transcript}"`);
      }
    };

    this.recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      
      // Handle specific errors
      if (event.error === 'no-speech') {
        this.onStatusCallback?.('No speech detected, still listening...');
      } else if (event.error === 'audio-capture') {
        this.onErrorCallback?.('No microphone found');
        this.autoRestart = false;
      } else if (event.error === 'not-allowed') {
        this.onErrorCallback?.('Microphone permission denied');
        this.autoRestart = false;
      } else {
        this.onErrorCallback?.(event.error);
      }
    };

    this.recognition.onsoundstart = () => {
      this.onStatusCallback?.('🔊 Sound detected...');
    };

    this.recognition.onspeechstart = () => {
      this.onStatusCallback?.('🗣️ Speech detected...');
    };
  }

  private registerDefaultCommands() {
    // Play commands
    this.registerCommand('play', ['play', 'start', 'resume'], () => {
      this.onCommandCallback?.('play', 'Playing music');
    });

    // Pause commands
    this.registerCommand('pause', ['pause', 'stop', 'halt'], () => {
      this.onCommandCallback?.('pause', 'Pausing music');
    });

    // Next song
    this.registerCommand('next', ['next', 'skip', 'next song', 'skip song'], () => {
      this.onCommandCallback?.('next', 'Skipping to next song');
    });

    // Previous song
    this.registerCommand('previous', ['previous', 'back', 'previous song', 'go back'], () => {
      this.onCommandCallback?.('previous', 'Going to previous song');
    });

    // Volume up
    this.registerCommand('volume_up', ['volume up', 'louder', 'increase volume', 'turn it up'], () => {
      this.onCommandCallback?.('volume_up', 'Increasing volume');
    });

    // Volume down
    this.registerCommand('volume_down', ['volume down', 'quieter', 'decrease volume', 'turn it down'], () => {
      this.onCommandCallback?.('volume_down', 'Decreasing volume');
    });

    // Shuffle
    this.registerCommand('shuffle', ['shuffle', 'shuffle on', 'play random'], () => {
      this.onCommandCallback?.('shuffle', 'Shuffle enabled');
    });

    // Mood-based playback
    this.registerCommand('play_chill', ['play something chill', 'play chill music', 'something relaxing', 'chill vibes'], () => {
      this.onCommandCallback?.('play_chill', 'Playing chill music');
    });

    this.registerCommand('play_energetic', ['play something energetic', 'play workout music', 'pump me up', 'energetic music'], () => {
      this.onCommandCallback?.('play_energetic', 'Playing energetic music');
    });

    this.registerCommand('play_happy', ['play something happy', 'play happy music', 'happy vibes', 'upbeat music'], () => {
      this.onCommandCallback?.('play_happy', 'Playing happy music');
    });

    this.registerCommand('play_sad', ['play something sad', 'play sad music', 'melancholic music', 'emotional music'], () => {
      this.onCommandCallback?.('play_sad', 'Playing sad music');
    });

    // Show recommendations
    this.registerCommand('recommendations', ['recommendations', 'show recommendations', 'suggest music', 'what should i listen to'], () => {
      this.onCommandCallback?.('recommendations', 'Showing recommendations');
    });

    // Show favorites
    this.registerCommand('favorites', ['favorites', 'show favorites', 'my favorites', 'liked songs'], () => {
      this.onCommandCallback?.('favorites', 'Showing favorites');
    });

    // Navigate home
    this.registerCommand('home', ['home', 'go home', 'dashboard', 'main page'], () => {
      this.onCommandCallback?.('home', 'Going to home');
    });
  }

  private processCommand(transcript: string) {
    // Always show what was heard
    this.onStatusCallback?.(`Heard: "${transcript}"`);
    
    // Check if it starts with wake word
    const wakeWords = ['hey groovex', 'groovex', 'ok groovex'];
    let commandText = transcript;
    
    // Remove wake word if present
    for (const wake of wakeWords) {
      if (transcript.startsWith(wake)) {
        commandText = transcript.substring(wake.length).trim();
        break;
      }
    }

    // Try to match command
    for (const [commandName, command] of this.commands.entries()) {
      for (const keyword of command.keywords) {
        if (commandText.includes(keyword)) {
          command.action();
          return;
        }
      }
    }

    // No command matched
    this.onErrorCallback?.(`Command not recognized: "${transcript}"`);
  }

  registerCommand(name: string, keywords: string[], action: () => void) {
    this.commands.set(name, { command: name, keywords, action });
  }

  start() {
    if (!this.recognition) {
      this.onErrorCallback?.('Speech recognition not available');
      return;
    }

    this.autoRestart = true;
    if (!this.isListening) {
      try {
        this.recognition.start();
        this.onStatusCallback?.('Starting voice recognition...');
      } catch (error) {
        console.error('Failed to start recognition:', error);
        // If already started, just continue
        if ((error as Error).message.includes('already started')) {
          this.isListening = true;
        }
      }
    }
  }

  stop() {
    this.autoRestart = false;
    if (this.recognition) {
      try {
        this.recognition.stop();
        this.isListening = false;
      } catch (error) {
        console.error('Failed to stop recognition:', error);
      }
    }
  }

  onCommand(callback: (command: string, message: string) => void) {
    this.onCommandCallback = callback;
  }

  onError(callback: (error: string) => void) {
    this.onErrorCallback = callback;
  }

  onStatus(callback: (status: string) => void) {
    this.onStatusCallback = callback;
  }

  getIsListening(): boolean {
    return this.isListening;
  }

  isSupported(): boolean {
    return !!this.recognition;
  }
}

export const voiceCommandService = new VoiceCommandService();
