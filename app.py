from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    name = request.json.get("name", "Happy User")
    
    # Load base image
    base = Image.open("birthday_template.png").convert("RGBA")
    draw = ImageDraw.Draw(base)
    
    # Use a TTF font
    font = ImageFont.truetype("Poppins-Medium.ttf", 60)
    draw.text((220, 295), name, fill=(160, 32, 240), font=font)
    
    # Output to memory
    img_io = io.BytesIO()
    base.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

# ✅ This is required for Render!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
