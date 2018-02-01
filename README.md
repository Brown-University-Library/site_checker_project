[![BUL Code Best-Practices](https://library.brown.edu/good_code/project_image/site-checker/)](https://library.brown.edu/good_code/project_info/site-checker/)

##### Overview

On this page...
- Info
- Installation
- Usage
- Other

---


##### Info

This is a [django](https://www.djangoproject.com) webapp that offers a publicly-viewable webpage of the current status of the [Brown University Library's](https://library.brown.edu) checked-services, and an admin interface to add a service to be checked.

The admin-view allows you to set up:
- a url to be checked
- some expected-html
- a check-frequency
- email-addresses that should be notified
- optional additional email text

A separate cron-triggered script determines what sites need to be checked, and checks them.

A nice feature of the system...

If a failure is detected, the check frequency will reset to check again a couple minutes later (regardless of the normal user-specified check-frequency). And if a _second_ failure then occurs (right after the first), _then_ a failure-notification email goes out, and the checks continue for that site every couple of minutes until it's back up (only that single initial 'failure' email goes out).

An email doesn't go out on that first failure in case it's just some weird temporary blip. And once the site is back up, a 'back-up' email goes out, and the check-frequency returns to the normal user-specified frequency.

---


##### Installation

- create a 'site_checker_stuff' directory, and cd into it

- in that create a virtual environment

        $ /path/to/python3 -m venv ./env_chkr

- git clone this project

        $ git clone https://github.com/birkin/site_checker_project.git ./site_checker_project

- cd into the project

        $ cd ./site_checker_project

- activate the virtual environment and load it up

        $ source ../env_chkr/bin/activate
        $ (env_chkr) pip install -r ./config/requirements.txt

- create a `sitechecker_env_settings.sh` file somewhere where it will not get accidentally checked-in to version-control

- at the bottom of the `env_chkr/bin/activate` file, add

        export SITECHKR__SETTINGS_PATH="/path/to/sitechecker_env_settings.sh"
        source $SITECHKR__SETTINGS_PATH

- begin running `python3 ./manage.py check`; the errors will tell you what you need to add to the sitechecker_env_settings.sh file
    - add those settings to the sitechecker_env_settings.sh file in the form of:

            export SITECHKR__KEY="value"

    - note that each time you add an entry to the `sitechecker_env_settings.sh` file, you'll need to source the virtual environment again

    TODO: add a default/sample `sitechecker_env_settings.sh` file

- after you've created a db, and configured the settings, set it up via

        $ python ./manage.py makemigrations
        $ python ./manage.py migrate

    TODO: add a default/sample sqlite3.db

- set yourself up as a superuser

        $ python ./manage.py createsuperuser

- start the app on your local devbox

        $ python ./manage.py runserver

    You'll then be able to access it in a browser via `http://127.0.0.1:8000/`

---


##### Usage

- add an entry via the admin

- run the cron-script.py file (see instructions in its docstring)

---


##### Other

- contact: birkin_diana@brown.edu

- TODO
    - add a default/sample `sitechecker_env_settings.sh` file
    - add a default/sample sqlite3.db
    - enable the login/shib module for effortless entry into the admin

---
