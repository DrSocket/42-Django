# d08 — Requirements & Compliance

Source: `en.subject_1-2.pdf` (**Version 1.2**), compared against `en.subject.pdf` (Version 1.1).

## 0. What changed between v1.1 and v1.2

The diff is almost entirely grammar, typography and pagination. Only two changes carry weight:

| # | Change | Impact |
|---|--------|--------|
| A | **New rule (Chapter I):** "any credentials, API keys, env variables etc... must be saved locally in a `.env` file and ignored by git. Publicly stored credentials will lead you directly to a failure of the project." | Hard-fail rule, absent from v1.1. |
| B | `requirement.txt` → **`requirements.txt`** | v1.1 carried the filename typo. |

v1.2 also drops the v1.1 "Preamble" chapter (the cat / "chat" pun). It contained no requirements.
Everything else — all five exercises, the jQuery-only rule, the WebSocket rule, the
"leave the default administration application" rule — is identical in substance.

---

## 1. General rules (Chapter I)

| ID | Requirement | Status |
|----|-------------|--------|
| G1 | Project realized in a virtual machine | ✅ `Vagrantfile` (Ubuntu 24.04); `./setup.sh` boots it — see README |
| G2 | VM has all necessary software, configured and installed | ✅ provisioned by the `Vagrantfile` from `requirements.txt`; no external service needed |
| G3 | OS of the VM is your choice | ✅ Ubuntu 24.04 (ships Python 3.12) |
| G4 | VM usable from a cluster computer | ✅ `./setup.sh` runs on a 42 station (Vagrant + VirtualBox preinstalled); box/VM on `/goinfre`, host reaches it at `127.0.0.1:8000` via port-forward |
| G5 | Shared folder between VM and host | ✅ `Vagrantfile` `synced_folder "." → /vagrant`; `DJANGO_DB_PATH` keeps sqlite off the share (vboxsf lacks the POSIX locking sqlite needs) |
| G6 | That folder used to share with the repository at evaluation | ✅ the repo is the shared folder at `/vagrant`; the server runs from it |
| G7 | Must not quit unexpectedly | ✅ `manage.py check` clean; 27 tests pass; verified in-browser |
| G8 | Test programs encouraged | ✅ `account/tests.py`, `chat/tests.py` |
| G9 | Only work in the git repository is graded | ✅ everything committed except `.env` and the local database |
| **G10** | **Credentials in a local, git-ignored `.env`** (new in v1.2) | ✅ see §9 |

## 2. Today's specific rules (Chapter II)

| ID | Requirement | Status | Where |
|----|-------------|--------|-------|
| S1 | jQuery is the only JavaScript library | ✅ | `static/js/jquery.min.js` (3.7.1) is the only library in the project. The transport in ex01–ex04 is the browser's native `WebSocket`, not a library. No Bootstrap, no Socket.IO. |
| S2 | A single Django project, not split per exercise | ✅ | One Django project (package `d09`), two apps: `account` (ex00) and `chat` (ex01–ex04). |
| S3 | Leave the default administration application | ✅ | `django.contrib.admin` installed and routed at `/admin/`; `Room` and `Message` registered in `chat/admin.py`. |
| S4 | `requirements.txt` from `pip freeze` | ✅ | `requirements.txt`, 26 fully-pinned packages. |

> Chapters III–VII each print `Directory: exNN/`, contradicting S2's "It won't be divided
> into exercises". S2 is the operative rule, so there are no `exNN/` directories.

## 3. Exercise 00 — AJAX my formula!

