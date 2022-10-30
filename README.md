# Lucos Contacts - Google Photos Importer

A python script to import google photo data to [lucos_contacts](https://github.com/lucas42/lucos_contacts)

## Setup

* Run `pipenv install` to install dependencies
* Create a `.env` file and set any necessary environment variables
* Follow the Load Data steps below

## Load Data

* Log into google photos and go to https://photos.google.com/people
* Right click and `View Source`
* Select All and Copy
* Paste the contents into a file called `data.html` at the top level of this project's directory structure

## Running
`pipenv run python import.py`

## Environment Variables

* _**LUCOS_CONTACTS**_ The base url for a running instance of [lucos_contacts](https://github.com/lucas42/lucos_contacts).  Defaults to the production url
* _**LUCOS_CONTACTS_API_KEY**_ A valid api key for _**LUCOS_CONTACTS**_.  Keys can be created manually through the admin UI at `/admin/lucosauth/apiuser/add/`.  Set the **system** field to `lucos_contacts_gphotos_import`.