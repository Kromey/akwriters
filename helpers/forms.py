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


class PlaceholderFormMixin(object):
    """
    A form mixin for automatically adding placeholder text.

    Forms that use this mixin will by default have all text, password, and
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


_bootstrap_formgroup = """
<div class="form-group %(css_classes)s">
	<div class="input-group">
		%(label)s
		%(field)s%(help_text)s
	</div>
</div>
"""

class BootstrapFormMixin(object):
    """
    A form mixin to generate Bootstrap form-groups
    """
    def as_formgroup(self):
        "Returns this form rendered as Bootstrap form-groups."
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update(
                        { 'class': field.widget.attrs.get('class', '') + ' form-control' }
                        )
                bf = self[field_name]
                bf.label_tag = self.style_label_tag(bf.label_tag)

        return self._html_output(
            normal_row=_bootstrap_formgroup,
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)

    def style_label_tag(self, label_tag):
        def inner(contents=None, attrs=None, label_suffix=None):
            attrs = attrs or {}
            if 'class' in attrs:
                attrs['class'] += ' input-group-addon'
            else:
                attrs['class'] = 'input-group-addon'
            return label_tag(contents, attrs, label_suffix)
        return inner

