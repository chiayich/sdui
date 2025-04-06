# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.database import Base  # noqa
from app.models.user import User  # noqa
from app.models.organization import OrganizationNode, Role, Permission, RolePermission, RoleOrgPermission  # noqa
from app.models.sdui_config import SDUIConfig  # noqa 