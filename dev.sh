#!/bin/sh

set -e
export FOLDER_VENV=".venv"
# set -x

echo "Creating dev environment in ./${FOLDER_VENV}..."

python3 -m venv $FOLDER_VENV
. ${FOLDER_VENV}/bin/activate
pip3 install pip setuptools
pip3 install -e .

echo ""
echo "  * Created virtualenv environment in ./${FOLDER_VENV}."
echo "  * Installed all dependencies into the virtualenv."
echo "  * You can now activate the $(python3 --version) virtualenv with this command: \`. ${FOLDER_VENV}/bin/activate\`"