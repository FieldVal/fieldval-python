class FVCheck(object):

    def __init__(self, required=True, stop_on_error=True, **kwargs):
        self.required = required
        self.stop_on_error = stop_on_error
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

    REQUIRED_ERROR = "required"
    NOT_REQUIRED_BUT_MISSING = "notrequired"

    ONE_OR_MORE_ERRORS = 0
    FIELD_MISSING = 1
    INCORRECT_FIELD_TYPE = 2
    FIELD_UNRECOGNIZED = 3
    MULTIPLE_ERRORS = 4

    def __init__(self, validating):
        self.validating = validating
        self.missing = {}
        self.invalid = {}
        self.unrecognized = {}
        self.recognized = []

    def add_to_unrecognized(self, key):
        self.unrecognized[key] = dict(error=FieldVal.FIELD_UNRECOGNIZED, error_message='Unrecognized filed')

    def add_to_missing(self, key):
        self.missing[key] = dict(error=FieldVal.FIELD_MISSING, error_message='Field is missing')

    def get(self, field_name, *checks):
        self.recognized.append(field_name)

        if field_name not in self.validating:
            self.add_to_missing(field_name)
            return

        value = self.validating[field_name]

        for check in checks:
            error = check.check(value)

            if error is None:
                if check.is_new_value_assigned():
                    value = check.get_new_value()

            else:
                self.invalid[field_name] = error
                break

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
