from tortoise.models import Model
from tortoise import fields


class TestCoverage(Model):
    class Meta:
        table = 'coverage'
        unique_together = ('definition', 'stream', 'source_file')

    definition = fields.ForeignKeyField('models.TestDefinition')
    stream = fields.ForeignKeyField('models.DevelopmentStream')
    source_file = fields.ForeignKeyField('models.SourceCodeFile')


class SourceCodeFile(Model):
    class Meta:
        table = 'file'

    path = fields.TextField()
