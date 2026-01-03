// Deepgram Voice Recognition Service (Alternative to Web Speech API)
// Much faster and more accurate, but requires API key

export interface DeepgramConfig {
  apiKey?: string;
  useBackend?: boolean; // If true, route through our backend
}

export class DeepgramVoiceService {
  private mediaRecorder: MediaRecorder | null = null;
  private audioContext: AudioContext | null = null;
  private isListening: boolean = false;
  private websocket: WebSocket | null = null;
  private config: DeepgramConfig;
  private onTranscriptCallback?: (transcript: string, isFinal: boolean) => void;
  private onErrorCallback?: (error: string) => void;
  private onStatusCallback?: (status: string) => void;

  constructor(config: DeepgramConfig = {}) {
    this.config = config;
  }

  async start() {
    try {
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      this.onStatusCallback?.('🎤 Microphone ready...');
      
      if (this.config.useBackend) {
        // Use backend WebSocket proxy
        await this.startBackendStream(stream);
      } else if (this.config.apiKey) {
        // Direct Deepgram connection
        await this.startDeepgramStream(stream);
      } else {
        throw new Error('No API key or backend configured');
      }
      
      this.isListening = true;
    } catch (error) {
      console.error('Failed to start Deepgram:', error);
      this.onErrorCallback?.(`Failed to start: ${(error as Error).message}`);
    }
  }

  private async startDeepgramStream(stream: MediaStream) {
    // Connect to Deepgram WebSocket
    const wsUrl = `wss://api.deepgram.com/v1/listen?punctuate=true&interim_results=true&language=en-US`;
    
    this.websocket = new WebSocket(wsUrl, ['token', this.config.apiKey!]);
    
    this.websocket.onopen = () => {
      this.onStatusCallback?.('✅ Connected to Deepgram');
      this.startRecording(stream);
    };
    
    this.websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.channel?.alternatives?.[0]?.transcript) {
        const transcript = data.channel.alternatives[0].transcript;
        const isFinal = data.is_final || false;
        
        this.onTranscriptCallback?.(transcript, isFinal);
      }
    };
    
    this.websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.onErrorCallback?.('Connection error');
    };
    
    this.websocket.onclose = () => {
      this.onStatusCallback?.('Disconnected');
      this.isListening = false;
    };
  }

  private async startBackendStream(stream: MediaStream) {
    // Connect to our backend WebSocket proxy
    const wsUrl = `ws://localhost:8000/ws/voice`;
    
    this.websocket = new WebSocket(wsUrl);
    
    this.websocket.onopen = () => {
      this.onStatusCallback?.('✅ Connected to voice server');
      this.startRecording(stream);
    };
    
    this.websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.transcript) {
          this.onTranscriptCallback?.(data.transcript, data.is_final || false);
        }
      } catch (e) {
        console.error('Failed to parse message:', e);
      }
    };
    
    this.websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.onErrorCallback?.('Connection error');
    };
    
    this.websocket.onclose = () => {
      this.onStatusCallback?.('Disconnected');
      this.isListening = false;
    };
  }

  private startRecording(stream: MediaStream) {
    // Create MediaRecorder to capture audio
    this.mediaRecorder = new MediaRecorder(stream, {
      mimeType: 'audio/webm;codecs=opus',
      audioBitsPerSecond: 16000
    });
    
    this.mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0 && this.websocket?.readyState === WebSocket.OPEN) {
        // Send audio chunk to WebSocket
        this.websocket.send(event.data);
      }
    };
    
    // Collect audio in small chunks for real-time streaming
    this.mediaRecorder.start(100); // 100ms chunks for low latency
    
    this.onStatusCallback?.('🎙️ Recording...');
  }

  stop() {
    this.isListening = false;
    
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
      this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
    
    if (this.websocket) {
      this.websocket.close();
    }
    
    this.onStatusCallback?.('Stopped');
  }

  onTranscript(callback: (transcript: string, isFinal: boolean) => void) {
    this.onTranscriptCallback = callback;
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
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
  }
}
