#!/usr/bin/bash
python -m venv apienv
source apienv/bin/activate
pip install -U pip
pip install -U setuptools
pip install setuptools_scm
pip install wheel
pip install pybiolib requests requests_toolbelt flask gunicorn
