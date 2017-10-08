from django.forms import ModelForm,Textarea


from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('subject','body')
        widgets = {
                'body': Textarea(
                    attrs={
                        'data-provide':'markdown',
                        'data-hidden-buttons':'cmdHeading',
                        }),
                }

