from tortoise.models import Model
from tortoise import fields

from enum import IntEnum


class StatusEnum(IntEnum):
    pass


class TestResult(Model):
    class Meta:
        table = 'results'
        unique_together = ("definition", "stream")

    definition = fields.ForeignKeyField('models.TestDefinition')
    stream = fields.ForeignKeyField('models.DevelopmentStream')
    status = fields.IntEnumField(StatusEnum)


class SourceCodeFile(Model):
    class Meta:
        table = 'file'

    path = fields.TextField()
    results = fields.ManyToManyField('models.TestResult', related_name='files', through='file_result')
