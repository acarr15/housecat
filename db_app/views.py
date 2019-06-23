from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import artist, artist_tag, tag, status, region, media
from .forms import ArtistForm, MediaForm, TagsForm, EditForm, TagForm, RegionForm, SearchForm
from django.contrib.auth.decorators import login_required

APPROVED, PENDING, DENIED = 1, 2, 3

def index(request):
	return render(request, "db_app/index.html", {})

def results(request):
	artistData = media.objects.select_related('artist').filter(artist__status=status.objects.get(id=APPROVED))

	if 'submit' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			# Tag PKs
			tags = request.GET.getlist("tags") 
			# Region PKs
			regions = request.GET.getlist("regions")
			# Name Value
			name = request.GET.get("name")
			if regions:
				artistData = artistData.filter(artist__region_id__in=list(region.objects.filter(pk__in=regions)))
			if tags:
				artist_tags = artist_tag.objects.values_list("artist", flat=True).filter(tag__in=list(tag.objects.filter(pk__in=tags)))
				artistData = artistData.filter(artist__id__in=list(set(artist_tags)))
			if name:
				artistData = artistData.filter(artist__name__icontains=name)

			return render(request, "db_app/results.html", {"artistData": artistData, "form":form})
	else:
		form = SearchForm()
	return render(request, "db_app/results.html", {"artistData": artistData, "form":form})

@login_required
def secure(request, value=PENDING):
	artists = artist.objects.filter(status=status.objects.get(id=value))
	return render(request, "db_app/secure.html", {"artists": artists})

@login_required
def edit_artist(request, pk):
	edit = get_object_or_404(artist, pk=pk)
	edit_media = get_object_or_404(media, pk=pk)
	edit_tags = artist_tag.objects.values_list('tag', flat=True).filter(artist=edit)
	if request.method == "POST":
		artist_form, media_form, tags_form = ArtistForm(request.POST), MediaForm(request.POST), TagsForm(request.POST)
		# if artist_form.is_valid() and media_form.is_valid() and tags_form.is_valid():
		form = EditForm(request.POST)
		if form.is_valid():
			edit.genre = request.POST.get("genre")
			edit.status = status.objects.get(id=request.POST.get("status"))
			edit.region_id = region.objects.get(id=request.POST.get("region_id"))
			edit.save()
			return redirect("secure_default")
	else:
		tags_form = TagsForm(initial={"tags": edit_tags})
		media_form = MediaForm(initial={"facebook": edit_media.facebook, "instagram": edit_media.instagram, 'twitter': edit_media.twitter, 'bandcamp':edit_media.bandcamp, 'soundcloud':edit_media.soundcloud, 'tumblr':edit_media.tumblr, 'patreon':edit_media.patreon, 'website':edit_media.website})
		artist_form = ArtistForm(initial={"name": edit.name, "hometown": edit.hometown, "email":edit.email, "genre":edit.genre, "status":edit.status, "region_id": edit.region_id})
		form = EditForm(initial={"genre":edit.genre, "status":edit.status, "region_id": edit.region_id})
	return render(request, "db_app/edit_artist.html", {"edit":edit, "form":form, "artist_form": artist_form, "media_form": media_form, "tags_form": tags_form})

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
			form.save()
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

			return render(request, "db_app/thanks.html", {})
	else:
		artist_form, media_form, tags_form = ArtistForm(), MediaForm(), TagsForm()

	return render(request, "db_app/submission.html", {"artist_form": artist_form, "media_form": media_form, "tags_form": tags_form})


