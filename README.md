# HyperVisorX

HyperVisorX is a Linux virtualization management platform for managing and monitoring KVM/libvirt virtual machines through a FastAPI backend and React-based web dashboard.

The project provides virtual machine lifecycle controls, VM monitoring, snapshot management, authentication, resource usage charts, and a browser-based management interface.

> **Status:** HyperVisorX is under active development. Some modules and frontend pages are incomplete or currently serve as scaffolding. Review the implementation and security configuration before using it in production.

## Features

- List and inspect libvirt virtual machines
- Start, shut down, stop, restart, suspend, and resume VMs
- Create, list, restore, and delete QCOW2 snapshots
- Monitor host CPU, memory, disk, and network usage
- Monitor VM CPU, memory, and network statistics
- JWT-based authentication
- Role-based access checks for admin, operator, and viewer users
- React monitoring dashboard with live metric polling
- Charts for CPU, memory, and disk usage
- FastAPI Swagger and ReDoc documentation
- SQLAlchemy database integration
- Alembic migration support
- Request logging with request IDs
- CORS support for the local React development server

## Architecture

```text
React + Vite frontend
        |
        | Axios / REST API
        v
FastAPI backend
        |
        +--> Authentication and authorization
        |
        +--> VM and monitoring services
        |
        +--> libvirt connection
        |        |
        |        +--> QEMU/KVM virtual machines
        |
        +--> SQLAlchemy
                 |
                 +--> PostgreSQL
```

The backend entry point is `Backend/app/main.py`. API requests are grouped into routers and mounted under the `/api/v1` prefix. Service classes contain the application logic, while `VirtualMachineManager` handles communication with libvirt.

## Project Structure

```text
HyperVisorX/
├── Backend/
│   ├── app/
│   │   ├── api/v1/          Versioned API endpoints such as health checks
│   │   ├── core/            Configuration, database, logging, and security
│   │   ├── dependencies/    FastAPI authentication dependencies
│   │   ├── libvirt/         libvirt connection and VM management
│   │   ├── models/          SQLAlchemy database models
│   │   ├── routers/         FastAPI route modules
│   │   ├── schemas/         Pydantic request and response schemas
│   │   ├── services/        Authentication, VM, monitoring, and console services
│   │   └── main.py          FastAPI application entry point
│   ├── alembic/              Database migration configuration
│   ├── scripts/              Snapshot management shell scripts
│   ├── requirements.txt      Python dependencies
│   └── test_*.py             Local libvirt and authentication smoke tests
│
├── Frontend/
│   ├── src/
│   │   ├── api/              Axios clients and authentication helpers
│   │   ├── components/       Shared UI components
│   │   ├── pages/            Dashboard, console, and snapshot pages
│   │   ├── services/         API service clients
│   │   ├── App.jsx           React Router configuration
│   │   └── main.jsx          Frontend entry point
│   ├── package.json           Frontend dependencies and scripts
│   └── vite.config.js         Vite configuration
│
└── logs/                      Application log output
```

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic Settings
- SQLAlchemy
- Alembic
- PostgreSQL
- libvirt
- QEMU/KVM
- psutil
- JWT authentication

### Frontend

- React
- Vite
- React Router
- Axios
- Tailwind CSS
- Chart.js
- Recharts

## Requirements

HyperVisorX is designed for a Linux system with virtualization support.

You will need:

- Python 3.10 or newer
- Node.js and npm
- QEMU/KVM
- libvirt
- Python libvirt bindings
- A running libvirt daemon
- PostgreSQL
- Permission to access libvirt and VM disk files

Verify that virtualization is available on the host:

```bash
sudo systemctl status libvirtd
virsh list --all
```

Depending on the Linux distribution, the libvirt service may be named `libvirt` instead of `libvirtd`.

## Backend Setup

Clone the repository and enter the backend directory:

