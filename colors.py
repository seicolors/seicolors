import numpy as np
import os
import json
from PIL import Image

# Create directory if necessary
if not os.path.exists("colors_nft"): os.makedirs("colors_nft")

# Primary Colors and Palettes
primary_colors = ["Red", "Blue", "Yellow"]
color_palettes = {"Red": [(255, g, g) for g in range(256)], "Blue": [(b, b, 255) for b in range(256)], "Yellow": [(255, 255, y) for y in range(256)]}

# Function to generate unique monochromatic colors
def generate_monochromatic(image_number, primary_color):
    np.random.seed(image_number) # Seed to ensure uniqueness
    color_range = color_palettes[primary_color]
    pixels = np.random.choice(len(color_range), size=(41 * 41))
    return np.array([color_range[p] for p in pixels])

# Function to generate an image
def generate_image(image_number):
    if image_number == 0: pixel_colors = np.full((41 * 41, 3), (255, 255, 255)) # All white
    elif 1 <= image_number <= 100: pixel_colors = generate_monochromatic(image_number, primary_colors[(image_number - 1) // 34]) # Rare monochromatic NFTs
    else: pixel_colors = np.random.randint(0, 256, (41 * 41, 3)) # Normal NFTs
    img = Image.fromarray(pixel_colors.reshape(41, 41, 3).astype('uint8'), 'RGB')
    img = img.resize((1010, 1010), Image.NEAREST)
    img.save(f"colors_nft/{image_number}.png")
    color_counts = {"Red": 0, "Blue": 0, "Yellow": 0, "White": 0, "Black": 0} # Color count
    for color in pixel_colors:
        if tuple(color) == (255, 255, 255): color_counts["White"] += 1
        elif tuple(color) == (0, 0, 0): color_counts["Black"] += 1
        else:
            added = False
            for primary_color in primary_colors:
                if tuple(color) in color_palettes[primary_color]: color_counts[primary_color] += 1; added = True; break
            if not added: color_counts[np.random.choice(primary_colors)] += 1 # Add a random count if the color does not match any primary palette
    return color_counts

# Function to create metadata
def create_metadata(image_number, color_counts):
    metadata = {
        "name": f"Sei Colors #{image_number}",
        "symbol": "Colors",
        "description": "10,101 unique NFTs, each a masterpiece capturing one of the 16,777,216 RGB colors that paint our world. A vibrant tribute to the community!",
        "image": f"{image_number}.png",
        "edition": image_number,
        "attributes": [{"trait_type": color, "value": f"{color_counts[color]}px"} 
                       for color in ["White", "Black", "Red", "Blue", "Yellow"]]
    }
    return metadata

# Generate images and metadata
for i in range(10101):
    color_counts = generate_image(i)
    metadata = create_metadata(i, color_counts)
    with open(f"colors_nft/{i}.json", "w") as json_file: json.dump(metadata, json_file, indent=2)

print("All PNG images and metadata have been generated in the 'colors_nft' folder.")