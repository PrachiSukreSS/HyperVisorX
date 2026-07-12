"""
app/api/v1/__init__.py
======================
Package marker for the v1 API sub-package.

All version-1 routers live in this package:
  app/api/v1/health.py    ← GET /api/v1/health
  app/api/v1/vms.py       ← (Module 3) VM CRUD + lifecycle endpoints
  app/api/v1/hosts.py     ← (future) Host metrics endpoints
  app/api/v1/storage.py   ← (future) Storage pool endpoints
  app/api/v1/network.py   ← (future) Network config endpoints
  app/api/v1/snapshots.py ← (future) Snapshot endpoints

Having a dedicated v1/ package means adding v2/ in the future requires
zero changes to existing routes.
"""