```bash
git clone https://github.com/PrachiSukreSS/HyperVisorX.git
cd HyperVisorX/Backend
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file inside the `Backend` directory:

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

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

Once the backend is running, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

## Frontend Setup

Open a second terminal:

```bash
cd HyperVisorX/Frontend
npm install
npm run dev
```

The frontend development server normally runs at:

```text
http://localhost:5173
```

The frontend currently communicates with the backend at:

```text
http://127.0.0.1:8000/api/v1
```

This URL is configured in:

```text
Frontend/src/api/axios.js
Frontend/src/services/api.js
```

For deployment, it is recommended to move the API URL into a Vite environment variable.

## Frontend Commands

```bash
npm run dev
```

Starts the Vite development server.

```bash
npm run build
```

Creates a production build.

```bash
npm run preview
```

Previews the production build locally.

```bash
npm run lint
```

Runs ESLint.

## API Endpoints

All versioned endpoints use the `/api/v1` prefix.

### Health

```http
GET /api/v1/health
```

Returns the application status, version, and current UTC timestamp.

### Authentication

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
GET  /api/v1/auth/admin
GET  /api/v1/auth/operator
GET  /api/v1/auth/viewer
```

The login endpoint returns a JWT bearer token.

Example response:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

The frontend authentication client stores the token in `localStorage` and sends it with subsequent requests.

### Virtual Machines

```http
GET    /api/v1/vms/
GET    /api/v1/vms/{vm_name}
POST   /api/v1/vms/{vm_name}/start
POST   /api/v1/vms/{vm_name}/shutdown
POST   /api/v1/vms/{vm_name}/stop
POST   /api/v1/vms/{vm_name}/restart
POST   /api/v1/vms/{vm_name}/suspend
POST   /api/v1/vms/{vm_name}/resume
GET    /api/v1/vms/{vm_name}/snapshots
POST   /api/v1/vms/{vm_name}/snapshot/{snapshot_name}
POST   /api/v1/vms/{vm_name}/snapshot/{snapshot_name}/restore
DELETE /api/v1/vms/{vm_name}/snapshot/{snapshot_name}
```

### Monitoring

```http
GET /api/v1/monitoring/
GET /api/v1/monitoring/host/cpu
GET /api/v1/monitoring/host/memory
GET /api/v1/monitoring/host/disk
GET /api/v1/monitoring/host/network
GET /api/v1/monitoring/vm/{vm_name}
GET /api/v1/monitoring/vm/{vm_name}/network
```

The dashboard periodically requests `/api/v1/monitoring/` to display live host metrics.

### Console

```http
GET /api/v1/console/{vm_name}
```

The console route is registered in the backend. The console service should be reviewed and completed before using it in production.

## Snapshot Management

Snapshot operations currently use QCOW2 disk images.

The implementation expects VM disk images at:

```text
/var/lib/libvirt/images/{vm_name}.qcow2
```

Snapshots are stored under:

```text
snapshots/{vm_name}/{snapshot_name}.qcow2
```

Snapshot operations require the VM to be shut down.

The backend uses shell scripts in `Backend/scripts/` to copy and delete snapshot files. Before using this feature, verify:

- File ownership and permissions
- `sudo` configuration
- VM disk locations
- Snapshot storage capacity
- Script paths
- Backup and recovery procedures

## Smoke Tests

The repository includes simple scripts for testing libvirt connectivity, VM listing, and JWT creation.

Run them from the `Backend` directory:

```bash
python test_libvirt.py
python test_list_vm.py
python test_hash.py
```

These are basic smoke tests and are not a replacement for a complete automated test suite.

## Security Considerations

HyperVisorX can perform privileged operations such as starting, stopping, destroying, and modifying virtual machines.

Before production deployment:

- Use a strong, private `SECRET_KEY`
- Never commit `.env` files or credentials
- Set `DEBUG=false`
- Restrict CORS to the trusted frontend origin
- Use HTTPS
- Protect destructive VM operations with authorization checks
- Validate VM and snapshot names before using them in filesystem paths
- Remove hardcoded machine-specific paths
- Configure least-privilege libvirt and filesystem access
- Add audit logging for administrative actions
- Protect the API behind a trusted network or reverse proxy

## Development Notes

The repository currently contains several placeholder or incomplete modules, including some frontend pages and backend route/service files. Features should be tested against the current implementation before being treated as production-ready.

The current implementation also contains machine-specific snapshot script paths. These should be replaced with configurable paths before deploying HyperVisorX to another host.

## Contributing

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Make and test your changes.
4. Commit your changes:

   ```bash
   git commit -m "Add your change"
   ```

5. Push the branch:

   ```bash
   git push origin feature/your-feature
   ```

6. Open a pull request.

## License

No license file is currently included in this repository.

Add an appropriate license before distributing or using HyperVisorX as a public or commercial project.
