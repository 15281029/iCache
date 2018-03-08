import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='iCache',
    version='1.0.2',
    description='A Python Cache Model',
    url='https://github.com/15281029/iCache',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    author='Zhangbo',
    author_email='15281029@bjtu.edu.cn',
    py_modules=['iCache'],
    license='MIT',
    include_package_data=True,
    zip_safe=True,
)
