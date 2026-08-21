from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': 'Topic'}
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'e.g. Spanish, Chess, Rock climbing'}),
        }


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry'}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': "What did you learn?",
            }),
        }
