
from setuptools import setup, find_packages


setup(
    name='lychee',
    version='0.2.2',

    packages=find_packages(),
    include_package_data=True,

    install_requires=['PyYAML', 'Jinja2', 'markdown'],

    zip_safe=False,

    description="I'm Lychee. A static blog generator.",
    keywords='lychee static blog generator',

    entry_points={
        'console_scripts': [
            'lychee=lychee.management:execute_from_command_line',
        ],
    }
)
