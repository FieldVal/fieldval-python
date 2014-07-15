from fieldval import FVCheck, FieldVal

__author__ = 'stan'


class String(FVCheck):

    @staticmethod
    def is_string(value):
        return type(value) in [unicode, str]

    def check(self, value):
        if not String.is_string(value):
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')


class Integer(FVCheck):

    @staticmethod
    def is_int(value):
        return type(value) == int

    def check(self, value):
        parse = self.args.get('parse', False)

        if Integer.is_int(value):
            return

        if not parse:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')

        try:
            self.assign_new_value(int(value))
        except:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')
