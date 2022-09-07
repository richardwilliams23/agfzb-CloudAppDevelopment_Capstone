from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    path(route='about/', view=views.about, name='about'),

    path(route='contact/', view=views.contact, name='contact'),

    path(route='registration/', view=views.registration_request, name='registration'),

    path(route='login/', view=views.login_request, name='login'),

    path(route='logout/', view=views.logout_request, name='logout'),

    # E.g. 127.0.0.1:8000/djangoapp/.  Should return all dealerships.
    path(route='', view=views.get_dealerships, name='index'),
    path(route='index/', view=views.get_dealerships, name='index'),

    # E.g. 127.0.0.1:8000/djangoapp/dealer/13/.  Should return reviews for dealer 13.
    path('dealer/<int:id>/', views.get_dealer_details, name='dealer_details'),

    # E.g. 127.0.0.1:8000/djangoapp/dealer/13/review
    path(route='dealer/<int:id>/add-review', view=views.add_review, name='add_review'),

    # E.g. 127.0.0.1:8000/djangoapp/review/13/
    path(route='review/<int:id>/', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)