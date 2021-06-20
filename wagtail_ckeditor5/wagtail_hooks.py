from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

try:
    from wagtail.wagtailcore import hooks
    from wagtail.wagtailcore.whitelist import allow_without_attributes, check_url, attribute_rule
except ImportError:
    from wagtail.core import hooks
    from wagtail.core.whitelist import allow_without_attributes, check_url, attribute_rule

from wagtail_ckeditor5 import settings


@hooks.register('insert_editor_js')
def ckeditorjs():
    # js_assets = [
    #     {'link': static("wagtail_ckeditor/ckeditor/ckeditor.js")},
    #     {'link': static("wagtail_ckeditor/ckeditor/adapters/jquery.js")}
    # ]
    # print(format_html_join('\n', '<script src="{}"></script>', (jsa['link'] for jsa in js_assets)))
    # return format_html_join('\n', '<script src="{}"></script>', (jsa['link'] for jsa in js_assets))

    return '\n'.join([
        format_html('<script src="{src}"></script>', src=static("wagtail_ckeditor/ckeditor/ckeditor.js")),
        format_html('<script src="{src}"></script>', src=static("wagtail_ckeditor/ckeditor/adapters/jquery.js"))
    ])
    # return format_html('<script src="{src}"></script>', src=static("wagtail_ckeditor/ckeditor/ckeditor.js"))


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        's': allow_without_attributes,
        'u': allow_without_attributes,
        'span': attribute_rule({'style': True, "class": True}),
        'p': attribute_rule({'style': True, "class": True}),
        'div': attribute_rule({'style': True, "class": True}),
        'q': allow_without_attributes,
        'ins': allow_without_attributes,
        'pre': allow_without_attributes,
        'address': allow_without_attributes,
        'table': attribute_rule({'align': True, "border": True, "cellpadding": True, "style": True}),
        'caption': allow_without_attributes,
        'thead': allow_without_attributes,
        'tr': allow_without_attributes,
        'tbody': allow_without_attributes,
        'td': attribute_rule({'style': True, "class": True}),
        'hr': allow_without_attributes,
        'img': attribute_rule({'alt': True, "src": True, 'style':True, 'width': True, 'height': True}),
    }
