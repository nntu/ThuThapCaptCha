from flask import Flask, render_template, request
import requests
from io import BytesIO
import base64
import os
from datetime import datetime
import certifi
app = Flask(__name__)

# Create a directory to store CAPTCHA images
UPLOAD_FOLDER = 'captcha_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_captcha_image():
    try:
        # Download the CAPTCHA image
        response = requests.get('https://tracuunnt.gdt.gov.vn/tcnnt/captcha.png' ,verify=False )
        if response.status_code == 200:
            # Store the raw content for saving later
            image_content = response.content
            # Convert the image to base64 for displaying in HTML
            image_data = base64.b64encode(image_content).decode()
            return image_data, image_content
        return None, None
    except Exception as e:
        print(f"Error fetching CAPTCHA: {e}")
        return None, None

def save_captcha_image(image_content, captcha_text):
    try:
        # Create filename with timestamp to avoid duplicates
         
        filename = f"{captcha_text}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(image_content)
        return filepath
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def captcha_form():
    message = None
    
    if request.method == 'POST':
        captcha_text = request.form.get('captcha')
        image_content = request.form.get('image_content')
        
        if image_content:
            # Decode the base64 image content
            image_content = base64.b64decode(image_content)
            # Save the image
            saved_path = save_captcha_image(image_content, captcha_text)
            if saved_path:
                message = f"CAPTCHA image saved as: {saved_path}"
            else:
                message = "Error saving CAPTCHA image"
        else:
            message = "No image data available"
    
    # Get new CAPTCHA image for both GET and POST requests
    captcha_image, image_content = get_captcha_image()
    
    # If we have image content, encode it for the hidden form field
    image_content_b64 = base64.b64encode(image_content).decode() if image_content else None
    
    return render_template('captcha_form.html', 
                         captcha_image=captcha_image,
                         image_content=image_content_b64,
                         message=message)

if __name__ == '__main__':
    app.run(debug=True)