from google.cloud import aiplatform
import os
import io
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv
import base64
load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

endpoint_id = "4623338642658557952"
# image_path = "/Users/bryannguyen/Downloads/IMG_1027.jpg"  # CHANGE TO USER PHOTO INPUT

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict

static_images_path = str(Path.cwd()) + "/static/images/"  # Change to correct static images path

def compress_image(input_file_path, max_size=1500000, quality_step=5):
    """
    Compress an image and save it such that its size does not exceed max_size.
    
    Args:
    input_file_path (str): The path to the original image file.
    max_size (int, optional): Maximum file size in bytes. Defaults to 1.5 MB.
    quality_step (int, optional): The decremental step in quality during compression iterations. Defaults to 5.
    """
    # Open the image
    img = Image.open(input_file_path)
    
    # In-memory file-like object
    img_bytes = io.BytesIO()
    
    # Initial compression attempt
    quality = 95
    while True:
        img_bytes.seek(0)  # Rewind to the beginning of the file-like object
        img.save(img_bytes, format='JPEG', quality=quality)
        size = img_bytes.tell()  # Get the size of the in-memory file
        if size <= max_size or quality <= 10:
            break
        quality -= quality_step  # Decrease quality to further reduce file size
    
    # Save the final compressed image
    output_file_path = static_images_path + "file.jpg"
    img_bytes.seek(0)  # Rewind to the beginning of the file-like object
    img = Image.open(img_bytes)
    img.save(output_file_path, 'JPEG')
    return output_file_path

def predict_image_classification_sample(
    filename: str,
    project: str = "1033084311617",
    endpoint_id: str = "4623338642658557952",
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageClassificationPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
    parameters = predict.params.ImageClassificationPredictionParams(
        confidence_threshold=0.5,
        max_predictions=5,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_classification_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))
        result = dict(prediction)
        diagnosis = result["displayNames"]
        confidences = result["confidences"]
        diagnosis_confidence_dict = dict(zip(diagnosis, confidences))
        most_confident_diagnosis = max(diagnosis_confidence_dict, key=diagnosis_confidence_dict.get)
        print(most_confident_diagnosis)
        return most_confident_diagnosis


# predict_image_classification_sample(
#     filename=compress_image("/Users/vincenthoang/Downloads/vincentacne.JPG")
# )