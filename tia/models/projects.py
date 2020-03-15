from tortoise.models import Model
from tortoise import fields


class Project(Model):
    class Meta:
        table = 'projects'

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)


class DevelopmentStream(Model):
    class Meta:
        table = 'devstreams'

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    project = fields.ForeignKeyField('models.Project', related_name='streams')
    base_stream = fields.ForeignKeyField('models.DevelopmentStream', related_name='derived_branches', null=True)
