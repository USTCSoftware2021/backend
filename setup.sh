#!/usr/bin/bash
python3 -m venv apienv
if ! [ -e apienv/bin/activate ]; then
	exit 1
fi
source apienv/bin/activate
pip install -U pip
pip install -U setuptools
pip install setuptools_scm
pip install wheel
pip install pybiolib requests requests_toolbelt flask gunicorn jpredapi scikit-learn==0.24.1 redis celery
