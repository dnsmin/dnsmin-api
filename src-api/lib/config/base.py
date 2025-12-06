import types

from pydantic import BaseModel as PydanticBaseModel


class BaseConfig(PydanticBaseModel):
    """This provides an abstract base class for all configuration related models to inherit from."""

    def __init__(self, **kwargs):
        import inspect

        for key, field in self.__class__.model_fields.items():
            if key in kwargs:
                continue

            if inspect.isclass(field.annotation):
                if type(field.annotation) is types.GenericAlias:
                    kwargs[key] = field.annotation()

                elif issubclass(field.annotation, BaseConfig):
                    kwargs[key] = field.annotation()

        super().__init__(**kwargs)
