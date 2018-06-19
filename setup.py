#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io

from setuptools import find_packages, setup

import django_elastipymemcache

setup(
    name='django-elastipymemcache',
    version=django_elastipymemcache.__version__,
    description='Django cache backend for Amazon ElastiCache (memcached)',
    keywords='elasticache amazon cache pymemcache memcached aws',
    author='UNCOVER TRUTH Inc.',
    author_email='develop@uncovertruth.co.jp',
    url='http://github.com/uncovertruth/django-elastipymemcache',
    license='MIT',
    long_description=io.open('README.rst').read(),
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=[
        'pymemcache',
        'Django>=1.11',
    ],
)
