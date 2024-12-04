import os

from setuptools import setup  # type: ignore[import-untyped]

if True:  # TODO: tox's pass_env is not working for unknown reason
# if os.environ.get("MARKDOWNIT_USE_MYPYC") == "1":
    import glob
    from mypyc.build import mypycify  # type: ignore[import-untyped]
    files = glob.glob("markdown_it/**/*.py", recursive=True)
    ext_modules = mypycify(files)
else:
    ext_modules = []

setup(ext_modules=ext_modules)
