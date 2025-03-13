from flask import Flask, request, send_file
from PIL import Image
import os

app = Flask(__name__)

# Define image size requirements for different exams (in pixels)
exam_sizes = {
    "UPPSC": {"photo": (300, 400), "signature": (140, 60)},
    "UPSSSC": {"photo": (200, 230), "signature": (140, 60)},
    "UPTET": {"photo": (200, 230), "signature": (140, 60)},
    "UP Police": {"photo": (200, 230), "signature": (140, 60)},
    "UP Junior Assistant": {"photo": (200, 230), "signature": (140, 60)},
    "UP Lekhpal": {"photo": (200, 230), "signature": (140, 60)},
    "UP Teacher Recruitment": {"photo": (200, 230), "signature": (140, 60)},
    "UP Health Department": {"photo": (200, 230), "signature": (140, 60)},
    "UP Power Corporation (UPPCL)": {"photo": (200, 230), "signature": (140, 60)},
    "UP Metro Rail": {"photo": (200, 230), "signature": (140, 60)},
    "UP PGT/TGT": {"photo": (200, 230), "signature": (140, 60)},
    "UP Forest Guard": {"photo": (200, 230), "signature": (140, 60)},
    
    # Central Government Exams
    "UPSC": {"photo": (200, 230), "signature": (140, 60)},
    "SSC": {"photo": (150, 200), "signature": (140, 60)},
    "Bank": {"photo": (180, 220), "signature": (140, 60)},
    "Railway (RRB)": {"photo": (200, 230), "signature": (140, 60)},
    
    "default": {"photo": (200, 200), "signature": (140, 60)}
}

def resize_image(image_path, output_path, size):
    img = Image.open(image_path)
    img = img.resize(size, Image.ANTIALIAS)
    img.save(output_path, quality=95)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'type' not in request.form:
        return {"error": "File or type not provided"}, 400

    file = request.files['file']
    exam = request.form.get('exam', 'default')
    img_type = request.form.get('type')  # "photo" or "signature"

    if exam not in exam_sizes or img_type not in ["photo", "signature"]:
        return {"error": "Invalid exam or type"}, 400

    # Get correct size
    size = exam_sizes[exam][img_type]

    # Save original file
    input_path = f"uploads/{file.filename}"
    output_path = f"uploads/resized_{file.filename}"

    file.save(input_path)
    resize_image(input_path, output_path, size)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
