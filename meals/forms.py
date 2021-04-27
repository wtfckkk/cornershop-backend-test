from datetime import datetime

from django import forms
from django.forms import ModelMultipleChoiceField, DateField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from rest_framework.exceptions import ValidationError

from .models import Menu, Meal


class MenuForm(forms.ModelForm):
    country = CountryField().formfield(
        widget=CountrySelectWidget(
            attrs={"class": "my-class"}
        )
    )
    meals = ModelMultipleChoiceField(queryset=Meal.objects.all())
    date = DateField(widget=forms.SelectDateWidget(), initial=datetime.today())

    class Meta:
        model = Menu
        fields = ("state", "date", "country", "meals")

    def clean(self):
        menu = Menu.objects.filter(date=self.cleaned_data['date'],
                                   state=Menu.STATE_OPEN,
                                   country=self.cleaned_data['country'])
        if self.cleaned_data['state'] == Menu.STATE_OPEN and menu:
            self._update_errors([f"Already exists a open menu for today in {self.cleaned_data['country']}"])
        super().clean()


class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = "__all__"
