from simple_validation import core


class StringValidator(core.FieldValidator):
    def clean(self, value):
        if isinstance(value, str):
            return value

        raise core.ValidationError("{} is not a string".format(value))


class IntegerValidator(core.FieldValidator):
    def clean(self, value):
        if isinstance(value, int):
            return value

        raise core.ValidationError("{} is not an integer".format(value))


class EmailValidator(StringValidator):
    def clean(self, value):
        value = super().clean(value)
        if '@' in value and '.' in value:
            return value

        raise core.ValidationError("{} is not a valid email!".format(value))


class RequiredValidator(core.FieldValidator):
    def clean(self, value):
        if value is not None:
            return value

        raise core.ValidationError("This field is required!")


class AlikeValidator(core.FieldValidator):
    def __init__(self, arg1, arg2):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2

    def clean(self, value):
        if self._get_object_attribute(value, self.arg1) == self._get_object_attribute(value, self.arg2):
            return value

        raise core.ValidationError("{} and {} are not alike".format(self.arg1, self.arg2))


class CapFirstValidator(core.FieldValidator):
    def clean(self, value):
        return value.capitalize()
