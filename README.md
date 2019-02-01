# phone-number-validator

An API on top of libphonenumber to check if a phone number is valid and if so, is it land line or mobile.

## Development

You'll need Python 3.6 installed, even though you'll probably have Python 2.7 or 3.7 installed. You can use [pyenv](https://github.com/pyenv/pyenv) to help you with that.

Once you have Python 3.6 available, you can install dependencies with [pipenv](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today):

```
pipenv sync --dev
```

Then enter the virtual environment that Pipenv created for you:

```
pipenv shell
```

(You'll see your prompt get pre-pended with the virtual environment name)

Then you can try running it locally:

```
FLASK_APP=run.py FLASK_DEBUG=true  flask run
```

and browse to [http://127.0.0.1:5000/v1/numbers/4158675309](http://127.0.0.1:5000/v1/numbers/4158675309) to try the API out.
