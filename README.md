# OCR Reader Writer


#### Technologies
Project was created and tested with:
* Windows 10
* Python 3.8.2
* Tesseract v5.0.0-alpha.20200328
* OCR Space

This project was tested with .jpg and .png only images.


#### Description
Project created in order to automate process of extracting text from images set into textfiles. This currently supports only .jpg and .png images extensions.


#### Example application
This project can be used in order to extract text from large amount of images with use of Tesseract or OCR Space technology. User can place directory tree with images into "ocr_reader_writer\input" catalogue, and texts from all images will be saved into .txt files in identical directory tree in "ocr_reader_writer\output" catalogue.


#### Setup
- Run command in ocr_reader_writer\ catalogue:
```
python -m virtualenv venv
cd venv
cd Scripts
activate
cd ..
cd ..
pip install -r requirements.txt
```
- In order to use Tesseract, download it from one of links from https://tesseract-ocr.github.io/tessdoc/Downloads.html (Tesseract used in testing was downloaded from https://github.com/UB-Mannheim/tesseract/wiki) and install it
- For OCR Space use, register on page https://ocr.space/ocrapi in order to get apikey
- Adjust ocr_reader_writer\ocr_rw_data.json file by setting correct paths and language settings


#### Run
Go to ocr_reader_writer\ and run command:
```
python ocr_reader_writer.py
```