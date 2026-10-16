# HyperVisorX

HyperVisorX is a Linux virtualization management platform for operating and monitoring KVM/libvirt virtual machines through a FastAPI REST API and a React dashboard.

It provides VM lifecycle controls, QCOW2 snapshot management, host and VM monitoring, JWT-based authentication, and a browser interface for administrators and operators.

> **Project status:** This repository is under active development. Several routers, frontend pages, and service modules are currently scaffolding or incomplete, so review the implementation before using HyperVisorX in a production environment.

## Features

- List virtual machines managed by libvirt
- Inspect VM details and runtime state
- Start, gracefully shut down, force stop, restart, suspend, and resume VMs
- Create, list, restore, and delete QCOW2 snapshots
- Collect host CPU, memory, disk, and network metrics with `psutil`
- Collect VM CPU, memory, and network statistics through libvirt
- FastAPI Swagger UI and ReDoc documentation
- JWT authentication with role checks for admin, operator, and viewer users
- React dashboard with live metrics polling and charts
- Request logging with correlation IDs through the `X-Request-ID` response header
- SQLAlchemy database foundation with Alembic migration support

## Architecture

```text
React + Vite frontend
        |
        | Axios / JSON over HTTP
        v
FastAPI application (Backend/app/main.py)
        |
        +--> Routers: auth, VM, monitoring, console, health
        |
        +--> Services: VM, monitoring, authentication, console
        |
        +--> libvirt manager --> libvirt daemon --> QEMU/KVM
        |
        +--> SQLAlchemy --> PostgreSQL
```

The backend is composed in `Backend/app/main.py`. Requests are routed under `/api/v1`, then delegated to service classes. VM operations use `VirtualMachineManager`, which opens a libvirt connection using `LIBVIRT_URI`. Monitoring combines host metrics from `psutil` with VM metrics from libvirt. Authentication uses a PostgreSQL-backed user model and JWT access tokens.

## Repository layout

```text
Backend/
├── app/
│   ├── api/v1/       Versioned health endpoint
│   ├── core/         Configuration, database, logging, and security
│   ├── dependencies/ Authentication and request dependencies
│   ├── libvirt/      libvirt connection and VM management logic
│   ├── models/       SQLAlchemy ORM models
│   ├── routers/      FastAPI route groups
│   ├── schemas/      Pydantic request and response schemas
│   ├── services/     Authentication, VM, monitoring, and console services
│   └── main.py       FastAPI application entry point
├── alembic/          Database migration configuration and versions
├── scripts/          Snapshot copy and deletion shell scripts
├── requirements.txt  Python dependencies
└── test_*.py         Local smoke-test scripts

Frontend/
├── src/
│   ├── api/          Axios client and authentication API helpers
│   ├── components/  Shared dashboard, navigation, and chart components
│   ├── pages/       Dashboard, console, snapshots, and planned views
│   ├── services/     Shared API client
│   └── App.jsx       React Router configuration
├── package.json       Vite scripts and JavaScript dependencies
└── vite.config.js     Vite configuration

logs/
└── app.log           Application log output
```

## Requirements

HyperVisorX is intended to run on a Linux host with virtualization enabled.

- Python 3.10 or newer
- Node.js and npm
- QEMU/KVM
- libvirt and the Python libvirt bindings
- A running libvirt daemon
- PostgreSQL, if using the database-backed authentication and ORM models
- Permission to access the system libvirt connection and VM disk files

The backend configuration defaults to the system libvirt URI `qemu:///system` and PostgreSQL database `hypervisorx` on `localhost:5432`.

> **Dependency check:** The application imports additional packages such as `libvirt`, `psutil`, SQLAlchemy, and JWT/security-related libraries. Ensure these are installed in the backend environment if they are not present in the current `requirements.txt`.

## Configuration

Create `Backend/.env` before starting the backend. `SECRET_KEY` is required by `app/core/config.py`.

```dotenv
APP_NAME=HyperVisorX
APP_VERSION=0.1.0
DEBUG=true
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
API_PREFIX=/api/v1
LIBVIRT_URI=qemu:///system
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/hypervisorx
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

For production, use a strong secret stored outside Git, set `DEBUG=false`, restrict CORS origins, and use a database password appropriate for the deployment.

## Backend setup

From the repository root:

```bash
cd Backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is then available at:

