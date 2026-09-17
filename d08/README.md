# d08 — Training Python-Django 3 (Final)

AJAX and WebSockets with Django. A single Django project named `d08` holding two
applications:

| App | Exercises | What it does |
|-----|-----------|--------------|
| `account` | ex00 | Login / logout driven entirely by AJAX, page never refreshed. |
| `chat` | ex01–ex04 | Three database-backed chatrooms over WebSockets, with history, a live connected-user list and a scrolling message pane. |

`REQUIREMENTS.md` maps every requirement of the subject to the code that satisfies it.

## Requirements

- **Python 3.11 or newer.** Verified: the pinned dependencies resolve on
  x86_64 Linux for 3.11, 3.12 and 3.13, and **fail on 3.10** (`autobahn`
  requires >= 3.11). Ubuntu 24.04 LTS ships 3.12 and is the reference target.
- No external services. The channel layer is in-memory, so there is no Redis to
  install or start.

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Secrets are not in git (see below). Create your own .env:
cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as k; print('DJANGO_SECRET_KEY=' + k())" > .env
echo "DJANGO_DEBUG=True" >> .env

python manage.py migrate          # also creates the three chatrooms
python manage.py createsuperuser  # to log in with
python manage.py runserver
```

Then open <http://127.0.0.1:8000/account>.

If `.env` is missing, the project stops with an `ImproperlyConfigured` error
naming the file to create — it never falls back to a hardcoded key.

## Credentials

Chapter I of the subject requires credentials, API keys and environment
variables to be kept in a local `.env` that git ignores. In this project:

- `SECRET_KEY` and `DEBUG` are read from `.env` (`d08/settings.py`).
- `.env` is listed in `.gitignore` and is **not** committed.
- `.env.example` is committed and contains placeholders only.
- The database is sqlite, so there is no database user or password anywhere.

## Layout

```
d08/
├── .env.example         # committed placeholders; real .env is git-ignored
├── manage.py
├── requirements.txt     # pip freeze
├── d08/                 # project package
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py          # HTTP + WebSocket routing
│   └── wsgi.py
├── account/             # ex00
│   ├── views.py         # AJAX login/logout endpoints returning JSON
│   ├── templates/account/
│   │   ├── account.html      # /account page
│   │   ├── _logged_out.html  # login form state
│   │   └── _logged_in.html   # "Logged as <user>" state
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

## Tests

```sh
python manage.py test
```

27 tests covering the graded behaviour: the `/account` URL and both of its
states, the login/logout JSON endpoints including form errors and CSRF, the
room model and views, and the consumer (auth refusal, broadcast, join/leave
notices, three-message history, live user list, multi-tab handling).

## Running it in a VM

The subject requires the project to run in a virtual machine with a folder
shared with the host.

The build machine here is an Apple-Silicon (arm64) Mac and the target is an
amd64 Linux box. That difference does not affect the project: every dependency
is either pure Python or publishes wheels for both architectures. The one rule
that matters is **never copy a virtualenv between machines** — recreate it with
`pip install -r requirements.txt` on each. A copied venv hardcodes absolute
interpreter paths and native binaries for the wrong architecture.

Suggested VM on Apple Silicon — **UTM** (free) with **Ubuntu Server 24.04 LTS
arm64**, which runs natively through Apple's hypervisor rather than being
emulated, and ships Python 3.12:

```sh
brew install --cask utm
```

Share a folder with the host via UTM's *VirtFS* directory share, then inside
the guest:

```sh
sudo apt update && sudo apt install -y python3-venv git
sudo mkdir -p /mnt/share && sudo mount -t 9p -o trans=virtio share /mnt/share
```

On the amd64 Linux machine later, the same commands work unchanged: clone the
repository, create a fresh venv, `pip install -r requirements.txt`, write a new
`.env`, `migrate`, `runserver`.
