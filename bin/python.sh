#!/bin/bash

# Disable core dump (no more core dump files)
ulimit -c 0

ENV_SH=$(dirname $BASH_SOURCE)/env.sh

if ! [ -f ${ENV_SH} ];
then
    echo "Missing env.sh file exiting ..."
    exit 1
fi

. ${ENV_SH}

PYTHON=${VIRTUAL_ENV}/bin/python

echo ${PYTHON}

exec ${PYTHON} "$@"