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

The subject requires the project to run in a virtual machine, with a folder
shared between the VM and the host, and the evaluation happens on the evaluated
group's computer.

### Architecture is not a problem

Verified, not assumed: the committed tree was installed from `requirements.txt`
alone inside an `x86_64` Linux container and passed all 27 tests, with every
package coming from a prebuilt wheel. An Apple-Silicon Mac and an amd64 Linux
box need no different code or pins.

The one rule that matters: **never copy a virtualenv between machines.**
Recreate it with `pip install -r requirements.txt` on each. A copied venv
hardcodes absolute interpreter paths and native binaries for the wrong
architecture.

### Step 0 — check the host can run a VM

```sh
lscpu | grep -o -E 'vmx|svm' | head -1     # non-empty means hardware virtualisation
ls /dev/kvm                                # present means KVM is usable
groups | grep -o -E 'kvm|libvirt|vboxusers'
```

If `/dev/kvm` is missing or you have no `sudo`, see "No root on the host" below.

### Choosing a hypervisor (Linux host, amd64)

| Option | Install | Notes |
|--------|---------|-------|
| **VirtualBox** | `sudo apt install virtualbox` | The usual 42 choice. GUI, easy shared folders via Guest Additions. |
| **virt-manager / KVM** | `sudo apt install virt-manager qemu-kvm libvirt-daemon-system` | Native, noticeably faster. Sharing uses virtiofs rather than Guest Additions. |
| **GNOME Boxes** | `sudo apt install gnome-boxes` | KVM with the simplest UI; least control over sharing. |

Use the **amd64** Ubuntu Server 24.04 LTS ISO — it ships Python 3.12, and the
pinned dependencies need **3.11 or newer** (they fail on 3.10; `autobahn`
requires >= 3.11). Server rather than Desktop keeps the VM small; you only ever
need a shell.

### Guest setup

```sh
sudo apt update
sudo apt install -y python3-venv git
```

### The shared folder (VirtualBox)

1. Install Guest Additions in the guest:
   `sudo apt install -y virtualbox-guest-utils`
2. VM → Settings → Shared Folders → add the host directory holding the repo,
   name it `share`, tick *Auto-mount* and *Make Permanent*.
3. Add yourself to the group that may read it, then log out and back in —
   this step is the usual reason a share looks empty or permission-denied:

```sh
sudo usermod -aG vboxsf $USER
```

The share then appears at `/media/sf_share`.

With **virt-manager** instead, add a Filesystem device (driver `virtiofs`,
target `share`) and mount it in the guest:

```sh
sudo mount -t virtiofs share /mnt/share
```

### Two things that will bite you on a shared folder

**sqlite does not work reliably on a VirtualBox share.** `vboxsf` does not
implement the POSIX locking sqlite needs, so you get "database is locked" or
disk I/O errors. Keep the repository on the share but put the database on the
guest filesystem:

```sh
echo "DJANGO_DB_PATH=$HOME/d08-db.sqlite3" >> .env
```

**Create the virtualenv on the guest filesystem too**, not on the share —
venvs contain symlinks and absolute paths that a share handles poorly, and it
keeps a host-built venv from ever being picked up by mistake:

```sh
python3 -m venv ~/venv-d08
source ~/venv-d08/bin/activate
cd /media/sf_share/d08
pip install -r requirements.txt
```

### Reaching the app from the host browser

Bind the server to every interface — the default `127.0.0.1` is only reachable
from inside the guest:

```sh
python manage.py runserver 0.0.0.0:8000
```

Then pick one:

- **NAT + port forwarding (simplest).** VirtualBox → Settings → Network →
  Advanced → Port Forwarding: host `127.0.0.1:8000` → guest `10.0.2.15:8000`.
  Browse `http://127.0.0.1:8000/account` on the host. Nothing else to change,
  because the Host header stays `127.0.0.1`.

- **Bridged adapter.** The VM gets its own LAN IP. Find it with `ip -4 addr`,
  then browse `http://<vm-ip>:8000/account`. Django will answer **400
  DisallowedHost** until you add that IP:

  ```sh
  echo "DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,<vm-ip>" >> .env
  ```

### No root on the host

If the Linux machine is a locked-down cluster station with no `sudo` and no
`/dev/kvm`, you cannot install a hypervisor. Options, in order of preference:

1. Use whatever hypervisor the campus image already provides — at 42 this is
   normally VirtualBox, already installed.
2. Keep a prepared VM disk image on external storage and open it there; the
   subject explicitly allows any guest OS, and evaluation happens on the
   evaluated group's machine, so a portable image is legitimate.
3. As a fallback for *functional* checking only, a rootless container
   (`podman run --rm -it -v "$PWD":/work -w /work python:3.12-slim bash`)
   reproduces the Linux environment — but a container is not a virtual machine
   and does not satisfy the requirement on its own.

### Building on an Apple-Silicon Mac

To develop on the Mac before moving to Linux, **UTM** (macOS only — it is not
available on the Linux host) runs an **arm64** Ubuntu 24.04 guest natively:

```sh
brew install --cask utm
```

Share a folder with UTM's VirtFS directory share and mount it in the guest:

```sh
sudo mkdir -p /mnt/share && sudo mount -t 9p -o trans=virtio share /mnt/share
```

Note that such a VM is **arm64**, so it does not by itself prove anything about
the amd64 target; the container check described above does.
