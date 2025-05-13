from flask import Flask, render_template, request, send_file, url_for
import os
import pdfkit
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Path to wkhtmltopdf executable
config = pdfkit.configuration(
    wkhtmltopdf=r"/usr/local/bin/wkhtmltopdf"
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = request.form.to_dict()
        
        # Handle image upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                data['profile_image'] = url_for('static', filename=f'uploads/{filename}')
        
        return render_template("resume.html", data=data)
    return render_template("form.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.form.to_dict()
    
    # Handle image in the data
    if 'profile_image' in data:
        # Convert image to base64 for PDF embedding
        image_path = os.path.join(app.root_path, data['profile_image'].lstrip('/'))
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                data['profile_image'] = f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"
    
    html = render_template("resume.html", data=data)

    # Enable local file access and set PDF options
    options = {
        'enable-local-file-access': '',
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'no-outline': None,
        'quiet': ''
    }

    # Generate the PDF with the necessary options
    pdfkit.from_string(html, "resume.pdf", configuration=config, options=options)

    return send_file("resume.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
