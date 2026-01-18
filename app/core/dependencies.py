from app.services import (
    AuthService,
    UserService,
    PropertyService,
    UnitService,
    TenantService,
    RentLedgerService,
    PaymentService,
    UtilityService,
    ExpenseService,
    DocumentService,
    AdjustmentService,
    CloudflareService,
)
from app.models import (
    User,
    Property,
    Unit,
    Tenant,
    RentLedger,
    Payment,
    UtilityBill,
    Expense,
    TenantDocument,
    Adjustment,
    RefreshToken,
)


async def get_user_service() -> UserService:
    return UserService(model=User)


async def get_auth_service() -> AuthService:
    return AuthService(model=User, refresh_token_model=RefreshToken)


async def get_property_service() -> PropertyService:
    return PropertyService(model=Property)


async def get_unit_service() -> UnitService:
    return UnitService(model=Unit, property_model=Property)


async def get_tenant_service() -> TenantService:
    return TenantService(model=Tenant, unit_model=Unit, ledger_model=RentLedger)


async def get_rent_ledger_service() -> RentLedgerService:
    return RentLedgerService(model=RentLedger, tenant_model=Tenant)


async def get_payment_service() -> PaymentService:
    return PaymentService(model=Payment, tenant_model=Tenant, ledger_model=RentLedger)


async def get_utility_service() -> UtilityService:
    return UtilityService(
        model=UtilityBill, tenant_model=Tenant, ledger_model=RentLedger
    )


async def get_adjustment_service() -> AdjustmentService:
    return AdjustmentService(
        model=Adjustment, tenant_model=Tenant, ledger_model=RentLedger
    )


async def get_expense_service() -> ExpenseService:
    return ExpenseService(model=Expense, property_model=Property)


async def get_cloudflare_service() -> CloudflareService:
    return CloudflareService(document_model=TenantDocument, tenant_model=Tenant)


async def get_document_service() -> DocumentService:
    cloudflare_service = await get_cloudflare_service()
    return DocumentService(
        cloudflare_service, model=TenantDocument, tenant_model=Tenant
    )
