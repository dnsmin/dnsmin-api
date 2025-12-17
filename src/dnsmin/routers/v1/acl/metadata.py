from fastapi import Depends

from dnsmin.lib.api.dependencies import get_principal
from dnsmin.models.api import Principal
from dnsmin.models.api.acl.metadata import PermissionsMetadataSchema
from dnsmin.routers.v1.acl import router


@router.get(
    '/metadata',
    response_model=PermissionsMetadataSchema,
    summary='Retrieve Permissions Metadata',
    description='Retrieves all ACL permissions metadata.',
    operation_id='acl:metadata:all',
)
async def list_metadata(
        principal: Principal = Depends(get_principal),
) -> PermissionsMetadataSchema:
    """List ACL permissions metadata."""
    return PermissionsMetadataSchema()
