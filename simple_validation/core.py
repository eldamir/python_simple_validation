class ValidationError(ValueError):
    def __init__(self, message):
        self.message = message


class ObjectGetterMixin(object):
    def _get_object_attribute(self, obj, name):
        if isinstance(obj, dict):
            return obj.get(name)
        else:
            return getattr(obj, name)


class FieldValidator(ObjectGetterMixin):
    def __init__(self):
        pass

    def clean(self, value):
        return value


class Validator(ObjectGetterMixin):
    def __init__(self):
        self.errors = {}
        self.values = {}

    def _fields(self):
        for name in dir(self):
            field = getattr(self, name)
            if not isinstance(field, list):
                _fields = [field]
            else:
                _fields = field

            for f in _fields:
                if not isinstance(f, FieldValidator):
                    break
            else:
                yield name, _fields

    def clean(self, obj):
        self.errors = {}
        self.values = {}
        for name, validators in self._fields():
            try:
                if name == '_all_':
                    value = obj
                else:
                    value = self._get_object_attribute(obj, name)
                self.values[name] = value
                for validator in validators:
                    self.values[name] = validator.clean(self.values[name])
            except ValidationError as e:
                self.errors[name] = e.message
        return not self.errors
