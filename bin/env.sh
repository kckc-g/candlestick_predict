#!/bin/bash

PROJECT_DIR=$(realpath $(dirname $BASH_SOURCE)/..)

# Location of venv directory
VENV_DIR=${PROJECT_DIR}/.venv

# Run bootstrap.py to create the virtualenv environment
if ! [ -d "${VENV_DIR}" ]; then
    echo "No venv directory found, please run bootstrap.py to create the venv environment, exiting..."
    exit 1
fi

# Activate virtualenv if not already
if [ -z "${VIRTUAL_ENV}" ];
then
    echo "No active virtualenv found, activating from: '${VENV_DIR}'"
    . ${VENV_DIR}/bin/activate
fi

# Include src dir as well
export PYTHONPATH=${PROJECT_DIR}/src