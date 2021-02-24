from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='billingyard',
    version='1.0.0',
    author='Martin Vondrák',
    author_email='martinvondrak@icloud.com',
    description='CLI invoice generator for business entities in the Czech republic',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MartinVondrak/billing-yard',
    keywords='invoice,cli,generator',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Czech',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
    packages=find_packages(),
    package_data={'billingyard': ['templates/*.html']},
    install_requires=[
        'Click>=7.1.2,<8',
        'Jinja2>=2.11.3,<3',
        'WeasyPrint>=52.2,<53'
    ],
    entry_points={
        'console_scripts': [
            'billingyard = billingyard.__main__:main',
        ],
    },
    zip_safe=False,
)
