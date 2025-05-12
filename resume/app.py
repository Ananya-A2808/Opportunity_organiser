from flask import Flask, render_template, request, send_file
import os
import pdfkit

app = Flask(__name__)

# Path to wkhtmltopdf executable
config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = request.form.to_dict()
        return render_template("resume.html", data=data)
    return render_template("form.html")


@app.route("/download", methods=["POST"])
def download():
    data = request.form.to_dict()
    html = render_template("resume.html", data=data)

    # Enable local file access to resolve static files
    options = {
        'enable-local-file-access': '',  # Allow local file access
    }

    # Generate the PDF with the necessary options
    pdfkit.from_string(html, "resume.pdf", configuration=config, options=options)

    return send_file("resume.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
