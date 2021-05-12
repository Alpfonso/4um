from django import forms

from .models import Thread, Thread_Comment



class ForumForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = [
            'title',
            'description',
            'live_thread',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class':"form-control",
            }),
            'description': forms.Textarea(attrs={
                'class':"form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ForumForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(ForumForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst

class CommentForm(forms.ModelForm):
    class Meta:
        model = Thread_Comment
        fields = [
            'comment_content',
        ]

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self.parent_thread = kwargs.pop('parent')
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(CommentForm, self).save(commit=False)
        inst.user = self._user
        inst.parent_thread = self.parent_thread
        if commit:
            inst.save()
            self.save_m2m()
        return inst