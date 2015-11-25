from django import forms


class PlaceholderForm(forms.Form):
    """
    A base form for automatically adding placeholder text.

    Forms that extend this form will by default have all text, password, and
    date input widgets display placeholder text equal to their label. This can
    be overridden per form field by simply specifying a different placeholder
    attribute.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) in (forms.TextInput, forms.PasswordInput, forms.EmailInput, forms.DateInput):
                    field.widget.attrs.update(
                            { 'placeholder': field.widget.attrs.get('placeholder', field.label or field_name) }
                            )

