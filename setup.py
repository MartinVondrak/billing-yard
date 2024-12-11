from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='billingyard',
    version='1.2.0',
    author='Martin Vondrák',
    author_email='martin@martinvondrak.cz',
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
        'Development Status :: 5 - Production/Stable',
    ],
    packages=find_packages(),
    package_data={'billingyard': ['templates/*.html']},
    python_requires='>=3.9',
    install_requires=[
        'Click>=8.1.7,<9',
        'Jinja2>=3.1.4,<4',
        'WeasyPrint>=63.1,<64',
        'qrcode>=8.0,<9',
    ],
    entry_points={
        'console_scripts': [
            'billingyard = billingyard.__main__:main',
        ],
    },
    zip_safe=False,
)
