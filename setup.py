from setuptools import setup

import django_elastipymemcache


setup(
    name='django-elastipymemcache',
    version=django_elastipymemcache.__version__,
    description='Django cache backend for Amazon ElastiCache (memcached)',
    long_description=open('README.md').read(),
    author='Danil Gusev',
    platforms='any',
    author_email='info@uncovertruth.jp',
    url='http://github.com/uncovertruth/django-elastipymemcache',
    license='MIT',
    keywords='elasticache amazon cache pymemcache memcached aws',
    packages=['django_elastipymemcache'],
    install_requires=['pymemcache', 'Django>=1.8'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
