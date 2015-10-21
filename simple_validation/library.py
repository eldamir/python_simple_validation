
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



class EmailValidator(FieldValidator):
    def clean(self, value):
        if isinstance(value, str) and '@' in value and '.' in value:
            return value

        raise ValidationError("Not a valid email!")


class RequiredValidator(FieldValidator):
    def clean(self, value):
        if value is not None:
            return value

        raise ValidationError("This field is required!")


class AlikeValidator(FieldValidator):
    def __init__(self, arg1, arg2):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2

    def clean(self, value):
        if self._get_object_attribute(value, self.arg1) == self._get_object_attribute(value, self.arg2):
            return value

        raise ValidationError("Values not alike")


class CapFirstValidator(FieldValidator):
    def clean(self, value):
        return value.capitalize()


class TwoEmailsValidator(Validator):
    email1 = [
        RequiredValidator(),
        EmailValidator(),
    ]
    email2 = [
        RequiredValidator(),
        EmailValidator(),
    ]
    _all_ = AlikeValidator('email1', 'email2')

class CappedEmailValidator(Validator):
    email = [
        RequiredValidator(),
        EmailValidator(),
        CapFirstValidator(),
    ]



if __name__ == '__main__':
    bad_value = "example.com"
    good_value = "john@example.com"

    # Test a field validator
    validator = EmailValidator()

    assert validator.clean(good_value)
    try:
        validator.clean(bad_value)
        assert False, "Exception not raised"
    except ValidationError:
        assert True

    # Test a validator with incorrect data
    email_val = TwoEmailsValidator()
    valid = email_val.clean({
        'email1': bad_value,
        'email2': good_value
    })

    assert not valid, "Validator unexpectedly returned True"
    assert email_val.errors['email1'] == "Not a valid email!"
    assert email_val.errors['_all_'] == "Values not alike"

    # Test a validator with correct data
    email_val = CappedEmailValidator()
    valid = email_val.clean({
        'email': good_value
    })

    assert valid
    assert email_val.values['email'] == "John@example.com"
