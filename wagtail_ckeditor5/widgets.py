from __future__ import absolute_import, unicode_literals
from django.utils.functional import cached_property

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
    from wagtail.admin.rich_text.converters.editor_html import EditorHTMLConverter as EditorHTMLConverterToDecorate, \
        DbWhitelister as DbWhitelisterToDecorate
    from wagtail.core.rich_text import expand_db_html
    from wagtail.core.rich_text import features
    from wagtail.core.whitelist import DEFAULT_ELEMENT_RULES, attribute_rule, check_url

    wagtail_version = 2

from wagtail_ckeditor5 import settings


# class BaseClass(object):
#     def __init__(self, classtype):
#         self._type = classtype


def allow_all_attributes(tag):
    pass


def ext_obj(obj, *args):
    _obj = obj.copy()
    for eobj in args:
        _obj.update(eobj)
    return _obj


ext_attributes = {'class': True, 'id': True, 'style': True}
allow_ext_attributes = attribute_rule(allowed_attrs=ext_attributes)
CUSTOM_DEFAULT_ELEMENT_RULES = {
    'a': attribute_rule(allowed_attrs=ext_obj(ext_attributes, {'href': check_url, 'target': True})),
    'img': attribute_rule(allowed_attrs=ext_obj(ext_attributes, {'src': check_url, 'width': True, 'height': True, 'alt': True})),
    'table': allow_ext_attributes,
    'tbody': allow_ext_attributes,
    'thead': allow_ext_attributes,
    'tr': allow_ext_attributes,
    'th': allow_ext_attributes,
    'td': allow_ext_attributes,
    'span': allow_ext_attributes,
    'u': allow_ext_attributes,
}

for t, a in list(DEFAULT_ELEMENT_RULES.items()):
    if not CUSTOM_DEFAULT_ELEMENT_RULES.get(t):
        if t == 'div':
            CUSTOM_DEFAULT_ELEMENT_RULES[t] = allow_all_attributes
        else:
            CUSTOM_DEFAULT_ELEMENT_RULES[t] = allow_ext_attributes


def c_clean_tag_node(self, doc, tag):
    if 'data-embedtype' in tag.attrs:
        embed_type = tag['data-embedtype']
        # fetch the appropriate embed handler for this embedtype
        try:
            embed_handler = self.embed_handlers[embed_type]
        except KeyError:
            # discard embeds with unrecognised embedtypes
            tag.decompose()
            return

        embed_attrs = embed_handler.get_db_attributes(tag)
        embed_attrs['embedtype'] = embed_type

        embed_tag = doc.new_tag('embed', **embed_attrs)
        embed_tag.can_be_empty_element = True
        tag.replace_with(embed_tag)
    elif tag.name == 'a' and 'data-linktype' in tag.attrs:
        # first, whitelist the contents of this tag
        for child in tag.contents:
            self.clean_node(doc, child)

        link_type = tag['data-linktype']
        try:
            link_handler = self.link_handlers[link_type]
        except KeyError:
            # discard links with unrecognised linktypes
            tag.unwrap()
            return

        link_attrs = link_handler.get_db_attributes(tag)
        link_attrs['linktype'] = link_type
        tag.attrs.clear()
        tag.attrs.update(**link_attrs)
    else:
        # self.element_rules = CUSTOM_DEFAULT_ELEMENT_RULES.copy()
        setattr(self, "element_rules", CUSTOM_DEFAULT_ELEMENT_RULES.copy())
        super(CustomDbWhitelister, self).clean_tag_node(doc, tag)


def c_whitelister(self):
    db_wl = CustomDbWhitelister(self.converter_rules)
    # db_wl.element_rules = CUSTOM_DEFAULT_ELEMENT_RULES.copy()
    setattr(db_wl, "element_rules", CUSTOM_DEFAULT_ELEMENT_RULES.copy())
    return db_wl


if wagtail_version == 2:
    CustomDbWhitelister = type('CustomDbWhitelister',
                               (DbWhitelisterToDecorate,),
                               {'clean_tag_node': c_clean_tag_node})
    globals()['CustomDbWhitelister'] = CustomDbWhitelister
    CustomEditorHTMLConverter = type('CustomEditorHTMLConverter',
                                     (EditorHTMLConverterToDecorate,),
                                     {
                                         'whitelister': cached_property(c_whitelister)
                                     })
    globals()['CustomEditorHTMLConverter'] = CustomEditorHTMLConverter


class CKEditor(WidgetWithScript, widgets.Textarea):

    def __init__(self, *args, **kwargs):
        if wagtail_version == 2:
            self.features = features.get_default_features()
            self.converter = CustomEditorHTMLConverter(self.features)
            # self.converter.converter_rules = DEFAULT_ELEMENT_RULES

        super().__init__(*args, **kwargs)

    def get_panel(self):
        return RichTextFieldPanel

    # def format_value(self, value):
    #     # Convert database rich text representation to the format required by
    #     # the input field
    #     value = super().format_value(value)
    #
    #     if value is None:
    #         return None
    #
    #     return self.converter.from_database_format(value)

    def render(self, name, value, *args, **kwargs):
        if value is None:
            translated_value = None
        elif wagtail_version == 2:
            translated_value = self.converter.from_database_format(value)
        else:
            translated_value = expand_db_html(value, for_editor=True)
        return super().render(name, translated_value, *args, **kwargs)

    def render_js_init(self, editor_id, name, value):

        return "CKEDITOR.replace( '%s', %s);" % (editor_id, mark_safe(json.dumps(settings.WAGTAIL_CKEDITOR_CONFIG)))

    def value_from_datadict(self, data, files, name):
        original_value = super().value_from_datadict(data, files, name)
        # print("\n ------=========----- \n")
        if original_value is None:
            return None
        if wagtail_version == 2:
            return self.converter.to_database_format(original_value)
        else:
            return DbWhitelister.clean(original_value)
