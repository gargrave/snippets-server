# Dev Notes

## Command Shortcuts

Since we are using multiple settings files, it can be a bit of a nuisance to enter some common commands. Let's create some shortcuts for them!

```sh
source ../venv_snippets2/bin/activate
export run="python manage.py runserver --settings=main.settings.dev"
export static="python manage.py collectstatic --settings=main.settings.dev"
export test="python manage.py test --settings=main.settings.dev"
export migrate="python manage.py migrate --settings=main.settings.dev"
export deploy_dev="git push heroku-dev dev:master"
export deploy_prod="git push heroku-prod master"
```

...and here are some pre-typed ones that are probably not common enough to warrant their own shortcuts.

```sh
python manage.py makemigrations api_snippets_v1 --settings=main.settings.dev
python manage.py createsuperuser --settings=main.settings.dev
```

---

## Deployment Checklist

- Test dev branch on dev
    - `git push heroku-dev dev:master`
- Merge dev/working branch to master
- Upload to prod
    - `git push heroku-prod master`
- Be sure to migrate the Heroku apps as needed!

---

## Heroku Notes

- add `--app APP` to the end of a command to specify which app
    - `heroku run python manage.py migrate --app snippets-staging`
- settings:
    - `heroku config:set DJANGO_SETTINGS_MODULE=main.settings.prod --app snippets-prod`
