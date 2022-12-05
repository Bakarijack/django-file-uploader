from django.shortcuts import render, redirect
from .models import Post
from pdf2image import convert_from_path
import os
from django.conf import settings

COVER_PAGE_DIRECTORY = 'cover/'
COVER_PAGE_FORMAT = 'jpg'
# Create your views here.
def set_cover_file_name(file_name):
    return os.path.join(COVER_PAGE_DIRECTORY, '{}.{}'.format(file_name, COVER_PAGE_FORMAT))
    
def convert_pdf_to_image(path, pdf_name):
    cover_page_dir = os.path.join(settings.MEDIA_ROOT, COVER_PAGE_DIRECTORY)
    
    if not os.path.exists(cover_page_dir):
        os.mkdir(cover_page_dir)
        
    cover_page_image = convert_from_path(
        pdf_path='media/pdf/'+path,
        dpi=200, 
        first_page= 1, 
        last_page= 1, 
        fmt=COVER_PAGE_FORMAT, 
        output_folder=cover_page_dir,
        )[0]
    
    new_cover_page_path = '{}.{}'.format(os.path.join(cover_page_dir, pdf_name), COVER_PAGE_FORMAT)
    print(new_cover_page_path)
    
    os.rename(cover_page_image.filename, new_cover_page_path)

    #return cover_page_image.filename

def uploadFile(request):
    if request.method == 'POST':
        fileName = request.POST['fileName']
        fileUrl = request.FILES['uploadedFile']
        
        pdf_name = str(fileUrl)
        real_pdf_name = pdf_name[:-4]
        print(real_pdf_name)
        
        post = Post.objects.create(name=fileName, fileUrl=fileUrl)
        convert_pdf_to_image(str(fileUrl), real_pdf_name)
        post.cover = COVER_PAGE_DIRECTORY + f'{real_pdf_name}.jpg'
        post.save()
        #set_cover_file_name(pdf_name)
        
        
    return render(request, 'home.html')