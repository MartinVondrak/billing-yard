from setuptools import setup, find_packages

setup(
    name='billingyard',
    version='0.1.2',
    packages=find_packages(),
    package_data={'billingyard': ['templates/*.html']},
    install_requires=[
        'Click',
        'Jinja2',
        'WeasyPrint'
    ],
    entry_points={
        'console_scripts': [
            'billingyard = billingyard.__main__:main',
        ],
    },
)
