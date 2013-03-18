#!/bin/bash

pushd /development/echomesh/code/python/

pylint echomesh \
 --indent-string="  " \
 --include-ids=y \
 --disable=\
C0103,\
C0111,\
C0301,\
F0401,\
I0011,\
R0201,\
R0902,\
R0903,\
R0912,\
R0913,\
R0915,\
W0141,\
W0142,\
W0201,\
W0511,\
W0603,\
W0702,\
W0703,\
W0603\
 | \
 /development/echomesh/code/python/experiments/FixLint.py
