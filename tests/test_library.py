from simple_validation import library, core


class TestStringValidator:
    def test_raises_exception(self):
        value = 1337
        validator = library.StringValidator()

        try:
            validator.clean(value)
            assert False, "Exception not raised"
        except core.ValidationError:
            assert True

    def test_cleans_value(self):
        value = "example"
        validator = library.StringValidator()
        assert validator.clean(value) == value


class TestIntegerValidator:
    def test_raises_exception(self):
        value = "example"
        validator = library.IntegerValidator()

        try:
            validator.clean(value)
            assert False, "Exception not raised"
        except core.ValidationError:
            assert True

    def test_cleans_value(self):
        value = 1337
        validator = library.IntegerValidator()
        assert validator.clean(value) == value


class TestEmailValidator:
    def test_raises_exception(self):
        bad_values = [
            "example.com",
            1337,
        ]
        validator = library.EmailValidator()
        for value in bad_values:
            try:
                validator.clean(value)
                assert False, "Exception not raised"
            except core.ValidationError:
                assert True

    def test_cleans_value(self):
        email = "john@example.com"
        validator = library.EmailValidator()
        assert validator.clean(email) == email


class TestRequiredValidator:
    def test_raises_exception(self):
        value = None
        validator = library.RequiredValidator()

        try:
            validator.clean(value)
            assert False, "Exception not raised"
        except core.ValidationError:
            assert True

    def test_cleans_value(self):
        email = "john@example.com"
        validator = library.RequiredValidator()
        assert validator.clean(email) == email


class TestAlikeValidator:
    def test_raises_exception(self):
        value1 = "Foo"
        value2 = "Bar"
        validator = library.AlikeValidator('value1', 'value2')

        try:
            validator.clean(locals())
            assert False, "Exception not raised"
        except core.ValidationError:
            assert True

    def test_cleans_value(self):
        value1 = "Foo"
        value2 = "Foo"
        validator = library.AlikeValidator('value1', 'value2')
        assert validator.clean(locals())
