from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "payments" ADD "reversed_on" TIMESTAMPTZ;
        ALTER TABLE "payments" ADD "is_reversed" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "payments" DROP COLUMN "reversed_on";
        ALTER TABLE "payments" DROP COLUMN "is_reversed";"""


MODELS_STATE = (
    "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"
    "uaXqBXLcaj/tfLz/8BpYcifQ=="
)
