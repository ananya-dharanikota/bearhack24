from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from vertex_ai import predict_image_classification_sample, compress_image
import skin_conditions

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
            image_path = url_for("static", filename="images/" + image.filename)
            file_path = str(Path.cwd()) + "/bearhack24/static/images/" + image.filename
            image.save(file_path)
            image_compressed = compress_image(file_path)
            results = predict_image_classification_sample(filename=image_compressed)
            overview = skin_conditions.print_description(results)
            symptoms = skin_conditions.print_symptoms(results)
            causes = skin_conditions.print_symptoms(results)
            print(overview, "CMON MAN")
            print(symptoms, "PLEASE")
            print(causes, 'OKAY')
            # You might want to pass some variables or results to the template
            print(image.filename)
            return render_template("results.html", user_pic=image_path, overview=overview, symptoms=symptoms, causes=causes)
        else:
            return redirect(request.url)
    else:
        # If someone navigates to /results without posting
        return redirect(url_for("home"))

app.run(port=5500)