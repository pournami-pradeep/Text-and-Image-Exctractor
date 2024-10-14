import os
from django.shortcuts import render
from PIL import Image 
from pytesseract import pytesseract
from pdf2image import convert_from_path
from django.http import HttpResponse

def handle_uploaded_file(f):
    file_name = f.name
    os.makedirs("myapp/static/media/", exist_ok=True)
    with open("myapp/static/media/"+file_name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_name

def extract_text_from_image(image):
    extracted_text = pytesseract.image_to_string(image, lang= 'eng')
    return extracted_text


def extract_text_from_pdf(pdf):
  pages = convert_from_path(pdf,last_page=5)
  text = ''
  for page in pages:
    text += str(extract_text_from_image(page))
  
  return text

def check_file(file):
    f = file.split(".")
    file_format = f[1]
    file_path = (os.path.join('myapp/static/media',file))
    if file_format == "pdf":
        data = extract_text_from_pdf(file_path)
    else:
        data = extract_text_from_image(file_path)
    return data

def upload_file(request):
    text = None
    if request.method == 'POST':
        file_save = handle_uploaded_file(request.FILES['upload_file'])
        try:
            text = check_file(file_save)
            if not text:
                extracted_text= "No text available to extract"
            else:
                extracted_text = text
            return render (request,'file_upload.html',{'text': extracted_text})
        except:
            return render (request,'file_upload.html',{'text': "Something went wrong."})
    return render (request,'file_upload.html' )

      


    