| ID | Requirement | Status | Where |
|----|-------------|--------|-------|
| E00.1 | Project named `d09` | ✅ | Django project package is named `d09`; the repo/day is `d08`. See §10. |
| E00.2 | Application named `account` | ✅ | `account/` |
| E00.3 | `127.0.0.1:8000/account` | ✅ | `account/urls.py` → `path("account", ...)` |
| E00.4 | Login/logout only through AJAX | ✅ | `account/static/account/js/account.js`; verified: 3 XHRs, 0 page loads |
| E00.5 | Not connected → standard login form | ✅ | `_logged_out.html`, built from `AuthenticationForm` |
| E00.6 | Login via AJAX, POST | ✅ | `views.login` is `@require_POST`; GET returns 405 |
| E00.7 | Invalid form → errors appear on the page | ✅ | bound form re-rendered with errors; verified in-browser |
| E00.8 | Valid form → form disappears, new behaviour, no refresh | ✅ | verified: `navigations == 1` across all transitions |
| E00.9 | Connected → `Logged as <user>` | ✅ | `_logged_in.html`, that exact wording |
| E00.10 | Connected → Logout button | ✅ | `_logged_in.html` |
| E00.11 | Logout via AJAX, POST | ✅ | `views.logout` is `@require_POST`; GET returns 405 |
| E00.12 | After logout text and button gone, other behaviour adopted | ✅ | verified in-browser |
| E00.13 | The page must never be refreshed | ✅ | verified: a `window` marker survived every transition |
| E00.14 | Manual refresh returns to the prior behaviour, errors excluded | ✅ | state rendered server-side from `user.is_authenticated`; verified |
| E00.15 | Bootstrap allowed; `AuthenticationForm` free | ✅ | `AuthenticationForm` used; Bootstrap deliberately not used, to keep jQuery the only library |

## 4. Exercise 01 — Basic chat

| ID | Requirement | Status | Where |
|----|-------------|--------|-------|
| E01.1 | Application named `chat` | ✅ | `chat/` |
| E01.2 | A page with 3 links to 3 chatrooms | ✅ | `chat/templates/chat/rooms.html`; seeded by `migrations/0002_default_rooms.py` |
| E01.3 | Room names in the database, suitable model | ✅ | `chat.models.Room` |
| E01.4 | Each link leads to a functional chat | ✅ | `chat/templates/chat/room.html` |
| E01.5 | jQuery only + WebSockets, **no AJAX** | ✅ | verified: 0 XHR/fetch requests on the room page |
| E01.6 | Logged-in users only | ✅ | `@login_required` on both views; consumer closes 4401 for anonymous |
| E01.7 | The chat's name appears | ✅ | `<h1 class="chat-title">` |
| E01.8 | Several users can connect | ✅ | verified with two isolated browser sessions |
| E01.9 | A user can post a message | ✅ | `consumers.receive_json` |
| E01.10 | A message is visible to all users in that room | ✅ | one channel-layer group per room; verified both directions |
| E01.11 | Messages at the bottom, ascending, with poster's name | ✅ | `Message.Meta.ordering = ("created", "id")`; appended, never prepended |
| E01.12 | Messages never disappear, are never replaced, order never changes | ✅ | client only ever appends; verified 25 messages strictly ascending |
| E01.13 | `<username> has joined the chat` for everyone, joiner included | ✅ | `chat.join` broadcast to the whole group after `accept()` |

## 5. Exercise 02 — History

| ID | Requirement | Status | Where |
|----|-------------|--------|-------|
| E02.1 | A joiner sees the last three messages of that room | ✅ | `consumers._recent_messages`, `CHAT_HISTORY_SIZE = 3` |
| E02.2 | Oldest to newest | ✅ | fetched newest-first then reversed; verified exactly `m2, m3, m4` |
| E02.3 | jQuery only + WebSockets | ✅ | replayed over the socket, before the join notice |

## 6. Exercise 03 — User list

