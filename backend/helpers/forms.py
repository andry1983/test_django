from django import forms

DEFAULT_VISIBLE_WIDGETS = (
    forms.TextInput,
    forms.Textarea,
    forms.Select,
    forms.FileInput
)

WIDGET_TYPES = (
    forms.TextInput,
    forms.Textarea,
    forms.Select,
    forms.FileInput,
    forms.EmailInput,
    forms.PasswordInput
)

ERROR_CSS_CLASS = 'is-invalid'


def add_css_class_to_field(form_field, css_class):
    attrs = form_field.widget.attrs
    if 'class' in attrs:
        if attrs['class']:
            attrs['class'] += ' '
    else:
        attrs['class'] = ''
    attrs['class'] += css_class


def set_default_placeholder(form_fields):
    for field in form_fields:
        form_fields[field].widget.attrs['placeholder'] = form_fields[
            field].label


def add_css_class_to_fields_widget(form_fields, css_class,
                                   widget_types=DEFAULT_VISIBLE_WIDGETS):
    for k in form_fields:
        if isinstance(form_fields[k].widget, widget_types):
            add_css_class_to_field(form_fields[k], css_class)


def add_error_css_class_to_form_fields_widget(form, css_class=ERROR_CSS_CLASS,
                                              widget_types=WIDGET_TYPES):
    for k in form.fields:
        if k in form.errors and isinstance(form.fields[k].widget,
                                           widget_types):
            add_css_class_to_field(form.fields[k], css_class)
