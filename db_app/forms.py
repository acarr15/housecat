from django import forms
from .models import artist, media, tag, region, status

class ArtistForm(forms.ModelForm):
	class Meta:
		model = artist
		fields = ('name', 'genre', 'region_id', 'hometown', 'email', 'status')

	def __init__(self, *args, **kwargs):
		super(ArtistForm, self).__init__(*args, **kwargs)
		self.fields['region_id'].label = 'Region'
		self.fields['region_id'].empty_label = 'Select a region...'
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
		self.fields['tags'].widget.attrs['title'] = 'Select tag(s)...'
		self.fields['tags'].widget.attrs['class'] = 'selectpicker'
		self.fields['tags'].widget.attrs['data-live-search'] = 'true'
		self.fields['tags'].widget.attrs['data-actions-box'] = 'true'
		self.fields['tags'].widget.attrs['data-size'] = '10'


class TagForm(forms.ModelForm):
	class Meta:
		model = tag
		fields = ('tag', )

class RegionForm(forms.ModelForm):
	class Meta:
		model = region
		fields = ('region', )

class SearchForm(forms.Form):
	name = forms.CharField(required=False)
	regions = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=region.objects.all(), required=False)
	tags = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=tag.objects.all(), required=False)

	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)

		for key in self.fields:
			self.fields[key].label = ''
			if key is not 'name':
				self.fields[key].widget.attrs['data-live-search'] = 'true'
				self.fields[key].widget.attrs['data-actions-box'] = 'true'
				self.fields[key].widget.attrs['class'] = 'selectpicker'

		self.fields['name'].widget.attrs['placeholder'] = 'Search by name...'
		self.fields['regions'].widget.attrs['title'] = 'Select region(s)...'
		self.fields['tags'].widget.attrs['title'] = 'Select tag(s)...'

	