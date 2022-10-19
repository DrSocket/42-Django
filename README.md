To untar:
`tar xvf (filename)`

End all python files with 

	if __name__ == '__main__':
	your_function( whatever, parameter, is, required )

Empty block: use `pass` statement

redirect error spam message to /dev/null `2>/dev/null`


shared folder virtualbox
https://linuxconfig.org/share-folders-virtualbox-quick-linux-setup

Permission problems for guest user in vbox:
Add yourself to the vboxsf group within the guest VM.

Solution 1

Run sudo adduser $USER vboxsf from terminal.
(On Suse it's sudo usermod --append --groups vboxsf $USER)
To take effect you should log out and then log in, or you may need to reboot.


Change disk partition sizes vbox
https://gparted.org/download.php

a voir: https://www.codequoi.com/

import antigravity
https://python-history.blogspot.com/2010/06/import-antigravity.html

## PYTHON ENV
python3 -m venv env
source env/bin/activate
deactivate

### Install Packages
python3 -m pip install (package-name)
or put in requirement.txt
pip install -r requirement.txt

## Begin Django
requirements:
Django
psycopg2-binary
`django-admin startproject django_project .`

## Start server
`python manage.py runserver` -> server running on localhost:8000

remove unapplied migrations (because of unmigrated database)
`python manage.py migrate`

## Create new app
`python manage.py startapp (app-name)` inside project folder

add pages.apps.PagesConfig to INSTALLED_APPS in django_project/settings.py

## Django Template Language

https://docs.djangoproject.com/en/4.1/ref/templates/language/

### Built-in tags and filters
https://docs.djangoproject.com/en/4.1/ref/templates/builtins/

## Docker compose cheatsheet
https://devhints.io/docker-compose

### Start docker desktop parrot os (after full install)
`systemctl --user start docker-desktop`
stop `systemctl --user stop docker-desktop`

## Django Model Meta Options
https://docs.djangoproject.com/en/4.1/ref/models/options/