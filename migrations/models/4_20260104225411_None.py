from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "phone" VARCHAR(15) NOT NULL UNIQUE,
    "email" VARCHAR(255),
    "is_active" BOOL NOT NULL DEFAULT True
);
CREATE TABLE IF NOT EXISTS "properties" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "address" TEXT NOT NULL,
    "owner_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "expenses" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(100) NOT NULL,
    "amount" DECIMAL(10,2) NOT NULL,
    "expense_date" DATE NOT NULL,
    "remarks" TEXT,
    "property_id" UUID NOT NULL REFERENCES "properties" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "units" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "unit_number" VARCHAR(50) NOT NULL,
    "monthly_rent" DECIMAL(10,2) NOT NULL,
    "is_occupied" BOOL NOT NULL DEFAULT False,
    "property_id" UUID NOT NULL REFERENCES "properties" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_units_propert_680ca0" UNIQUE ("property_id", "unit_number")
);
CREATE TABLE IF NOT EXISTS "tenants" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL,
    "phone" VARCHAR(15) NOT NULL,
    "move_in_date" DATE NOT NULL,
    "deposit_amount" DECIMAL(10,2) NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "unit_id" UUID NOT NULL UNIQUE REFERENCES "units" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "rent_ledgers" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "month" VARCHAR(7) NOT NULL,
    "rent_amount" DECIMAL(10,2) NOT NULL,
    "paid_amount" DECIMAL(10,2) NOT NULL DEFAULT 0,
    "is_closed" BOOL NOT NULL DEFAULT False,
    "tenant_id" UUID NOT NULL REFERENCES "tenants" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_rent_ledger_tenant__0ad0e7" UNIQUE ("tenant_id", "month")
);
CREATE TABLE IF NOT EXISTS "payments" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "amount" DECIMAL(10,2) NOT NULL,
    "payment_mode" VARCHAR(20) NOT NULL,
    "paid_on" DATE NOT NULL,
    "ledger_id" UUID NOT NULL REFERENCES "rent_ledgers" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tenant_documents" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "doc_type" VARCHAR(50) NOT NULL,
    "file_url" TEXT NOT NULL,
    "tenant_id" UUID NOT NULL REFERENCES "tenants" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "utility_bills" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "bill_type" VARCHAR(20) NOT NULL,
    "month" VARCHAR(7) NOT NULL,
    "amount" DECIMAL(10,2) NOT NULL,
    "is_paid" BOOL NOT NULL DEFAULT False,
    "tenant_id" UUID NOT NULL REFERENCES "tenants" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_utility_bil_tenant__f68199" UNIQUE ("tenant_id", "bill_type", "month")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "DfLbC9JzmR1gVC6wuvvHy9N/ysYPVA=="
)
