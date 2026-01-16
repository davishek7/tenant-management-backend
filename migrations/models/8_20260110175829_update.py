from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "rent_ledgers" DROP CONSTRAINT IF EXISTS "uid_rent_ledger_tenant__0ad0e7";
        ALTER TABLE "payments" ALTER COLUMN "payment_mode" TYPE VARCHAR(20) USING "payment_mode"::VARCHAR(20);
        COMMENT ON COLUMN "payments"."payment_mode" IS 'CASH: CASH
UPI: UPI
BANK: BANK';
        ALTER TABLE "rent_ledgers" ADD "period" DATE NOT NULL;
        ALTER TABLE "rent_ledgers" ADD "unit_id" UUID NOT NULL;
        ALTER TABLE "rent_ledgers" RENAME COLUMN "rent_amount" TO "balance";
        ALTER TABLE "rent_ledgers" ADD "reference_id" UUID;
        ALTER TABLE "rent_ledgers" ADD "property_id" UUID NOT NULL;
        ALTER TABLE "rent_ledgers" ADD "user_id" UUID NOT NULL;
        ALTER TABLE "rent_ledgers" ADD "entry_type" VARCHAR(20) NOT NULL;
        ALTER TABLE "rent_ledgers" ADD "amount" DECIMAL(10,2) NOT NULL;
        ALTER TABLE "rent_ledgers" DROP COLUMN "paid_amount";
        ALTER TABLE "rent_ledgers" DROP COLUMN "is_closed";
        ALTER TABLE "rent_ledgers" DROP COLUMN "month";
        COMMENT ON COLUMN "rent_ledgers"."entry_type" IS 'RENT: RENT\nPAYMENT: PAYMENT\nUTILITY: UTILITY\nADJUSTMENT: ADJUSTMENT';
        ALTER TABLE "rent_ledgers" ADD CONSTRAINT "fk_rent_led_properti_53cd2ecf" FOREIGN KEY ("property_id") REFERENCES "properties" ("id") ON DELETE CASCADE;
        ALTER TABLE "rent_ledgers" ADD CONSTRAINT "fk_rent_led_users_9029fe45" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
        ALTER TABLE "rent_ledgers" ADD CONSTRAINT "fk_rent_led_units_a884ecb7" FOREIGN KEY ("unit_id") REFERENCES "units" ("id") ON DELETE CASCADE;
        CREATE INDEX IF NOT EXISTS "idx_rent_ledger_tenant__b04388" ON "rent_ledgers" ("tenant_id", "entry_type");
        CREATE INDEX IF NOT EXISTS "idx_rent_ledger_tenant__9a7b3f" ON "rent_ledgers" ("tenant_id", "period");
        CREATE INDEX IF NOT EXISTS "idx_rent_ledger_unit_id_4b6fdb" ON "rent_ledgers" ("unit_id");
        CREATE INDEX IF NOT EXISTS "idx_rent_ledger_propert_fb5479" ON "rent_ledgers" ("property_id");
        CREATE INDEX IF NOT EXISTS "idx_rent_ledger_user_id_4104d9" ON "rent_ledgers" ("user_id");
        CREATE INDEX IF NOT EXISTS "idx_rent_ledger_tenant__4d3e31" ON "rent_ledgers" ("tenant_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "idx_rent_ledger_tenant__4d3e31";
        DROP INDEX IF EXISTS "idx_rent_ledger_user_id_4104d9";
        DROP INDEX IF EXISTS "idx_rent_ledger_propert_fb5479";
        DROP INDEX IF EXISTS "idx_rent_ledger_unit_id_4b6fdb";
        DROP INDEX IF EXISTS "idx_rent_ledger_tenant__9a7b3f";
        DROP INDEX IF EXISTS "idx_rent_ledger_tenant__b04388";
        ALTER TABLE "rent_ledgers" DROP CONSTRAINT IF EXISTS "fk_rent_led_units_a884ecb7";
        ALTER TABLE "rent_ledgers" DROP CONSTRAINT IF EXISTS "fk_rent_led_users_9029fe45";
        ALTER TABLE "rent_ledgers" DROP CONSTRAINT IF EXISTS "fk_rent_led_properti_53cd2ecf";
        ALTER TABLE "payments" ALTER COLUMN "payment_mode" TYPE VARCHAR(20) USING "payment_mode"::VARCHAR(20);
        COMMENT ON COLUMN "payments"."payment_mode" IS NULL;
        ALTER TABLE "rent_ledgers" ADD "paid_amount" DECIMAL(10,2) NOT NULL DEFAULT 0;
        ALTER TABLE "rent_ledgers" ADD "is_closed" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "rent_ledgers" RENAME COLUMN "balance" TO "rent_amount";
        ALTER TABLE "rent_ledgers" ADD "month" VARCHAR(7) NOT NULL;
        ALTER TABLE "rent_ledgers" DROP COLUMN "period";
        ALTER TABLE "rent_ledgers" DROP COLUMN "unit_id";
        ALTER TABLE "rent_ledgers" DROP COLUMN "reference_id";
        ALTER TABLE "rent_ledgers" DROP COLUMN "property_id";
        ALTER TABLE "rent_ledgers" DROP COLUMN "user_id";
        ALTER TABLE "rent_ledgers" DROP COLUMN "entry_type";
        ALTER TABLE "rent_ledgers" DROP COLUMN "amount";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_rent_ledger_tenant__0ad0e7" ON "rent_ledgers" ("tenant_id", "month");"""


MODELS_STATE = (
    "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"
    "7eVvL0//A7yqvR4="
)
