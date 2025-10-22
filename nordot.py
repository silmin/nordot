#!/usr/bin/env python3
"""
Convert images to pixel art using Nord color scheme (blue and black palette)
"""
import sys
from PIL import Image
import numpy as np

# Nord color scheme (blue and black)
NORD_COLORS = [
    (46, 52, 64),      # Nord0 (Polar Night - darkest)
    (59, 66, 82),      # Nord1 (Polar Night)
    (67, 76, 94),      # Nord2 (Polar Night)
    (76, 86, 106),     # Nord3 (Polar Night - brightest)
    (94, 129, 172),    # Nord9 (Frost - blue)
    (129, 161, 193),   # Nord10 (Frost - light blue)
]

def closest_nord_color(rgb):
    """Find the closest Nord color"""
    min_dist = float('inf')
    closest = NORD_COLORS[0]

    for nord_color in NORD_COLORS:
        dist = sum((a - b) ** 2 for a, b in zip(rgb, nord_color))
        if dist < min_dist:
            min_dist = dist
            closest = nord_color

    return closest

def convert_to_pixel_art(image_path, output_path, pixel_size=8, gap=0):
    """Convert image to Nord color pixel art"""
    # Open image
    img = Image.open(image_path).convert('RGB')
    width, height = img.size

    # Calculate number of pixel blocks
    blocks_x = width // pixel_size
    blocks_y = height // pixel_size

    # Calculate output image size
    output_width = blocks_x * (pixel_size + gap) - gap if gap > 0 else width
    output_height = blocks_y * (pixel_size + gap) - gap if gap > 0 else height

    # Initialize with background color (darkest Nord color)
    final_img = Image.new('RGB', (output_width, output_height), NORD_COLORS[0])

    # Process each pixel block
    for block_y in range(blocks_y):
        for block_x in range(blocks_x):
            # Average pixels in block and convert to Nord color
            block_left = block_x * pixel_size
            block_top = block_y * pixel_size
            block_right = block_left + pixel_size
            block_bottom = block_top + pixel_size

            # Crop block region
            block = img.crop((block_left, block_top, block_right, block_bottom))
            block_array = np.array(block)

            # Calculate average color of block
            avg_color = tuple(block_array.mean(axis=(0, 1)).astype(int))
            nord_color = closest_nord_color(avg_color)

            # Draw block to output image
            out_x = block_x * (pixel_size + gap)
            out_y = block_y * (pixel_size + gap)

            for dy in range(pixel_size):
                for dx in range(pixel_size):
                    final_img.putpixel((out_x + dx, out_y + dy), nord_color)

    # Save
    final_img.save(output_path)
    print(f"Conversion complete: {output_path}")
    print(f"Original size: {width}x{height}")
    print(f"Output size: {output_width}x{output_height}")
    print(f"Pixel block size: {pixel_size}x{pixel_size}")
    if gap > 0:
        print(f"Gap between blocks: {gap}px")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nordot.py <input_image> [output_image] [pixel_size] [gap_size]")
        print("Example: python nordot.py input.jpg output.png 8 2")
        print("    pixel_size: Block size for pixelation (default: 8)")
        print("    gap_size: Gap between pixel blocks (0=none, 1-3 recommended)")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "nord_pixel_art.png"
    pixel_size = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    gap = int(sys.argv[4]) if len(sys.argv) > 4 else 0

    convert_to_pixel_art(input_path, output_path, pixel_size, gap)
