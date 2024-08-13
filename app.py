from flask import Flask, request, jsonify, send_file
from PIL import Image
import cv2
import numpy as np
import io

app = Flask(__name__)

def compress_image_opencv(image, quality=20, downscale_factor=2):
    # Convert PIL Image to NumPy array
    img_array = np.array(image)

    # Convert RGB to BGR (as OpenCV uses BGR)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Downscale the image to reduce the resolution
    new_width = img_array.shape[1] // downscale_factor
    new_height = img_array.shape[0] // downscale_factor
    img_array = cv2.resize(img_array, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Encode the image using JPEG format with specified quality
    _, encoded_img = cv2.imencode('.jpg', img_array, [cv2.IMWRITE_JPEG_QUALITY, quality])

    # Convert the encoded image to BytesIO
    output = io.BytesIO(encoded_img.tobytes())
    return output

def add_watermark(image, text, opacity=0.1):
    # Convert PIL Image to NumPy array
    img_array = np.array(image)

    # Convert RGB to BGR (as OpenCV uses BGR)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Define font and watermark parameters
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 0, 0)  # Light gray
    thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    
    # Create an overlay image for the watermark
    overlay = img_array.copy()
    
    # Add watermark in a grid pattern
    spacing_x, spacing_y = text_size[0] + 50, text_size[1] + 50
    for y in range(0, img_array.shape[0], spacing_y):
        for x in range(0, img_array.shape[1], spacing_x):
            cv2.putText(overlay, text, (x, y), font, font_scale, font_color, thickness)
    
    # Blend the overlay with the original image
    cv2.addWeighted(overlay, opacity, img_array, 1 - opacity, 0, img_array)
    
    # Convert BGR back to RGB
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

    # Convert back to PIL Image
    img_pil = Image.fromarray(img_array)
    return img_pil

@app.route('/hello', methods=['GET'])
def say_hello():
    return "Hello, World!"

@app.route('/api/compress', methods=['POST'])
def compress():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    file = request.files['image']
    image = Image.open(file)
    quality = int(request.form.get('quality', 20))  # Default quality is 20 if not provided
    downscale_factor = int(request.form.get('downscale_factor', 2))  # Default downscale factor is 2 if not provided
    compressed_image = compress_image_opencv(image, quality, downscale_factor)
    return send_file(compressed_image, mimetype='image/jpeg')

@app.route('/api/watermark', methods=['POST'])
def watermark():
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Image and text are required'}), 400
    file = request.files['image']
    text = request.form['text']
    opacity = float(request.form.get('opacity', 0.1))  # Default opacity is 0.1 if not provided
    image = Image.open(file)
    watermarked_image = add_watermark(image, text, opacity)
    output = io.BytesIO()
    watermarked_image.save(output, format='JPEG')
    output.seek(0)
    return send_file(output, mimetype='image/jpeg')


# New route that combines both functionalities
@app.route('/api/updateImage', methods=['POST'])
def update_image():
    if 'image' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Image and text are required'}), 400
    file = request.files['image']
    text = request.form['text']
    quality = int(request.form.get('quality', 20))
    downscale_factor = int(request.form.get('downscale_factor', 2))
    opacity = float(request.form.get('opacity', 0.1))

    # Open the image
    image = Image.open(file)

    # Apply watermark
    watermarked_image = add_watermark(image, text, opacity)

    # Compress the watermarked image
    compressed_image = compress_image_opencv(watermarked_image, quality, downscale_factor)

    return send_file(compressed_image, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
