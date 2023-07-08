#!/bin/bash

# If not installed
if ! ls ./venv &>/dev/null; then

  # Check if Python is installed
  if command -v python3 &>/dev/null; then
    echo "Python is already installed."
  else
    echo "Python is not installed, no doughnut for you. You can install it using:"
    echo "brew install python3"
    exit 1
  fi
  
  # Check if virtualenv is installed
  if command -v virtualenv &>/dev/null; then
    echo "virtualenv is already installed."
  else
    pip3 install -U virtualenv
  fi

  # Create a virtual environment
  virtualenv venv

  # Activate the virtual environment
  if ! source venv/bin/activate &>/dev/null; then
    echo "Failed to activate the virtual environment."
    exit 1
  fi

  # Update pip
  echo "updating PIP."
  python3 -m pip install --upgrade pip

  # Install the requirements
  pip3 install -r requirements.txt

else

  # Activate the virtual environment
  if ! source venv/bin/activate &>/dev/null; then
    echo "Failed to activate the virtual environment."
    exit 1
  fi

fi

python3 -m src.app

open "http://localhost:5000/"

###################################################################################################################
# Run code                          ### !!! NO LONGER IN USE !!!! ###                                                                                         #
#                                                                                                                 #
# Change:                                   "./CSV/<FILENAME>.csv"       -s   <VESSEL_NUMBER> -d <VARIABLES_NAMES>#
###################################################################################################################
#python -m src.DASGIPGraphBuilder "./CSV/CTPCLI308268.Manager 584248e0.Control.csv" -s 2 -d FAir FA FB FC FD
###################################################################################################################


# Deactivate the virtual environment
deactivate