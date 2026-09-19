# d08 — Training Python-Django 3 (Final)

AJAX and WebSockets with Django. A single Django project named `d09` (as ex00
requires) holding two applications:

| App | Exercises | What it does |
|-----|-----------|--------------|
| `account` | ex00 | Login / logout driven entirely by AJAX; the page is never refreshed. |
| `chat` | ex01–ex04 | Three database-backed chatrooms over WebSockets, with history, a live connected-user list and a scrolling message pane. |

`REQUIREMENTS.md` maps every requirement of the subject to the code that satisfies it.

## Run it in the VM — one command

The subject requires the project to run in a virtual machine with a folder
shared between host and VM. On a 42 station everything needed (Vagrant,
VirtualBox) is already installed, so bringing it up is a single command:

```sh
./setup.sh
```

`setup.sh` boots an **Ubuntu 24.04** VM, **shares this repository into it** (the
required host↔VM shared folder, mounted at `/vagrant`), installs the project and
starts the server. Then open <http://127.0.0.1:8000/account> on the host.

- The box cache and VM disk go to local scratch storage — `/goinfre`, else
  `/sgoinfre`, else `/tmp` — so the small NFS home is untouched. Override with
  `D08_WORKDIR=/path ./setup.sh`.
- First run takes a few minutes (it downloads the base box and installs the
  dependencies). Re-running `./setup.sh` reuses the VM and just starts the
  server again. `Ctrl-C` stops the server; `vagrant halt` powers off the VM.
- Ubuntu 24.04 is used on purpose: it ships **Python 3.12**. Ubuntu 22.04 ships
  3.10, on which the pinned dependencies fail (`autobahn` needs ≥ 3.11).

### Accounts

Seeded automatically: `admin`/`adminadmin` (superuser), `alice`/`alicealice`,
`bob`/`bobbobbob`. Create more from the **Create account** form on the page, or:

```sh
python manage.py createuser <name>          # prompts for a password
python manage.py createuser <name> --admin  # a superuser instead
```

## Credentials (Chapter I / G10)

Secrets live in a local `.env` that git ignores; nothing is hardcoded.

- `SECRET_KEY` and `DEBUG` are read from `.env` (`d09/settings.py`); a missing
  `.env` raises `ImproperlyConfigured` rather than falling back to a default.
- `setup.sh` (via the Vagrantfile) generates `.env` inside the VM on first run.
- `.env` is the first entry in `.gitignore` and is **not** committed; only
  `.env.example` (placeholders) is. The database is sqlite, so there is no
  database user or password anywhere.

## Running without the VM (development)

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -c "from django.core.management.utils import get_random_secret_key as k; print('DJANGO_SECRET_KEY=' + k())" > .env
echo "DJANGO_DEBUG=True" >> .env
python manage.py migrate          # also creates the three chatrooms
python manage.py runserver
```

Requires **Python 3.11+** (the pinned deps fail on 3.10). Then open
<http://127.0.0.1:8000/account>.

## Tests

```sh
python manage.py test
```

27 tests covering the graded behaviour: the `/account` URL and both of its
states, the login/logout JSON endpoints including form errors and CSRF, the
room model and views, and the consumer (auth refusal, broadcast, join/leave
notices, three-message history, live user list, multi-tab handling).

## Layout

```
d08/
├── setup.sh             # one command: boot the VM + run the server
├── Vagrantfile          # the VM (Ubuntu 24.04) + shared folder + provisioning
├── .env.example         # committed placeholders; real .env is git-ignored
├── manage.py
├── requirements.txt     # pip freeze
├── d09/                 # project (config) package — named d09 per the subject
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py          # HTTP + WebSocket routing
│   └── wsgi.py
├── account/             # ex00
│   ├── views.py         # AJAX login/logout endpoints returning JSON
│   ├── management/commands/createuser.py   # make a login user from the CLI
│   ├── templates/account/
│   │   ├── account.html      # /account page
│   │   ├── _logged_out.html  # login + create-account form
│   │   ├── _logged_in.html   # "Logged as <user>" state
│   │   └── _register.html     # AJAX create-account form
│   └── static/account/js/account.js
├── chat/                # ex01-ex04
│   ├── models.py        # Room, Message
│   ├── consumers.py     # ChatConsumer: join/leave, broadcast, history, users
│   ├── routing.py       # ws/chat/<slug>/
│   ├── migrations/0002_default_rooms.py   # seeds the three rooms
│   ├── templates/chat/{rooms,room}.html
│   └── static/chat/js/chat.js
├── templates/base.html
└── static/
    ├── css/app.css
    └── js/jquery.min.js  # jQuery 3.7.1, the only JS library used
```

## Extras beyond the subject

Additive only; the graded login/logout and chat behaviour is unchanged.

- A **create-account form** on `/account` (`account/register`), submitted over
  AJAX like login, so users can be made from the page itself.
- A `manage.py createuser` command (`account/management/commands/`).
- Password-strength validators are disabled (`AUTH_PASSWORD_VALIDATORS = []`) so
  demo/evaluation accounts can use simple passwords.

## Note: `d09` vs `d08`

Exercise 00 says *"create a project named `d09`"*, so the Django project package
is named **`d09`** (`manage.py` points at `d09.settings`). The assignment day and
this git repository are **`d08`** — the subject text carried over from the next
day. In short: the repo/day is `d08`, the Django project inside it is `d09`. See
`REQUIREMENTS.md §10`.
