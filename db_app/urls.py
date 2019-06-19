from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.index, name="index"),
	path('search/', views.search, name="search"),
	path('results/', views.results, name="results"),
	path('secure/', views.secure, name="secure_default"),
	path('submission/', views.submission, name="submission"),
	path('edit/<int:pk>/', views.edit_artist, name="edit_artist"),
	path('remove/<int:pk>/', views.remove_artist, name="remove_artist"),
	path('secure/<int:value>/', views.secure, name="secure"),
	path('add_tag/', views.add_tag, name="add_tag"),
	path('add_region', views.add_region, name="add_region"),
	url(r'^select2/', include('django_select2.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)