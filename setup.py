import io
import os
import re
import sys

from Cython.Build import cythonize
from setuptools import Extension
from setuptools import find_packages
from setuptools import setup

_dev_build = "--inplace" in sys.argv
_ci_build = "egg_info" in sys.argv or "install" in sys.argv
_define_macros = []
_extra_cargs = []


if int(os.getenv("FOR_PRODUCTION", "0")) == 1:
    _dev_build = False
    _ci_build = False
    _extra_cargs.append("-O2")
else:
    _extra_cargs.append("-O0")
    _define_macros += [
        ("CYTHON_PROFILE", 1),
        ("CYTHON_TRACE", 1),
        ("CYTHON_TRACE_NOGIL", 1),
    ]


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ).read()


ext_modules = [
    Extension(
        "xrtr",
        sources=["src/xrtr.{}".format("c" if _ci_build else "pyx")],
        extra_compile_args=_extra_cargs,
        define_macros=_define_macros,
    )
]

setup(
    name="xrtr",
    version="0.1.0",
    description="A Radix Tree based router for HTTP and other routing needs "
    "with support for middlewares and endpoints with a Cython "
    "boost",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Richard Kuesters",
    author_email="rkuesters@gmail.com",
    url="https://github.com/vltr/xrtr",
    setup_requires=["Cython"],
    install_requires=["setuptools>=19.0"],
    ext_modules=cythonize(
        ext_modules,
        compiler_directives={
            "optimize.use_switch": False,
            "optimize.unpack_method_calls": False,
            "language_level": 3,
            "c_string_type": "bytes",
            "c_string_encoding": "ascii",
            "boundscheck": False,
            "wraparound": False,
            "embedsignature": _dev_build,
            "linetrace": _dev_build,
            "profile": _dev_build,
            "binding": _dev_build,
        },
    ),
    package_data={
        "xrtr": [
            "src/xrtr.pyx",
            "src/xrtr.c",
            "src/__init__.py",
            "src/__init__.pxd",
        ]
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False,
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: Cython",
        # 'Programming Language :: Python :: Implementation :: PyPy',
        "Topic :: Utilities",
    ],
    keywords=[
        "router",
        "radix",
        "tree",
        "cython",
        "trie",
        "middleware",
        "endpoint",
    ],
)
