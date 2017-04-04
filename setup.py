# -*- coding: utf-8 -*-
"""Installer for the claytonc.govtiles package."""

from setuptools import find_packages
from setuptools import setup

description = 'Tiles para Portal Padrão'
long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='claytonc.govtiles',
    version='1.0a1',
    description=description,
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Clayton Caetano de Sousa',
    author_email='claytonc.sousa@gmail.com',
    url='https://pypi.python.org/pypi/claytonc.govtiles',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['claytonc'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api > 1.1.0',
        'Products.GenericSetup>=1.8.2',
        'setuptools',
        'z3c.jbot',
        'brasil.gov.portal',
        'collective.cover > 1.0a8',
    ],
    extras_require={
        'test': [
            'brasil.gov.portal',
            'collective.cover',
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.registry',
            'plone.testing',
            'plonetheme.sunburst',
            'Products.GenericSetup',
            'robotframework-wavelibrary',
            'robotsuite',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
