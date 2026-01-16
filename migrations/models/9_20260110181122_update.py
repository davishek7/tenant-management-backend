from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "utility_bills" DROP CONSTRAINT IF EXISTS "uid_utility_bil_tenant__f68199";
        ALTER TABLE "payments" DROP CONSTRAINT IF EXISTS "fk_payments_rent_led_e7ac016d";
        ALTER TABLE "expenses" ADD "user_id" UUID NOT NULL;
        ALTER TABLE "payments" ADD "user_id" UUID NOT NULL;
        ALTER TABLE "payments" ADD "property_id" UUID NOT NULL;
        ALTER TABLE "payments" ADD "unit_id" UUID NOT NULL;
        ALTER TABLE "payments" ADD "tenant_id" UUID NOT NULL;
        ALTER TABLE "payments" DROP COLUMN "ledger_id";
        ALTER TABLE "utility_bills" ADD "utility_type" VARCHAR(20) NOT NULL;
        ALTER TABLE "utility_bills" ADD "user_id" UUID NOT NULL;
        ALTER TABLE "utility_bills" ADD "period" DATE NOT NULL;
        ALTER TABLE "utility_bills" ADD "property_id" UUID NOT NULL;
        ALTER TABLE "utility_bills" ADD "unit_id" UUID NOT NULL;
        ALTER TABLE "utility_bills" DROP COLUMN "month";
        ALTER TABLE "utility_bills" DROP COLUMN "bill_type";
        ALTER TABLE "utility_bills" DROP COLUMN "is_paid";
        COMMENT ON COLUMN "utility_bills"."utility_type" IS 'ELECTRICITY: ELECTRICITY\nWATER: WATER\nGAS: GAS\nINTERNET: INTERNET\nMAINTENANCE: MAINTENANCE';
        ALTER TABLE "expenses" ADD CONSTRAINT "fk_expenses_users_0f8ffb9b" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
        CREATE INDEX IF NOT EXISTS "idx_expenses_user_id_2c15d3" ON "expenses" ("user_id");
        ALTER TABLE "payments" ADD CONSTRAINT "fk_payments_properti_792cea25" FOREIGN KEY ("property_id") REFERENCES "properties" ("id") ON DELETE CASCADE;
        ALTER TABLE "payments" ADD CONSTRAINT "fk_payments_units_8e9f9285" FOREIGN KEY ("unit_id") REFERENCES "units" ("id") ON DELETE CASCADE;
        ALTER TABLE "payments" ADD CONSTRAINT "fk_payments_users_5514215d" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
        ALTER TABLE "payments" ADD CONSTRAINT "fk_payments_tenants_e5693ac7" FOREIGN KEY ("tenant_id") REFERENCES "tenants" ("id") ON DELETE CASCADE;
        CREATE INDEX IF NOT EXISTS "idx_payments_user_id_e10631" ON "payments" ("user_id");
        CREATE INDEX IF NOT EXISTS "idx_payments_propert_c44d58" ON "payments" ("property_id");
        CREATE INDEX IF NOT EXISTS "idx_payments_unit_id_eb62a4" ON "payments" ("unit_id");
        CREATE INDEX IF NOT EXISTS "idx_payments_tenant__99230e" ON "payments" ("tenant_id");
        ALTER TABLE "utility_bills" ADD CONSTRAINT "fk_utility__properti_8ea11c6d" FOREIGN KEY ("property_id") REFERENCES "properties" ("id") ON DELETE CASCADE;
        ALTER TABLE "utility_bills" ADD CONSTRAINT "fk_utility__units_e70e6bb7" FOREIGN KEY ("unit_id") REFERENCES "units" ("id") ON DELETE CASCADE;
        ALTER TABLE "utility_bills" ADD CONSTRAINT "fk_utility__users_b4c6661b" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_utility_bil_tenant__90e057" ON "utility_bills" ("tenant_id", "utility_type", "period");
        CREATE INDEX IF NOT EXISTS "idx_utility_bil_user_id_64add0" ON "utility_bills" ("user_id");
        CREATE INDEX IF NOT EXISTS "idx_utility_bil_propert_c2eb33" ON "utility_bills" ("property_id");
        CREATE INDEX IF NOT EXISTS "idx_utility_bil_unit_id_18bbc1" ON "utility_bills" ("unit_id");
        CREATE INDEX IF NOT EXISTS "idx_utility_bil_tenant__4fd27a" ON "utility_bills" ("tenant_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_utility_bil_tenant__4fd27a";
        DROP INDEX IF EXISTS "idx_utility_bil_unit_id_18bbc1";
        DROP INDEX IF EXISTS "idx_utility_bil_propert_c2eb33";
        DROP INDEX IF EXISTS "idx_utility_bil_user_id_64add0";
        DROP INDEX IF EXISTS "uid_utility_bil_tenant__90e057";
        ALTER TABLE "utility_bills" DROP CONSTRAINT IF EXISTS "fk_utility__users_b4c6661b";
        ALTER TABLE "utility_bills" DROP CONSTRAINT IF EXISTS "fk_utility__units_e70e6bb7";
        ALTER TABLE "utility_bills" DROP CONSTRAINT IF EXISTS "fk_utility__properti_8ea11c6d";
        DROP INDEX IF EXISTS "idx_payments_tenant__99230e";
        DROP INDEX IF EXISTS "idx_payments_unit_id_eb62a4";
        DROP INDEX IF EXISTS "idx_payments_propert_c44d58";
        DROP INDEX IF EXISTS "idx_payments_user_id_e10631";
        ALTER TABLE "payments" DROP CONSTRAINT IF EXISTS "fk_payments_tenants_e5693ac7";
        ALTER TABLE "payments" DROP CONSTRAINT IF EXISTS "fk_payments_users_5514215d";
        ALTER TABLE "payments" DROP CONSTRAINT IF EXISTS "fk_payments_units_8e9f9285";
        ALTER TABLE "payments" DROP CONSTRAINT IF EXISTS "fk_payments_properti_792cea25";
        DROP INDEX IF EXISTS "idx_expenses_user_id_2c15d3";
        ALTER TABLE "expenses" DROP CONSTRAINT IF EXISTS "fk_expenses_users_0f8ffb9b";
        ALTER TABLE "expenses" DROP COLUMN "user_id";
        ALTER TABLE "payments" ADD "ledger_id" UUID NOT NULL;
        ALTER TABLE "payments" DROP COLUMN "user_id";
        ALTER TABLE "payments" DROP COLUMN "property_id";
        ALTER TABLE "payments" DROP COLUMN "unit_id";
        ALTER TABLE "payments" DROP COLUMN "tenant_id";
        ALTER TABLE "utility_bills" ADD "month" VARCHAR(7) NOT NULL;
        ALTER TABLE "utility_bills" ADD "bill_type" VARCHAR(20) NOT NULL;
        ALTER TABLE "utility_bills" ADD "is_paid" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "utility_bills" DROP COLUMN "utility_type";
        ALTER TABLE "utility_bills" DROP COLUMN "user_id";
        ALTER TABLE "utility_bills" DROP COLUMN "period";
        ALTER TABLE "utility_bills" DROP COLUMN "property_id";
        ALTER TABLE "utility_bills" DROP COLUMN "unit_id";
        ALTER TABLE "payments" ADD CONSTRAINT "fk_payments_rent_led_e7ac016d" FOREIGN KEY ("ledger_id") REFERENCES "rent_ledgers" ("id") ON DELETE CASCADE;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_utility_bil_tenant__f68199" ON "utility_bills" ("tenant_id", "bill_type", "month");"""


MODELS_STATE = (
    "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"
    "=="
)
