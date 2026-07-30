from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID

from fastapi import HTTPException, status


BASE_DIR = Path(__file__).resolve().parent.parent
TENANT_DATA_DIR = BASE_DIR / "tenant_data"


class TenantJsonLoader:

    def __init__(self, tenant_uuid: UUID | str):
        self.tenant_uuid = str(tenant_uuid)

        self.base_path = (
            TENANT_DATA_DIR
            / self.tenant_uuid
        )

        if not self.base_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant data directory not found.",
            )

    def _load(self, filename: str):

        file_path = self.base_path / filename

        if not file_path.exists():
            return []

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
            ) as f:
                return json.load(f)

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{filename} contains invalid JSON.",
            )

    def customers(self):
        return self._load("customers.json")

    def products(self):
        return self._load("products.json")

    def orders(self):
        return self._load("orders.json")

    def tickets(self):
        return self._load("tickets.json")

    def conversations(self):
        return self._load("conversations.json")

    def email_logs(self):
        return self._load("email_logs.json")