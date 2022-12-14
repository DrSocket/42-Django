#!/bin/env bash

PYTHON_PATH="/usr/bin/python3"
VENV_DIR="django_venv"
pip3 install virtualenv

# setup venv
$PYTHON_PATH -m virtualenv $VENV_DIR
activate="`pwd`/$VENV_DIR/bin/activate"

if [ ! -f "$activate" ]
then
	echo "ERROR: activate not found at $activate"
	return 1
fi

#activate
source $activate

#install requirement
pip install -r requirement.txt