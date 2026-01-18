from tortoise import fields
from tortoise.models import Model


class RefreshToken(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="refresh_tokens")
    revoked = fields.BooleanField(default=False)
    expires_at = fields.DatetimeField()

    class Meta:
        table = "refresh_tokens"
