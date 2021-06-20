from setuptools import setup
setup(
   name='wagtail-ckeditor5',
   version='1.0',
   description='CKEditor 5 widget for Wagtail CMS',
   author='Martin Mastny',
   author_email='martin.mastny@vscht.cz',
   packages=['wagtail_ckeditor5'],
   include_package_data=True,
   install_requires=['wagtail'],
)
