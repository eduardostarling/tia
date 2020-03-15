from tortoise.models import Model
from tortoise import fields


class TestDefinition(Model):
    class Meta:
        table = 'definitions'

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    streams = fields.ManyToManyField('models.DevelopmentStream', related_name='tests', through='definition_stream')
