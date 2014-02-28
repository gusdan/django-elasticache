from setuptools import setup

import django_elasticache


setup(
    name='django-elasticache',
    version=django_elasticache.__version__,
    description='Django cache backend for Amazon ElastiCache (memcached)',
    long_description=open('README.rst').read(),
    author='Danil Gusev',
    platforms='any',
    author_email='danil.gusev@gmail.com',
    url='http://github.com/gusdan/django-elasticache',
    license='MIT',
    keywords='elasticache amazon cache pylibmc memcached aws',
    packages=['django_elasticache'],
    install_requires=['pylibmc', 'Django>=1.3'],
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
