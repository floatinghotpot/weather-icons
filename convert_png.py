
'''

brew install python3
brew install cairo pango gdk-pixbuf libxml2 libxslt libffi

# install & run cairosvg in virtual environment

python3 -m venv myenv
source myenv/bin/activate
pip3 install cairosvg
python3 convert_png.py
deactivate

'''

import os
import cairosvg

# Define the SVG and PNG directories
svg_dir = 'svg'
png_dir = 'png'

# Create the PNG directory if it does not exist
if not os.path.exists(png_dir):
    os.makedirs(png_dir)

# Iterate through all SVG files in the SVG directory
for filename in os.listdir(svg_dir):
    if filename.endswith('.svg'):
        # Construct the full path of the SVG file
        svg_path = os.path.join(svg_dir, filename)
        # Construct the full path of the PNG file
        png_filename = os.path.splitext(filename)[0] + '.png'
        png_path = os.path.join(png_dir, png_filename)

        try:
            # Convert the SVG file to a PNG file and set the image pixels to 256x256
            cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=256, output_height=256)
            print(f"Converted {svg_path} to {png_path}")
        except Exception as e:
            print(f"Error converting {svg_path}: {e}")
