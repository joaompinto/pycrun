# pycrun

Container Runtime Written in Python

[![PyPi](https://img.shields.io/pypi/v/pycrun.svg?style=flat-square)](https://pypi.python.org/pypi/pycrun)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

pycrun allows running Linux distributions in a containerized environment, providing an isolated and controlled environment for their execution.

It is written purely in Python and does not require the installation of other engines such as Docker or Containerd.


# System Requirements
- Linux or Windows with WSL
- Python 3.10+

# Using the source from this repo
```bash
# Create a virtual environment for pycrun 
python3 -m venv $HOME/pycrun_venv
sudo $HOME/pycrun_venv/bin/python -m \
    pip install -r requirements.txt
```

## Examples

Run `sh` using an alpine root filesystem archive .
```bash
# The rfs: stands for root file system archive
# Currently supported: Alpine, Ubuntu
sudo $HOME/pycrun_venv/bin/python -m pycrun run alpine
```

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the [GitHub
Issue
Tracker](https://github.com/joaompinto/pycrun/issues).
Pull requests are welcome. Issues that don't have an accompanying pull
request will be worked on as my time and priority allows.

