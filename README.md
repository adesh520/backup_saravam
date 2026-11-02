# Comic Strip Generator

An interactive, AI-powered comic strip generator supporting Indian languages. Built with Flask and powered by [Sarvam AI](https://sarvam.ai).

## Features

- **Multi-panel Comic Generation**: Creates humorous, kid-friendly 4-panel comic strips in 10+ Indian languages using `sarvam-105b-conversations`.
- **Text-to-Speech (TTS)**: Click any speech bubble or "Play all" to hear the dialogue spoken with natural Indian accents using Sarvam's `bulbul:v3`.
- **Speech-to-Text (STT)**: Speak your comic idea using your microphone via `saaras:v3`.
- **Language Translation**: Translate generated comics dynamically across Indian languages and English using `sarvam-translate:v1`.

## Supported Languages

- Hindi (`hi-IN`)
- Marathi (`mr-IN`)
- Tamil (`ta-IN`)
- Telugu (`te-IN`)
- Bengali (`bn-IN`)
- Gujarati (`gu-IN`)
- Kannada (`kn-IN`)
- Malayalam (`ml-IN`)
- Punjabi (`pa-IN`)
- Odia (`od-IN`)
- English (`en-IN`)

## Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd "saravam(proj)"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your Sarvam API subscription key in `.env`:
     ```env
     SARVAM_API_KEY=your_sarvam_api_key_here
     ```

4. **Run the application**:
   ```bash
   python server.py
   ```

5. Open [http://localhost:5000](http://localhost:5000) in your web browser.
