# Pixel Art Album Cover Generator

This simple application generates pixel art album covers for songs based on their lyrics and themes.

## Features

- Generate pixel art album covers using AI
- Fetch lyrics from Genius (optional)
- Simple command-line interface

## Setup

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Set up Genius API (optional):**
   - Create an account at [Genius Developer Portal](https://genius.com/api-clients)
   - Create a new API client
   - Set your API key as an environment variable:
     - On Windows: `set GENIUS_API_KEY=your_key_here`
     - On macOS/Linux: `export GENIUS_API_KEY=your_key_here`

## Usage

Run the application:
```
python main.py
```

Follow the prompts to:
1. Enter song title and artist
2. Add additional themes or imagery for the cover
3. Wait for the pixel art generation

The generated album cover will be saved in the `output` directory.

## Requirements

- Python 3.7+
- GPU recommended for faster image generation

## Example

```
---- PIXEL ART ALBUM COVER GENERATOR ----
Enter song title: Digital Love
Enter artist name: Daft Punk

Fetching lyrics for 'Digital Love' by Daft Punk...
Lyrics fetched successfully!

Based on these lyrics, please add any additional themes or imagery you want in the cover:
> retro arcade, neon lights, heart

Generating pixel art album cover...

Album cover generated successfully: output/Digital_Love_1710431234_cover.png
Thank you for using the Pixel Art Album Cover Generator!
```