from setuptools import setup

import django_elastipymemcache


setup(
    name='django-elastipymemcache',
    version=django_elastipymemcache.__version__,
    url='http://github.com/uncovertruth/django-elastipymemcache',
    author='UNCOVER TRUTH Inc.',
    author_email='dev@uncovertruth.co.jp',
    description='Django cache backend for Amazon ElastiCache (memcached)',
    long_description=open('README.md').read(),
    keywords='elasticache amazon cache pymemcache memcached aws',
    license='MIT',
    packages=[
        'django_elastipymemcache',
    ],
    install_requires=[
        'pymemcache',
        'Django>=1.8',
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['nose', 'coverage', 'flake8', 'isort', 'readme_renderer'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
