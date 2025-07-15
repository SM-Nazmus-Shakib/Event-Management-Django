from django import forms
from .models import Event, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class StyledFormMixin:
    """Mixin to apply consistent styling to form fields"""
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 4
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'type': 'date'
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'type': 'time'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })

class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'description', 'location', 'category', 'participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].required = False
        if self.instance.pk and not self.request.user.has_perm('events.can_manage_events'):
            self.fields['participants'].queryset = self.fields['participants'].queryset.filter(
                user=self.request.user
            )

    def save(self, commit=True):
        event = super().save(commit=False)
        if not event.pk or not event.created_by:
            event.created_by = self.request.user
        if commit:
            event.save()
            self.save_m2m()
        return event