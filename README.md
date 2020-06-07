# TweetMe

## Description

It is a simulating app for the Twitter website 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages:

```
pip install Django==2.2.5
pip install django-crispy-forms==1.7.2
pip install django-filter==2.2.0
pip install djangorestframework==3.10.3
pip install Markdown==3.1.1
pip install django-location-field
```

## Urls

  1.I have created django rest framework to easily retrieve the tweets 
  and the user details
  
  
   . [To get the tweets](http://127.0.0.1:8000/api/tweet/)
      
      
   . [To create a new tweet](http://127.0.0.1:8000/api/tweet/create/)
   
   
  2.I have customized the user model to be Myuser
  
   > N.B: i used the same urls of django.contrib.auth.urls
   
   . [To update the user profile](http://127.0.0.1:8000/accounts/profile)
   
   

## Usage

Connecting People  :busts_in_silhouette:

## Built with 
 . [Django](https://docs.djangoproject.com/en/2.2/) 
 
 . [Rest framework](https://django-rest-framework.org)
 
 . [Jquery](https://learn.jquery.com/)
 
 . [Bootstrap](https://getbootstrap.com/)
 
 . [cripsy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
 
 
## Contributing
 
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

 ## Project status
 
The website is under construction, stay tuned for the final version.