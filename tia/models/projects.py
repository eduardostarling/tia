from tortoise.models import Model
from tortoise import fields


class Project(Model):
    class Meta:
        table = 'project'

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)


class DevelopmentStream(Model):
    class Meta:
        table = 'devstream'

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    project = fields.ForeignKeyField('models.Project', related_name='streams')
    base_stream = fields.ForeignKeyField('models.DevelopmentStream', related_name='derived_branches', null=True)
