
'''

brew install python3
brew install fontforge

python3 convert_ttf.py

'''

import fontforge
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Define the basic paths
svg_dir = 'svg'
ttf_dir = 'ttf'
output_font_file = os.path.join(ttf_dir, 'weathericons.ttf')
output_xml_file = os.path.join(ttf_dir, 'weathericons.xml')

# Create a new font object
font = fontforge.font()

# Set the basic information of the font
font.fontname = "weathericons"
font.fullname = "Weather Icons"
font.familyname = "Weather Icons"

# Initialize the Unicode code point, starting from 0xf001
unicode_value = 0xf001

# Create the PNG directory if it does not exist
if not os.path.exists(ttf_dir):
    os.makedirs(ttf_dir)

# Create the root element of the XML
root = ET.Element('resources')

# Traverse all SVG files in the SVG directory
for svg_file in os.listdir(svg_dir):
    if svg_file.endswith('.svg'):
        # Get the icon name (remove the file extension) and replace '-' with '_'
        icon_name = os.path.splitext(svg_file)[0].replace('-', '_')

        # Create a new glyph
        glyph = font.createChar(unicode_value)

        # Import the SVG file into the glyph
        glyph.importOutlines(os.path.join(svg_dir, svg_file))

        # Automatically adjust the outline of the glyph
        glyph.removeOverlap()
        glyph.simplify()

        # Create an XML element, using the &#x...; format to represent Unicode
        string_element = ET.SubElement(root, 'string', name=icon_name)
        string_element.text = f"&#x{unicode_value:04x};"

        # Increment the Unicode code point
        unicode_value += 1

# Generate the TTF file
font.generate(output_font_file)
print(f"TTF file has been generated: {output_font_file}")

# Generate the XML file
# Use a custom function to generate the XML string and avoid escaping the & symbol
def custom_tostring(element, encoding='utf-8'):
    rough_string = ET.tostring(element, encoding=encoding, method='xml')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ").replace('&amp;#x', '&#x')

xml_content = custom_tostring(root)

# Write to the XML file
with open(output_xml_file, 'w', encoding='utf-8') as f:
    f.write(xml_content)
print(f"XML index file has been generated: {output_xml_file}")
