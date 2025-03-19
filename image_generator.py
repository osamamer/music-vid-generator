# image_generator.py - Module to generate pixel art images

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import time
import re


def clean_text_for_prompt(text):
    """Clean lyrics or description text to create a good prompt"""
    if not text:
        return ""

    # Extract the first few lines to capture the song's essence
    lines = text.strip().split('\n')
    short_text = ' '.join(lines[:8])  # First 8 lines should be enough

    # Remove special characters and excessive spaces
    cleaned_text = re.sub(r'[^\w\s]', ' ', short_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Truncate if too long
    return cleaned_text[:200] if len(cleaned_text) > 200 else cleaned_text


def generate_pixel_art(song_title, artist_name, lyrics=None, additional_description=""):
    """Generate a pixel art album cover based on song information"""
    try:
        # Setup image generation pipeline
        print("Loading image generation model...")
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        else:
            print("Warning: Running on CPU, which will be slow")

        # Prepare the prompt
        lyrics = clean_text_for_prompt(lyrics) if lyrics else ""

        # Build a comprehensive prompt
        prompt_parts = [
            f"pixel art album cover for song '{song_title}' by {artist_name}",
            "16-bit style, vibrant colors, detailed",
            f"lyrics: {lyrics}",
            additional_description
        ]

        # Join non-empty parts
        prompt = ", ".join([part for part in prompt_parts if part])

        print(f"Generating image with prompt: {prompt}")

        # Generate the image
        image = pipe(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]

        # Apply pixel art effect
        width, height = image.size
        pixel_art_size = (64, 64)  # Downsample to create pixelation effect

        # Resize down and then back up to create pixel art effect
        pixel_art = image.resize(pixel_art_size, Image.NEAREST)
        pixel_art = pixel_art.resize((width, height), Image.NEAREST)

        # Save the image
        timestamp = int(time.time())
        clean_title = re.sub(r'[\\/*?:"<>|]', "", song_title).strip()
        filename = f"output/{clean_title}_{timestamp}_cover.png"
        pixel_art.save(filename)

        return filename

    except Exception as e:
        print(f"Error generating image: {e}")
        return None