from pathlib import Path
import json


class TenantDatabaseManager:

    BASE_DIR = (
        Path(__file__).resolve().parent.parent
        / "tenant_data"
    )

    DEFAULT_FILES = {
        "customers.json": [],
        "products.json": [],
        "orders.json": [],
        "tickets.json": [],
        "conversations.json": [],
        "email_logs.json": [],
    }

    @classmethod
    def create_database(cls, tenant_uuid):

        tenant_dir = cls.BASE_DIR / str(tenant_uuid)

        tenant_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        for filename, default_data in cls.DEFAULT_FILES.items():

            file_path = tenant_dir / filename

            if not file_path.exists():

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, indent=4)

        return tenant_dir