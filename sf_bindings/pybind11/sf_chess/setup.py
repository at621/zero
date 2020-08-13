import os, sys

from distutils.core import setup, Extension
from distutils import sysconfig

sf_module = Extension(
    'sf_chess',
     sources = ['sf_chess.cpp'],
    include_dirs=['c:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\\Python37_86\\include', '.'],
    extra_objects=[
        '.\\Release\\benchmark',
        '.\\Release\\bitbase',
        '.\\Release\\bitboard',
        '.\\Release\\endgame',
        '.\\Release\\evaluate',
        '.\\Release\\main',
        '.\\Release\\material',
        '.\\Release\\misc',
        '.\\Release\\movegen',
        '.\\Release\\movepick',
        '.\\Release\\pawns',
        '.\\Release\\position',
        '.\\Release\\psqt',
        '.\\Release\\search',
        '.\\Release\\tbprobe',
        '.\\Release\\thread',
        '.\\Release\\timeman',
        '.\\Release\\tt',
        '.\\Release\\tune',
        '.\\Release\\uci',
        '.\\Release\\ucioption',
    ],
    language='c++',
    )

setup(
    name = 'sf_chess',
    version = '1.0',
    description = 'Python package with sf_chess C++ extension (PyBind11)',
    ext_modules = [sf_module],
)