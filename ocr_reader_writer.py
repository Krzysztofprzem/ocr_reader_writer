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
        print("The directory %s already exists" % path)
    else:
        print("Successfully created the directory %s " % path)


def check_size(path):
    file_size_B = os.stat(path).st_size
    file_size_KB = file_size_B/1024.0
    
    if file_size_KB > 1024:
        return False, file_size_B
    else:
        return True, file_size_B


def compression(input_path, output_path, compression_factor=0.8):
    im = Image.open(input_path)  

    width, height = im.size  
    width_new  = int(width*compression_factor)
    height_new = int(height*compression_factor)
    newsize = (width_new, height_new) 

    im = im.resize(newsize) 
    im.save(output_path)


def compressator(path, compression_factor=0.8):
    temp_path = "temp\\" + path.split("\\")[-1]
    compression(path, temp_path)

    while check_size(temp_path)[0] is False:
        compression(temp_path, temp_path, compression_factor)

    return temp_path


def preprocess(filename_str):
    good_size, _ = check_size(filename_str)
    if good_size is False:
        temp_path = compressator(filename_str)
        return False, temp_path
    else:
        return True, filename_str


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

        files = {filename: f}
        data = {"apikey": apikey, 
                "language": language}

        result = requests.post(url_api, files=files, data=data)
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
        # Convert filename into string
        filename_str = str(filename)

        # Create catalog tree in outputpath for each image 
        index = filename_str.rfind("\\")
        directory_path = output_path+filename_str[:index]
        create_necessary_directories(directory_path)

        # Check if image has size bigger than 1024KB
        good_size, filename_new = preprocess(filename_str)

        # Send image to ocr space
        text_detected = ocrspace_call(filename_new, apikey, language, True)

        # If image had size bigger than 1024KB remove temporary compressed image
        if good_size is False:
            os.remove(filename_new)

        # Save detected text into text file
        outputtextfilepath = output_path+filename_str[:-3]+"txt"
        textfile = open(outputtextfilepath, 'w', encoding='utf8')
        textfile.write(text_detected)
        textfile.close()

        # In order to not getting banned from ocr space
        time_start = time.time()
        while time.time() - time_start < interval:
            continue



if __name__ == "__main__":
    ocr_reader_writer()