| ID | Requirement | Status | Where |
|----|-------------|--------|-------|
| E03.1 | Joiner can see connected users, and appears among them | ✅ | `chat.users` broadcast on connect |
| E03.2 | User list clearly separated from the messages list | ✅ | `<aside class="users">` beside `<div id="messages">` |
| E03.3 | A joining user's name appears in the list for others | ✅ | verified: alice's list went `["alice"] → ["alice","bob"]` |
| E03.4 | A leaving user's name disappears from the list | ✅ | verified: back to `["alice"]` |
| E03.5 | `<username> has left the chat` after the posted messages | ✅ | `chat.leave`, appended like any other row |
| E03.6 | The list updates by itself | ✅ | pushed by the server; no polling, no AJAX |
| E03.7 | jQuery only + WebSockets | ✅ | |

## 7. Exercise 04 — Scroll

| ID | Requirement | Status | Where |
|----|-------------|--------|-------|
| E04.1 | Fixed-size container for the message list | ✅ | `.messages { height: 340px }` in `static/css/app.css` |
| E04.2 | Overflow disappears at the top, scroll bar on the side | ✅ | `overflow-y: auto`; verified 847px content in a 338px box, first row scrolled out |
| E04.3 | Scroll bar always at the bottom so the last messages show | ✅ | `scrollToBottom()` after every append; verified `scrollTop == scrollHeight - clientHeight` |

## 8. Submission (Chapter VIII)

| ID | Requirement | Status |
|----|-------------|--------|
| P1 | Turn in via the git repository | ✅ |
| P2 | Double-check folder and file names | ✅ `account`, `chat`, `requirements.txt` all as named by the subject |
| P3 | Evaluation on the evaluated group's computer | ⚙️ environment |

---

## 9. How G10 (the new v1.2 credentials rule) is satisfied

- `SECRET_KEY` and `DEBUG` are read from `.env` by `d09/settings.py`. Nothing falls back to a
  hardcoded value: a missing variable raises `ImproperlyConfigured` naming the file to create.
- `.env` is the first entry in `.gitignore` and is not committed.
- `.env.example` is committed and holds placeholders only.
- The database is sqlite, so no database user or password exists anywhere in the project.
- `db.sqlite3` and `__pycache__/` are git-ignored, so no local data or build artefact is tracked.

## 10. Note for the evaluator: `d09` vs `d08`

Exercise 00 says "Create a new project named `d09`" in **both** v1.1 and v1.2, so the Django
project package is named **`d09`** (`d09/settings.py`, `d09/urls.py`, `d09/asgi.py`,
`d09/wsgi.py`; `manage.py` and the ASGI/WSGI entry points point at `d09.settings`).

The assignment day and this git repository are **`d08`** — the subject text appears to carry
over from the following day. So: the repo/day is `d08`, the Django project it contains is `d09`.

## 11. Extras beyond the subject

Additive only — the graded login/logout (ex00) and chat (ex01–04) behaviour is unchanged:

- A **create-account form** on `/account` (view `account/register`, template `_register.html`),
  submitted over AJAX like login, so users can be made from the page itself.
- A `manage.py createuser` command (`account/management/commands/createuser.py`).
- Password-strength validators are disabled (`AUTH_PASSWORD_VALIDATORS = []`) so demo/evaluation
  accounts can use simple passwords; this also removes the requirements help-text from the form.

## 12. Verification performed

- `python manage.py check` — no issues.
- `python manage.py test` — **27 tests, all passing** (11 for ex00, 16 for ex01–ex04).
- End-to-end from a clean state: `./setup.sh` boots the Ubuntu 24.04 VM, shares the repo at
  `/vagrant`, installs the deps, migrates + seeds the three rooms, and serves `/account`
  (HTTP 200) reachable from the host at `127.0.0.1:8000` via NAT port-forward.
- Driven in Chrome against the running server: invalid login, valid login, logout, manual
  refresh, two users in isolated sessions, join/leave notices, live user list, three-message
  history, message overflow with scroll pinned to the bottom, and the create-account form.
- Dependencies install from `requirements.txt` entirely from prebuilt wheels on x86_64 Linux;
  they resolve on Python 3.11/3.12/3.13 and **fail on 3.10** (`autobahn` requires >= 3.11).
