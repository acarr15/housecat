from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import artist, artist_tag, tag, status, region
from .forms import ArtistForm, MediaForm, TagsForm, EditForm, TagForm, RegionForm, SearchForm
from django.contrib.auth.decorators import login_required

PENDING, APPROVED, DENIED = 1, 2, 3

def index(request):
	return render(request, "db_app/index.html", {})

def search(request):
	if 'submit' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			# Tag PKs
			tags = request.GET.getlist("tags") 
			# Region PKs
			regions = request.GET.getlist("regions")
			# Name Value
			name = request.GET.get("name")

			artists = artist.objects.filter(status=status.objects.get(id=APPROVED))
			if regions:
				artists = artists.filter(region_id__in=list(region.objects.filter(pk__in=regions)))
			if tags:
				artist_tags = artist_tag.objects.values_list("artist", flat=True).filter(tag__in=list(tag.objects.filter(pk__in=tags)))
				artists = artists.filter(pk__in=list(set(artist_tags)))
			if name:
				artists = artists.filter(name__icontains=name)

			print(artists)	

			return render(request, "db_app/results.html", {"artists": artists})
	else:
		form = SearchForm()
	return render(request, "db_app/search.html", {"form":form})

def results(request):
	# approved = status.objects.get(id=APPROVED)
	# artists = artist.objects.filter(status=approved)
	artists = artist.objects.all()
	return render(request, "db_app/results.html", {"artists": artists})

@login_required
def secure(request, value=PENDING):
	artists = artist.objects.filter(status=status.objects.get(id=value))
	return render(request, "db_app/secure.html", {"artists": artists})

@login_required
def edit_artist(request, pk):
	edit = get_object_or_404(artist, pk=pk)
	if request.method == "POST":
		form = EditForm(request.POST)
		if form.is_valid():
			edit.genre = request.POST.get("genre")
			edit.status = status.objects.get(id=request.POST.get("status"))
			edit.region_id = region.objects.get(id=request.POST.get("region_id"))
			edit.save()
			return redirect("secure_default")
	else:
		form = EditForm(initial={"genre":edit.genre, "status":edit.status, "region_id": edit.region_id})
	return render(request, "db_app/edit_artist.html", {"edit":edit, "form":form})

@login_required
def remove_artist(request, pk):
	remove = get_object_or_404(artist, pk=pk)
	remove.delete()
	return redirect("secure_default")

@login_required
def add_tag(request):
	if request.method == "POST":
		form = TagForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("secure_default")
	else:
		form = TagForm()
	return render(request, "db_app/add_tag.html", {"form":form})

@login_required
def add_region(request):
	if request.method == "POST":
		form = RegionForm(request.POST)
		if form.is_valid():
			new_tag = tag(tag=request.POST.tag)
			new_tag.save()
			return redirect("secure_default")
	else:
		form = RegionForm()
	return render(request, "db_app/add_region.html", {"form":form})

def submission(request):
	if request.method == "POST":
		artist_form, media_form, tags_form = ArtistForm(request.POST), MediaForm(request.POST), TagsForm(request.POST)
		if artist_form.is_valid() and media_form.is_valid() and tags_form.is_valid():
			artist = artist_form.save()

			media = media_form.save(commit=False)
			media.artist = artist
			media.save()

			tags = request.POST.getlist("tags")
			for value in tags:
				new_entry = artist_tag(artist=artist, tag=tag.objects.get(id=value))
				new_entry.save()

			return HttpResponse("Thanks!")
	else:
		artist_form, media_form, tags_form = ArtistForm(), MediaForm(), TagsForm()
	return render(request, "db_app/submission.html", {"artist_form": artist_form, "media_form": media_form, "tags_form": tags_form})



