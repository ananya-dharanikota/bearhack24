from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from vertex_ai import predict_image_classification_sample, compress_image


print()
template_path = str(Path.cwd()) + "/bearhack24/templates"
app = Flask(__name__, template_folder=template_path)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/results.html", methods=["POST", "GET"])
def upload_img():
    if request.method == "POST":
        image = request.files['myfile']
        if image:
            # Here you could process the file or save it
            image_path = str(Path.cwd()) + "/bearhack24/user_pic/" + image.filename  # Ensure the path exists
            image.save(image_path)
            image_compressed = compress_image(image_path)
            results = predict_image_classification_sample(filename=image_compressed)
            # You might want to pass some variables or results to the template
            print(image.filename)
            return render_template("results.html", results=results)
        else:
            return redirect(request.url)
    else:
        # If someone navigates to /results without posting
        return redirect(url_for("home"))

app.run(port=5500)