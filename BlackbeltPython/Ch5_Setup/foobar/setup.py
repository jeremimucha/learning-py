from setuptools import setup

setup(
    name='foobar',
    version='0.1.0',
    description='Foo!',
    author='jamcodes',
    author_email='jam@codes.com',
    packages=['foobar'],
    entry_points={
        "console_scripts":[
            "foobard = foobar.server:main",
            "foobar = foobar.client:main",
        ],
    },
)