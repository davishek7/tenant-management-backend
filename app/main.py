from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.lifespan import lifespan
from app.core.settings import settings
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.property import router as property_router
from app.routes.unit import router as unit_router
from app.routes.tenant import router as tenant_router
from app.routes.rent_ledger import router as rent_ledger_router
from app.routes.payment import router as payment_router
from app.routes.utility import router as utility_router
from app.routes.adjustment import router as adjustment_router
from app.routes.document import router as document_router
from app.routes.expense import router as expense_router
from app.exceptions.handlers import register_exception_handlers


app = FastAPI(
    title=settings.APP_NAME,
    description="These are REST APIs for Tenant Managment App.",
    version="1.0.0",
    contact={
        "name": "Avishek Das",
        "email": "davishek7@gmail.com",
    },
    lifespan=lifespan,
)

origins = [settings.FRONTEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app=app)


URL_PREFIX = "/api"

app.include_router(auth_router, prefix=f"{URL_PREFIX}/auth", tags=["Auth"])
app.include_router(property_router, prefix=f"{URL_PREFIX}/property", tags=["Property"])
app.include_router(unit_router, prefix=f"{URL_PREFIX}", tags=["Unit"])
app.include_router(tenant_router, prefix=f"{URL_PREFIX}", tags=["Tenant"])
app.include_router(
    rent_ledger_router, prefix=f"{URL_PREFIX}/rent-ledger", tags=["Rent Ledger"]
)
app.include_router(payment_router, prefix=f"{URL_PREFIX}", tags=["Payment"])
app.include_router(utility_router, prefix=f"{URL_PREFIX}", tags=["Utility Bill"])
app.include_router(adjustment_router, prefix=f"{URL_PREFIX}", tags=["Adjustment"])
app.include_router(document_router, prefix=f"{URL_PREFIX}", tags=["Tenant Documents"])
app.include_router(expense_router, prefix=f"{URL_PREFIX}", tags=["Expense"])
app.include_router(user_router, prefix=f"{URL_PREFIX}/user", tags=["User"])