- Root status: `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/api/v1/health`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

If the package is not being resolved, run the command from `Backend/` or set `PYTHONPATH` to the backend directory.

## Frontend setup

In a second terminal:

```bash
cd Frontend
npm install
npm run dev
```

The Vite development server normally runs at `http://localhost:5173`. The frontend API clients currently target `http://127.0.0.1:8000/api/v1`; update `Frontend/src/api/axios.js` and `Frontend/src/services/api.js` or move the URL to an environment variable when deploying elsewhere.

Other frontend commands:

```bash
npm run build
npm run preview
npm run lint
```

## API overview

All routes below are prefixed with `/api/v1`.

### Health

```text
GET /health
```

Returns application status, version, and a UTC timestamp.

### Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
GET  /auth/admin
GET  /auth/operator
GET  /auth/viewer
```

Login returns a bearer token. The frontend Axios interceptor reads `access_token` from `localStorage` and sends it as an `Authorization: Bearer ...` header.

### Virtual machines

```text
GET    /vms/
GET    /vms/{vm_name}
POST   /vms/{vm_name}/start
POST   /vms/{vm_name}/shutdown
POST   /vms/{vm_name}/stop
POST   /vms/{vm_name}/restart
POST   /vms/{vm_name}/suspend
POST   /vms/{vm_name}/resume
GET    /vms/{vm_name}/snapshots
POST   /vms/{vm_name}/snapshot/{snapshot_name}
POST   /vms/{vm_name}/snapshot/{snapshot_name}/restore
DELETE /vms/{vm_name}/snapshot/{snapshot_name}
```

VM actions are executed through libvirt. Snapshot creation and restoration currently expect VM disks under `/var/lib/libvirt/images/` and use shell scripts under `Backend/scripts/`.

### Monitoring

```text
GET /monitoring/
GET /monitoring/host/cpu
GET /monitoring/host/memory
GET /monitoring/host/disk
GET /monitoring/host/network
GET /monitoring/vm/{vm_name}
GET /monitoring/vm/{vm_name}/network
```

The dashboard polls `/monitoring/` every three seconds and retains a short in-memory history for its charts.

### Console

```text
GET /console/{vm_name}
```

The console endpoint is wired into the application, but its service implementation should be reviewed before relying on it.

## Snapshots and permissions

Snapshot operations require the VM to be shut off. The implementation currently:

1. Looks for the source disk at `/var/lib/libvirt/images/{vm_name}.qcow2`.
2. Stores snapshots under `snapshots/{vm_name}/` relative to the backend process directory.
3. Calls shell scripts through `sudo` to copy or delete QCOW2 files.

Before using this functionality, verify file ownership, sudo permissions, script paths, and disk safety. The current implementation contains host-specific absolute script paths and should be made configurable before deployment to another machine.

## Smoke tests

The repository includes simple scripts for checking libvirt connectivity, listing VMs, and creating/verifying a JWT. Run them from `Backend/` with the virtual environment active:

```bash
python test_libvirt.py
python test_list_vm.py
python test_hash.py
```

These are executable smoke-test scripts rather than a complete automated test suite.

## Development notes

- The backend exposes CORS for `localhost:5173` and `127.0.0.1:5173`.
- The API has a global JSON exception handler and request timing logs.
- The database layer uses SQLAlchemy sessions and Alembic configuration is present under `Backend/alembic/`.
- Several route files and frontend pages are currently empty or placeholders; implement and test them before advertising those features as complete.
- Avoid committing `.env` files, JWT secrets, credentials, generated logs, or VM disk images.

## Security considerations

HyperVisorX can start, stop, destroy, and modify virtual machines. Run it only on a trusted management network and apply least-privilege access to libvirt and VM storage. Before production use:

- Replace development secrets and credentials.
- Remove hardcoded host-specific paths.
- Replace broad CORS settings with an explicit frontend origin.
- Add authorization dependencies to destructive VM and snapshot endpoints.
- Validate VM and snapshot names before using them in filesystem paths.
- Add tests for authentication, authorization, error handling, and snapshot safety.
- Put the API behind TLS and an authenticated reverse proxy where appropriate.

## License

No license file is currently present in the repository. Add a license before distributing HyperVisorX.
