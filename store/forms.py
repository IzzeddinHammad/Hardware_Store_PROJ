from django import forms
from .models import Rating , Review
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '5',
                'step': '1'
            })
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3})
        }