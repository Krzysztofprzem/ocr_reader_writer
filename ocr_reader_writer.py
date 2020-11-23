from pathlib import Path
import json
import numpy as np
import requests
import time
from PIL import Image
import os


def create_necessary_directories(path):
    try:
        os.makedirs(path)
    except OSError:
        print ("The directory %s already exists" % path)
    else:
        print ("Successfully created the directory %s " % path)


def ocrspace_call(filename="kawaii.jpg", apikey="helloworld", language="jpn", printing=False):
    """
    Method to scrape text string from image saved on disk
    :param filename: path to image
    :param apikey: shouldn't be equal to "helloworld" unless method is used to test less than or equal to 10 times (look on https://ocr.space/ocrapi)
    :param language: language (look on https://ocr.space/ocrapi)
    :param printing: if True then printing debugging stuff
    :return: text from image
    """

    url_api = "https://api.ocr.space/parse/image"
    with open(filename, "rb") as f:

        result = requests.post(url_api,
                    files = {filename: f},
                    data = {"apikey": apikey,
                            "language": language})

        result = result.content.decode()
        result = json.loads(result)

        if printing:
            print(result)

        parsed_results = result.get("ParsedResults")[0]
        text_detected = parsed_results.get("ParsedText")
        return text_detected


def ocr_reader_writer():
    # Load ocr reader writer data
    ocr_rw_data_path = "my_ocr_rw_data.json"
    ocr_rw_data = json.load(open(ocr_rw_data_path))

    # Unpack ocr reader writer data
    input_path = ocr_rw_data["input_path"]
    output_path = ocr_rw_data["output_path"]
    apikey = ocr_rw_data["apikey"]
    language = ocr_rw_data["language"]
    interval = ocr_rw_data["interval"]

    # Get paths to all images in input_path
    filenames = Path(input_path).rglob('*.jpg')
    for filename in filenames:
        # Create catalog tree in outputpath for each image 
        index = str(filename).rfind("\\")
        directory_path = output_path+str(filename)[:index]
        create_necessary_directories(directory_path)

        # Send image to ocr space and get text result
        filename = "00127.jpg"
        text_detected = ocrspace_call(str(filename), apikey, language, False)
        print(text_detected)

        # Save detected text into text file
        outputtextfilepath = output_path+str(filename)[:-3]+".txt"
        textfile = open(outputtextfilepath, 'w', encoding='utf8')
        textfile.write(text_detected)
        textfile.close()

        # In order to not getting banned from ocr space
        time_start = time.time()
        while time.time() - time_start < interval:
            continue
        break


if __name__ == "__main__":
    ocr_reader_writer()