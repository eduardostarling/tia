from sqlalchemy import Column, Integer, String, ForeignKey

from tia.models.base import Base


class TestDefinition(Base):
    __tablename__ = 'definitions'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=256))


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=256))


class DevelopmentStream(Base):
    __tablename__ = 'devstreams'
    id = Column(Integer, primary_key=True)
    project = ForeignKey('projects.id')
    branch = Column(String(length=256))
    base_branch = ForeignKey('devstreams.id')
    commit = Column(String(length=256))


class TestResult(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    definition = ForeignKey('definitions.id')
    stream = ForeignKey('devstreams.id')
    status = Column(Integer)
