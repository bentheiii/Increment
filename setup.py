import setuptools

import increment

setuptools.setup(
    name=increment.__name__,
    version=increment.__version__,
    author=increment.__author__,
    packages=['increment'],
    install_requires=['PySide2'],
    python_requires='>=3.7.0',
    include_package_data=True,
    data_files=[
        ('increment', ['increment/resources/favicon.ico']),
    ],
)
