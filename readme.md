Wagtail CKEditor plugin
======

This is a [Wagtail](https://wagtail.io/) plugin, which allows [CKEditor](http://ckeditor.com/) to be used as an internal editor
instead of hallo.js.

How to install
----

Since the original owner of this project is [not willing add to PYPI](https://github.com/mastnym/wagtail-ckeditor/issues/1), so we can't install it as usual. But we can install it directly from github (this repo). 

```
pip install git+git://github.com/tegarimansyah/wagtail-ckeditor5.git
```

Include `wagtail_ckeditor5` in your `INSTALLED_APPS`.

Ensure that you have this entry in your `settings.py` file.


```python
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail_ckeditor5.widgets.CKEditor'
    }
}
```

There are several options you can add to your `settings.py` file.

- Use Mathjax plugin to be able to insert mathematical formulas

```python
WAGTAIL_CKEDITOR_USE_MATH = True
```

- If above set to true you need to specify an url to Mathjax Library, defaults to:

```python
WAGTAIL_CKEDITOR_MATHJAX_URL = getattr(settings, 'WAGTAIL_CKEDITOR_MATHJAX_URL', "//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_HTML")
```

- CKEditor settings, defaults to:

```python        
WAGTAIL_CKEDITOR_CONFIG = getattr(settings, 'WAGTAIL_CKEDITOR_CONFIG',
            {
                'language': settings.LANGUAGE_CODE,
            'toolbar': [
                {
                    'name': 'basicstyles',
                    'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript']
                },
                {
                    'name': 'clipboard',
                    'items': [
                        'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'
                    ]
                },
                {
                    'name': 'paragraph',
                    'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                            'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
                {
                    'name': 'links', 
                    'items': ['Link', 'Unlink', 'Anchor']
                },
                '/',
                {
                    'name': 'styles', 
                    'items': ['Styles', 'Format', 'Font', 'FontSize']
                },
                {
                    'name': 'insert',
                    'items': [
                        'Image', 'Mathjax' if WAGTAIL_CKEDITOR_USE_MATH else '-', 'Table', 'HorizontalRule', 'SpecialChar'
                    ]
                },
                {
                    'name': 'colors', 'items': ['TextColor', 'BGColor']
                },
                {
                    'name': 'document', 'items': ['Maximize', '-', 'Source']
                },
            ]
            }
        )
```

Inspired by:
---
Richard Mitchell (https://github.com/isotoma/wagtailtinymce.git)