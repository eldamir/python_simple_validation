from simple_validation import core, library


class TwoEmailsValidator(core.Validator):
    email1 = [
        library.RequiredValidator(),
        library.EmailValidator(),
    ]
    email2 = [
        library.RequiredValidator(),
        library.EmailValidator(),
    ]
    _all_ = library.AlikeValidator('email1', 'email2')


class CappedEmailValidator(core.Validator):
    email = [
        library.RequiredValidator(),
        library.EmailValidator(),
        library.CapFirstValidator(),
    ]


class Foo(object):
    bar = "foobar"
    baz = 1337


class FooValidator(core.Validator):
    bar = library.StringValidator()
    baz = library.IntegerValidator()


class TestFieldValidator:
    def test_does_nothing(self):
        value = "Foobar"
        validator = core.FieldValidator()
        assert validator.clean(value) == value


class TestValidator:
    def test_gathers_errors(self):
        bad_value = "example.com"
        good_value = "john@example.com"

        # Test a validator with incorrect data
        email_val = TwoEmailsValidator()
        valid = email_val.clean({
            'email1': bad_value,
            'email2': good_value
        })

        assert not valid, "Validator unexpectedly returned True"
        assert email_val.errors['email1'] == "example.com is not a valid email!"
        assert email_val.errors['_all_'] == "email1 and email2 are not alike"

    def test_cleans_values(self):
        good_value = "john@example.com"
        # Test a validator with correct data
        email_val = CappedEmailValidator()
        valid = email_val.clean({
            'email': good_value
        })

        assert valid
        assert email_val.values['email'] == "John@example.com"

    def test_can_clean_non_dict_object(self):
        obj = Foo()
        validator = FooValidator()
        assert validator.clean(obj)
