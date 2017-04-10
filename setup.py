from setuptools import setup

import django_elasticache_pymemcache


setup(
    name='django-elasticache-pymemcache',
    version=django_elasticache.__version__,
    description='Django cache backend for Amazon ElastiCache (memcached)',
    long_description=open('README.rst').read(),
    author='Danil Gusev',
    platforms='any',
    author_email='info@uncovertruth.jp',
    url='http://github.com/uncovertruth/django-elasticache-pymemcache',
    license='MIT',
    keywords='elasticache amazon cache pymemcache memcached aws',
    packages=['django_elasticache'],
    install_requires=['pymemcache', 'Django>=1.7'],
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
