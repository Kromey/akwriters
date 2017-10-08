from django.forms import ModelForm,Textarea,TextInput


from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('subject','body')
        widgets = {
                'subject': TextInput(attrs={'autofocus':'autofocus'}),
                'body': Textarea(
                    attrs={
                        'data-provide':'markdown',
                        'data-hidden-buttons':'cmdHeading',
                        }),
                }

