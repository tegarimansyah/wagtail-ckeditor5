from __future__ import absolute_import, unicode_literals

import json

from django.forms import widgets
from django.utils.safestring import mark_safe
from wagtail.utils.widgets import WidgetWithScript

try:
    from wagtail.wagtailadmin.edit_handlers import RichTextFieldPanel
    from wagtail.wagtailcore.rich_text import DbWhitelister
    from wagtail.wagtailcore.rich_text import expand_db_html

    wagtail_version = 1

except ImportError:
    from wagtail.admin.edit_handlers import RichTextFieldPanel
    from wagtail.admin.rich_text.converters.editor_html import EditorHTMLConverter
    from wagtail.core.rich_text import expand_db_html
    from wagtail.core.rich_text import features

    wagtail_version = 2

from wagtail_ckeditor import settings


class CKEditor(WidgetWithScript, widgets.Textarea):

    def __init__(self, *args, **kwargs):
        if wagtail_version == 2:
            self.features = features.get_default_features()
            self.converter = EditorHTMLConverter(self.features)

        super().__init__(*args, **kwargs)

    def get_panel(self):
        return RichTextFieldPanel

    def render(self, name, value, *args, **kwargs):
        if value is None:
            translated_value = None
        elif wagtail_version == 2:
            translated_value = expand_db_html(value)
        else:
            translated_value = expand_db_html(value, for_editor=True)
        return super().render(name, translated_value, *args, **kwargs)

    def render_js_init(self, editor_id, name, value):

        return "CKEDITOR.replace( '%s', %s);" % (editor_id, mark_safe(json.dumps(settings.WAGTAIL_CKEDITOR_CONFIG)))

    def value_from_datadict(self, data, files, name):
        original_value = super().value_from_datadict(data, files, name)
        if original_value is None:
            return None
        if wagtail_version == 2:
            return self.converter.to_database_format(original_value)
        else:
            return DbWhitelister.clean(original_value)
