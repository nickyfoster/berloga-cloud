from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    role = fields.CharField(max_length=20, null=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    ssh_key = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Servers(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=225)
    type = fields.CharField(max_length=225)
    public_ip = fields.CharField(max_length=20, null=True)
    image = fields.CharField(max_length=20, null=True)
    ssh_key = fields.TextField(null=True)
    creator = fields.ForeignKeyField("models.Users", related_name="server")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    status = fields.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.name}, {self.creator_id} on {self.created_at}"


