#!/usr/bin/env python

import sys
from setuptools import find_packages


try:
    from notsetuptools import setup
except ImportError:
    from setuptools import setup


tests_require = [
    'Django>=1.1', 'nose', 'exam', 'mock', 'South', 'redis'
]

install_requires = [
    'nexus>=0.2.3', 'chimera-client'
]

setup_requires = []
if 'nosetests' in sys.argv[1:]:
    setup_requires.append('nose')


setup(
    name='chimera-web',
    version='0.1',
    author='DISQUS',
    author_email='opensource@disqus.com',
    url='http://github.com/disqus/chimera-web',
    description = 'Web UI to administer Chimera switches.',
    packages=find_packages(exclude=["example_project", "tests"]),
    zip_safe=False,
    install_requires=install_requires,
    license='Apache License 2.0',
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='nose.collector',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)