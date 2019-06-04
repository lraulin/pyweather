import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyweather',
    version='0.0.6',
    entry_points={
        'console_scripts': ['pyweather=pyweather.main:main'],
    },
    author="Lee Raulin",
    author_email="leeraulin@gmail.com",
    description="Show current weather from OpenWeather API in console.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lraulin/pyweather",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
