from setuptools import Extension, setup

ext = Extension(
    name='webgl2',
    sources=['./webgl2.c'],
)

setup(
    name='webgl2',
    version='0.2.0',
    py_modules=['_webgl2'],
    ext_modules=[ext],
)
