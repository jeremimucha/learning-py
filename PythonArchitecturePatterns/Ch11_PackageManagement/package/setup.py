import setuptools

with open("README.md") as readme:
    description = readme.read()


setuptools.setup(
    name='wheel-package',
    version='0.1.0',
    author='jam',
    author_email='jam@jam.com',
    description='an example of a package',
    url="http://site.com",
    long_description=description,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={'': 'src'},
    install_requires=[
        'requests',
    ],
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.9'
)

# Run `python setup.py check` to verify that the setup script is correct.
