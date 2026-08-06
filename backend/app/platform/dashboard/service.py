from sqlalchemy.orm import Session
from sqlalchemy import func

from app.platform.tenants.models import Tenant


class DashboardService:

    def __init__(self, db: Session):
        self.db = db

    def get_stats(self):

        total_tenants = (
            self.db.query(func.count(Tenant.id))
            .scalar()
        )

        return {
            "total_tenants": total_tenants,
        }