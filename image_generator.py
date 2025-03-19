# improved_image_generator.py - Module to generate better pixel art images

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageEnhance, ImageFilter
import time
import re
import os

# Make sure output directory exists
os.makedirs("output", exist_ok=True)


def clean_text_for_prompt(text):
    """Clean lyrics or description text to create a good prompt"""
    if not text:
        return ""

    # Extract key phrases instead of full lines
    lines = text.strip().split('\n')
    short_text = ' '.join(lines[:5])  # Fewer lines to focus on core message

    # Remove special characters and excessive spaces
    cleaned_text = re.sub(r'[^\w\s]', ' ', short_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Extract keywords
    keywords = [word for word in cleaned_text.split()
                if len(word) > 3 and word.lower() not in
                ['this', 'that', 'then', 'than', 'with', 'from']][:10]

    return ' '.join(keywords)


def apply_pixel_art_effect(image, pixel_size=8):
    """Apply a better pixel art effect with color palette optimization"""
    width, height = image.size

    # Step 1: Enhance contrast and saturation
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(1.2)

    saturation = ImageEnhance.Color(image)
    image = saturation.enhance(1.3)

    # Step 2: Apply slight smoothing to reduce noise before pixelation
    image = image.filter(ImageFilter.SMOOTH_MORE)

    # Step 3: Calculate dimensions for proper pixelation
    small_width = width // pixel_size
    small_height = height // pixel_size

    # Step 4: Create the pixel art effect
    # Downscale with BICUBIC for smoother color averaging, then upscale with NEAREST for sharp pixels
    small_image = image.resize((small_width, small_height), Image.BICUBIC)
    pixel_art = small_image.resize((width, height), Image.NEAREST)

    # Step 5: Final sharpness adjustment
    sharpness = ImageEnhance.Sharpness(pixel_art)
    pixel_art = sharpness.enhance(0.8)  # Slight reduction in sharpness to avoid harshness

    return pixel_art


def generate_pixel_art(song_title, artist_name, lyrics=None, additional_description="", style="fantasy"):
    """Generate a pixel art album cover based on song information with style guidance"""
    try:
        # Setup image generation pipeline - using a better model if available
        print("Loading image generation model...")
        model_id = "runwayml/stable-diffusion-v1-5"  # Better base model

        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        else:
            print("Warning: Running on CPU, which will be slow")

        # Prepare the prompt with better guidance for pixel art
        lyrics_keywords = clean_text_for_prompt(lyrics) if lyrics else ""

        # Style presets for different pixel art aesthetics
        style_presets = {
            "fantasy": "fantasy rpg pixel art, 16-bit era, detailed characters, vibrant colors",
            "retro": "retro arcade pixel art, 8-bit style, bold colors, simple shapes",
            "cyberpunk": "cyberpunk pixel art, neon colors, dark background, high contrast",
            "vaporwave": "vaporwave aesthetic pixel art, pastel colors, glitch art elements",
            "minimal": "minimalist pixel art, limited color palette, simple geometric shapes"
        }

        style_prompt = style_presets.get(style.lower(), style_presets["fantasy"])

        # Build an improved prompt
        prompt_parts = [
            f"album cover for '{song_title}' by {artist_name}",
            style_prompt,
            "professional quality, cohesive composition",
        ]

        # Add lyrics keywords if available
        if lyrics_keywords:
            prompt_parts.append(f"themes: {lyrics_keywords}")

        # Add additional description if provided
        if additional_description:
            prompt_parts.append(additional_description)

        # Negative prompt to avoid common issues
        negative_prompt = "blurry, text, watermark, signature, distorted, low quality, disfigured"

        # Join non-empty parts
        prompt = ", ".join([part for part in prompt_parts if part])

        print(f"Generating image with prompt: {prompt}")
        print(f"Using negative prompt: {negative_prompt}")

        # Generate the image with better parameters
        image = pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,  # Fewer steps can sometimes work better
            guidance_scale=8.5,  # Slightly higher guidance
            height=512,
            width=512
        ).images[0]

        # Apply our improved pixel art effect
        pixel_art = apply_pixel_art_effect(image, pixel_size=6)  # Adjust pixel size as needed

        # Save the image
        timestamp = int(time.time())
        clean_title = re.sub(r'[\\/*?:"<>|]', "", song_title).strip()
        filename = f"output/{clean_title}_{timestamp}_cover.png"
        pixel_art.save(filename)

        print(f"Pixel art saved to {filename}")
        return filename

    except Exception as e:
        print(f"Error generating image: {e}")
        return None

