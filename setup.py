import os

from setuptools import setup, find_packages

requires = [
    'gevent-websocket',
    'picamera',
]

tests_require = [
    'pylint',
    'WebTest >= 1.3.1',  # py3 compat
]

setup(
    name='tarcioscope',
    version='0.0.1',
    description='A simple tool to look at the sky with a PiKon Telescope (a newtonian tube).',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Tarcio Saraiva',
    author_email='tarcio@gmail.com',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = tarcioscope:main',
        ],
    },
)
