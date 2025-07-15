from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    name = request.json.get("name", "Happy User")
    
    # Load base image
    base = Image.open("birthday_template.png").convert("RGBA")
    draw = ImageDraw.Draw(base)
    
    # Use a TTF font (ensure Arial.ttf is in the folder or use another font)
    font = ImageFont.truetype("Poppins-Medium.ttf", 60)
    draw.text((220, 295), name, fill=(160, 32, 240), font=font)
    
    # Output to memory
    img_io = io.BytesIO()
    base.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')