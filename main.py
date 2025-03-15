from lyrics_fetcher import fetch_lyrics_from_php_api
from image_generator import generate_pixel_art
import os


def create_output_directory():
    """Create output directory if it doesn't exist"""
    if not os.path.exists("output"):
        os.makedirs("output")


def main():
    """Main function to run the pixel art album cover generator"""
    create_output_directory()

    # Get song information from user
    print("---- PIXEL ART ALBUM COVER GENERATOR ----")
    song_title = input("Enter song title: ")
    artist_name = input("Enter artist name: ")

    # Fetch lyrics using Spotify API and PHP-based Lyrics API
    print(f"\nFetching lyrics for '{song_title}' by {artist_name}...")
    lyrics = fetch_lyrics_from_php_api(song_title, artist_name)

    if not lyrics:
        print("Couldn't fetch lyrics. Please enter a brief description of the song's mood/theme:")
        description = input("> ")
    else:
        print("Lyrics fetched successfully!")
        print("\nBased on these lyrics, please add any additional themes or imagery you want in the cover:")
        description = input("> ")

    # Generate the album cover
    print("\nGenerating pixel art album cover...")
    output_path = generate_pixel_art(song_title, artist_name, lyrics, description)

    print(f"\nAlbum cover generated successfully: {output_path}")
    print("Thank you for using the Pixel Art Album Cover Generator!")


if __name__ == "__main__":
    main()
