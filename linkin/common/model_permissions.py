from abc import abstractmethod, ABCMeta
from django.db import models


class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class ModelPermissions(models.Model, metaclass=AbstractModelMeta):

    class Meta:
        abstract = True

    @abstractmethod
    def is_owner(self, user):
        pass
