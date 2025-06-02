#!/usr/bin/env python3
"""
Simple script to create an icon for BlackzAllocator
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for BlackzAllocator"""
    # Create a 256x256 image with dark background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle background
    margin = 20
    bg_color = (30, 30, 30, 255)  # Dark gray
    draw.rounded_rectangle(
        [margin, margin, size-margin, size-margin], 
        radius=40, 
        fill=bg_color
    )
    
    # Draw a network/pool symbol
    center_x, center_y = size // 2, size // 2
    
    # Draw network nodes (circles)
    node_color = (0, 123, 255, 255)  # Blue
    node_radius = 15
    
    # Central node
    draw.ellipse(
        [center_x-node_radius, center_y-node_radius, 
         center_x+node_radius, center_y+node_radius], 
        fill=node_color
    )
    
    # Surrounding nodes
    import math
    for i in range(6):
        angle = i * (2 * math.pi / 6)
        x = center_x + 60 * math.cos(angle)
        y = center_y + 60 * math.sin(angle)
        draw.ellipse(
            [x-node_radius//2, y-node_radius//2, 
             x+node_radius//2, y+node_radius//2], 
            fill=node_color
        )
        
        # Draw lines to center
        draw.line([center_x, center_y, x, y], fill=node_color, width=3)
    
    # Add "B" text for BlackzAllocator
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Get text size and center it
    text = "B"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 + 60
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save as ICO file
    img.save('blackz_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("✅ Icon created: blackz_icon.ico")

if __name__ == "__main__":
    create_icon() 