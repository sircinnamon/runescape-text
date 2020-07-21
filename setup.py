import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="runescape-text",
	version="1.1.0",
	author="Riley Lahd",
	author_email="sircinnamon@gmail.com",
	description="A program for generating runescape-chat-like images of text.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/sircinnamon/runescape-text",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
    install_requires=[
        "pillow",
    ],
    package_data={"":["data/runescape_uf.ttf"]},
)