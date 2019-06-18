from django import forms
from .models import artist, media, tag, region
from django.contrib.admin.widgets import FilteredSelectMultiple

class ArtistForm(forms.ModelForm):
	class Meta:
		model = artist
		fields = ('name', 'genre', 'region_id', 'hometown', 'email')

class MediaForm(forms.ModelForm):
	class Meta:
		model = media
		fields = ('facebook', 'instagram', 'twitter', 'bandcamp', 'soundcloud', 'tumblr', 'patreon', 'website')

	def __init__(self, *args, **kwargs):
		super(MediaForm, self).__init__(*args, **kwargs)
		for key in self.fields:
			self.fields[key].required = False

class TagsForm(forms.Form):
	tags = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=tag.objects.all(), required=False, widget=FilteredSelectMultiple(_('tags'), True))
	
	# def __init__(self, *args, **kwargs):
	# 	super(TagsForm, self).__init__(*args, **kwargs)
	# 	self.fields['tags'].widget = forms.HiddenInput()

class EditForm(forms.ModelForm):
	class Meta:
		model = artist
		fields = ('genre', 'status', 'region_id')

class TagForm(forms.ModelForm):
	class Meta:
		model = tag
		fields = ('tag', )

class RegionForm(forms.ModelForm):
	class Meta:
		model = region
		fields = ('region', )

class SearchForm(forms.Form):
	name = forms.CharField(empty_value="Search by Name", required=False)
	regions = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=region.objects.all(), required=False)
	tags = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=tag.objects.all(), required=False)



	