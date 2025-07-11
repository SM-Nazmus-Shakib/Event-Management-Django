from django import forms
from .models import Event, Category
from django.contrib.auth.models import User

class EventModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['time'].required = False
        self.fields['participants'].queryset = User.objects.all()
        if not self.request.user.is_superuser:
            self.fields['participants'].queryset = User.objects.filter(
                groups__name__in=['Event Managers', 'Staff']
            )

    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'description', 'location', 'category', 'participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'participants': forms.CheckboxSelectMultiple(),
        }