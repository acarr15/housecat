from django import forms
from .models import artist, media, tag, region

class ArtistForm(forms.ModelForm):
	class Meta:
		model = artist
		fields = ('name', 'genre', 'region_id', 'hometown', 'email')

	def __init__(self, *args, **kwargs):
		super(ArtistForm, self).__init__(*args, **kwargs)
		self.fields['region_id'].label = 'Region'
		self.fields['region_id'].empty_label = 'Choose a region...'
		self.fields['region_id'].widget.attrs['class'] = 'selectpicker'
		self.fields['region_id'].widget.attrs['data-live-search'] = 'true'

class MediaForm(forms.ModelForm):
	class Meta:
		model = media
		fields = ('facebook', 'instagram', 'twitter', 'bandcamp', 'soundcloud', 'tumblr', 'patreon', 'website')

	def __init__(self, *args, **kwargs):
		super(MediaForm, self).__init__(*args, **kwargs)
		for key in self.fields:
			self.fields[key].required = False

class TagsForm(forms.Form):
	tags = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=tag.objects.all(), required=False)

	def __init__(self, *args, **kwargs):
		super(TagsForm, self).__init__(*args, **kwargs)
		self.fields['tags'].widget.attrs['class'] = 'selectpicker'
		self.fields['tags'].widget.attrs['data-live-search'] = 'true'
		self.fields['tags'].widget.attrs['data-actions-box'] = 'true'
		self.fields['tags'].widget.attrs['data-size'] = '10'

class EditForm(forms.ModelForm):
	class Meta:
		model = artist
		fields = ('genre', 'status', 'region_id')

	def __init__(self, *args, **kwargs):
		super(EditForm, self).__init__(*args, **kwargs)
		self.fields['status'].widget.attrs['class'] = 'selectpicker'
		self.fields['region_id'].label = 'Region'
		self.fields['region_id'].empty_label = 'Choose a region...'
		self.fields['region_id'].widget.attrs['class'] = 'selectpicker'
		self.fields['region_id'].widget.attrs['data-live-search'] = 'true'

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

	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)

		for key in self.fields:
			self.fields[key].label = ''

		self.fields['name'].widget.attrs['placeholder'] = 'Enter an artist or band name...'
		
		self.fields['regions'].empty_label = 'Select a region...'
		self.fields['regions'].widget.attrs['class'] = 'selectpicker'
		self.fields['regions'].widget.attrs['data-live-search'] = 'true'
		self.fields['regions'].widget.attrs['data-actions-box'] = 'true'

		self.fields['tags'].empty_label = 'Select tags...'
		self.fields['tags'].widget.attrs['data-live-search'] = 'true'
		self.fields['tags'].widget.attrs['class'] = 'selectpicker'
		self.fields['tags'].widget.attrs['data-actions-box'] = 'true'



	