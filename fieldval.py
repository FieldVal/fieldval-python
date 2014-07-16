class FVCheck(object):

    def __init__(self, **kwargs):
        self.new_value = None
        self.args = kwargs

    def assign_new_value(self, new_value):
        self.new_value = new_value

    def is_new_value_assigned(self):
        return self.new_value is not None

    def get_new_value(self):
        return self.new_value

    def check(self, value):
        raise NotImplementedError('check method needs to overridden')


class FieldVal(object):

    ONE_OR_MORE_ERRORS = 0
    FIELD_MISSING = 1
    INCORRECT_FIELD_TYPE = 2
    FIELD_UNRECOGNIZED = 3
    MULTIPLE_ERRORS = 4

    REQUIRED_ERROR = dict(error=FIELD_MISSING, error_message='Field is missing')
    NOT_REQUIRED_BUT_MISSING = "notrequired"

    def __init__(self, validating):
        self.validating = validating
        self.missing = {}
        self.invalid = {}
        self.unrecognized = {}
        self.recognized = []

    def add_to_unrecognized(self, key):
        self.unrecognized[key] = dict(error=FieldVal.FIELD_UNRECOGNIZED, error_message='Unrecognized field')

    def get(self, field_name, *checks):
        self.recognized.append(field_name)

        value = self.validating.get(field_name, None)

        for check in checks:
            error = check.check(value)
            if error is None:
                if check.is_new_value_assigned():
                    value = check.get_new_value()

            else:
                if error == FieldVal.REQUIRED_ERROR:
                    self.missing[field_name] = error
                    continue
                elif error == FieldVal.NOT_REQUIRED_BUT_MISSING:
                    break

                self.invalid[field_name] = error
                break

        return value

    def end(self):
        returning = dict()

        if self.validating:
            for key in self.validating.keys():
                if not key in self.recognized:
                    self.add_to_unrecognized(key)

        if self.missing:
            returning['missing'] = self.missing

        if self.invalid:
            returning['invalid'] = self.invalid

        if self.unrecognized:
            returning['unrecognized'] = self.unrecognized

        if returning:
            returning.update(dict(error=FieldVal.ONE_OR_MORE_ERRORS, error_message='One or more errors'))
            return returning

        return None
