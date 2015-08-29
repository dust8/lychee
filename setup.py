
from setuptools import setup, find_packages


setup(
    name='lychee',
    version='0.1.6',

    packages=find_packages(),
    include_package_data=True,

    install_requires = ['PyYAML', 'Jinja2', 'markdown'],
    
    zip_safe=False,

    # metadata for upload to PyPI
    author='dust8',
    author_email='adbcdust@gmail.com',
    description="I'm Lychee. A static blog generator.",
    keywords='lychee static blog generator',
    
    # could also include long_description, download_url, classifiers, etc.
    entry_points={
        'console_scripts': [
            'lychee=lychee.management:execute_from_command_line',
        ],
    }
    )