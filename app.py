from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Birthday Card API is running!",
        "endpoints": {
            "generate": "/generate (POST) - Generate a birthday card image",
            "health": "/health (GET) - Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "API is running"})

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        # Get name from JSON payload, default to "Happy User" if not provided
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        name = data.get("name", "Happy User")
        
        # Check if required files exist
        template_path = "birthday_template.png"
        font_path = "Poppins-Medium.ttf"
        
        if not os.path.exists(template_path):
            return jsonify({"error": "Template image not found"}), 500
        
        if not os.path.exists(font_path):
            return jsonify({"error": "Font file not found"}), 500
        
        # Load base image
        base = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(base)
        
        # Use a TTF font
        font = ImageFont.truetype(font_path, 60)
        
        # Add the name to the image at specified coordinates
        draw.text((220, 295), name, fill=(160, 32, 240), font=font)
        
        # Output to memory
        img_io = io.BytesIO()
        base.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png', as_attachment=False)
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate image: {str(e)}"}), 500

@app.route('/generate', methods=['GET'])
def generate_info():
    return jsonify({
        "message": "Use POST method to generate birthday card",
        "required_payload": {
            "name": "string (required) - Name to put on the birthday card"
        },
        "example": {
            "name": "John Doe"
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ✅ This is required for Render!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)