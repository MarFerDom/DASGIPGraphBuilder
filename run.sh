#!/bin/bash

# If not installed
if ! ls ./venv &>/dev/null; then

  # Check if Python is installed
  if command -v python &>/dev/null; then
    echo "Python is already installed."
  else
    echo "Python is not installed, no doughnut for you. You can install it using:"
    echo "brew install python3"
    exit 1
  fi

  # Create a virtual environment
  python -m venv venv

  # Activate the virtual environment
  if ! source venv/bin/activate &>/dev/null; then
    echo "Failed to activate the virtual environment."
    exit 1
  fi

  # Update pip
  echo "updating PIP."
  python -m pip install --upgrade pip

  # Install the requirements
  pip install -r requirements.txt

else

  # Activate the virtual environment
  if ! source venv/bin/activate &>/dev/null; then
    echo "Failed to activate the virtual environment."
    exit 1
  fi

fi


###################################################################################################################
# Run code                                                                                                        #
#                                                                                                                 #
# Change:                                   "./CSV/<FILENAME>.csv"       -s   <VESSEL_NUMBER> -d <VARIABLES_NAMES>#
###################################################################################################################
python -m src.DASGIPGraphBuilder "./CSV/CTPCLI308268.Manager 584248e0.Control.csv" -s 2 -d FAir FA FB FC FD
###################################################################################################################


# Deactivate the virtual environment
deactivate