# Odoo 19 Development Setup

macOS + PostgreSQL (Docker Port 5434) + pyenv + venv

---

## Overview

This project runs Odoo 19 using:

- macOS
- PostgreSQL via Docker (host port 5434)
- Python 3.12 (managed by pyenv)
- Virtual environment per project
- Development mode with auto-reload

This setup is isolated, clean, and upgrade-safe.

---

# 1. System Requirements

Install the following:

- Docker
- pyenv
- PostgreSQL client (psql)
- Node.js (recommended for assets)
- wkhtmltopdf (optional, for PDF reports)

---

# 2. PostgreSQL Setup (Docker, Port 5434)

## Remove existing container (if any)

```bash
docker rm -f odoo-postgres
```

## Run PostgreSQL container

```bash
docker run --name odoo-postgres \
  -e POSTGRES_USER=odoo \
  -e POSTGRES_PASSWORD=odoo \
  -e POSTGRES_DB=postgres \
  -p 5434:5432 \
  -d postgres:15
```

## Verify container

```bash
docker ps
```

Expected output should include:

```
0.0.0.0:5434->5432/tcp
```

## Test connection

```bash
psql -h localhost -p 5434 -U odoo -d postgres
```

If connection succeeds, PostgreSQL is ready.

---

# 3. Python Setup (pyenv)

## Install Python 3.12.x

```bash
pyenv install 3.12.3
pyenv local 3.12.3
python -V
```

Ensure Python version is 3.12.x.

---

# 4. Create Virtual Environment

From project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip wheel setuptools
```

---

# 5. Install Odoo Dependencies

```bash
pip install -r requirements.txt
```

If psycopg2 fails:

```bash
pip install psycopg2-binary
```

---

# 6. Recommended Project Structure

```
odoo-19/
├── odoo/               # Core framework
├── addons/             # Official modules
├── custom_addons/      # Custom modules
├── logs/
├── .venv/
├── odoo-bin
└── odoo.conf
```

Create folders if missing:

```bash
mkdir custom_addons
mkdir logs
```

---

# 7. Odoo Configuration

Create `odoo.conf` in the project root:

```ini
[options]

; Database
db_host = localhost
db_port = 5434
db_user = odoo
db_password = odoo

; Module paths
addons_path = odoo/addons,addons,custom_addons

; Logging
logfile = logs/odoo.log
log_level = info

; Admin password
admin_passwd = admin
```

---

# 8. Run Odoo (Development Mode)

Activate virtual environment:

```bash
source .venv/bin/activate
```

Start server:

```bash
./odoo-bin -c odoo.conf --dev=reload --limit-time-real=0 --limit-time-cpu=0
```

Open browser:

[http://localhost:8069](http://localhost:8069)

Create a new database from the UI.

---

# 9. Development Workflow

## Terminal 1 – Run Server

```bash
source .venv/bin/activate
./odoo-bin -c odoo.conf --dev=reload
```

## Terminal 2 – Upgrade Module

```bash
source .venv/bin/activate
./odoo-bin -c odoo.conf -u my_module --stop-after-init
```

---

# 10. When to Upgrade Module (-u)

You must upgrade the module when:

- Adding new fields
- Modifying model structure
- Updating XML views
- Changing security rules
- Updating manifest
- Modifying data XML

Reload alone is not sufficient because Odoo stores metadata in the database.

---

# 11. Developer Mode (Frontend Debug)

From UI:

Settings → Developer Mode (with assets)

Useful for:

- Debugging JavaScript
- Debugging CSS
- Inspecting QWeb templates

---

# 12. Useful Commands

## Restart PostgreSQL container

```bash
docker restart odoo-postgres
```

## Stop container

```bash
docker stop odoo-postgres
```

## View Odoo logs

```bash
tail -f logs/odoo.log
```

---

# 13. Best Practices

- Never modify `odoo/` (core framework)
- Avoid modifying official modules in `addons/`
- Always extend using `_inherit`
- Keep custom modules inside `custom_addons/`
- Use `-u` for structural changes
- Keep development environment isolated per project

---

# 14. Clean Development Principles

- Python isolated via pyenv
- Virtual environment per project
- Dockerized PostgreSQL
- Custom modules separated from core
- Configuration tracked in version control
- Safe for future Odoo upgrades

---

This setup provides a stable and professional Odoo 19 development environment.
