
## Setup

I've used a virtual env under the directory env.

In order to create this virtual environment enter:

`virtualenv env`

Then to activate the env before running Django enter:

`source ./env/bin/activate`

You should see (env) $ at your prompt, letting you know that you're running under the 'env' virtualenv install.

You can then install all of the environment requirements by running:

`pip install -r requirements.txt`

To deactivate the env run:

`deactivate`

## Running the Queue

Start the developement server by running: `python main.py`

## Running the Tests

Start the developement server by running: `python tests.py`
