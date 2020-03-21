from tortoise.models import Model
from tortoise import fields


class TestDefinition(Model):
    class Meta:
        table = 'definition'

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    streams = fields.ManyToManyField('models.DevelopmentStream', related_name='tests', through='definition_stream')


class Metadata(Model):
    class Meta:
        table = 'metadata'
        unique_together = ('key', 'definition', 'stream')

    key = fields.CharField(max_length=255)
    value = fields.TextField()
    inherit = fields.BooleanField(default=True)
    definition = fields.ForeignKeyField('models.TestDefinition')
    stream = fields.ForeignKeyField('models.DevelopmentStream')
