# -*- encoding: utf-8 -*-
# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import re

from setuptools import find_packages, setup

dev_requirements = [
    'flake8',
    'pytest',
]
unit_test_requirements = [
    'pytest',
    'pandas'
]
integration_test_requirements = [
    'pytest',
    'pandas'
]
run_requirements = [
    'flask==1.1.2',
    'itsdangerous==2.0.1',
    'Flask-Cors==4.0.0',
    'flask-restplus==0.13.0',
    'werkzeug==0.16.1',
    'gunicorn==20.0.4',
    'requests==2.31.0',
    'jinja2==3.0.0',
    'loguru==0.4.1',
    'numpy==1.24.0',
    'prometheus_client==0.8.0',
    'shapely==2.0.3',
    'pyproj==3.4.0',
    'Rtree==1.2.0'
]

with io.open('./service/__init__.py', encoding='utf8') as version_f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="service",
    version=version,
    packages=find_packages(exclude='tests'),
    include_package_data=True,  
    description="Template para API flask arq 3.0",
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
         'dev': dev_requirements,
         'unit': unit_test_requirements,
         'integration': integration_test_requirements,
    },
    python_requires='>=3.8',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11'
    ],
    keywords=(),
    entry_points={
        'console_scripts': [
            'service = service.__main__:app'
        ],
    },
)
