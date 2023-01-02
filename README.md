# DjangoNoteEditor

A Simple note editor in Django.

### Installing instruction

pip install -r requirements.txt

Create .env file in same folder as settings.py with following content 
"""
cloud_name='cloud_name'
api_key='api_key'
api_secret='api_secret'
api_proxy=http://proxy.server:3128
"""
api_proxy is only need if deployed at PythonAnywhere where communication to outside severs need to be done via their proxyserver. PythonAnywhere's proxyservers whitelist can viewed [here](https://www.pythonanywhere.com/whitelist/).

Alternativly change NoteImage to use django.db.models.imagefield instead of cloudinary.models.CloudinaryField. 

CLOUDINARY is a service which enables to upload and download images.
CLOUDINARY django sample project: https://github.com/cloudinary/cloudinary-django-sample. 

### Test online
You can test the app online via this [link](http://asmail.eu.pythonanywhere.com/editor) until Thursday 30 March 2023. Create a account or log in with
"RandomPerson" as username and "simple-Password1" as password.

### run

python manage.py runserver

# preview

## home page

![](./preview_images/img1.png)

#

## note view page

![](./preview_images/img4.png)

#

## note search page

![](./preview_images/img5.png)

#

## home page for smartphone

<p align="center">
  <img src="./preview_images/img2.png"/>
  <br>
<a href ="https://www.moviezine.se/nyheter/batman-the-animated-series-fyller-25-ar"> batman img source </a>
</p>
