from fieldval import FVCheck, FieldVal

__author__ = 'stan'


class TypeFVCheck(FVCheck):
    
    def check(self, value):
        if value is None:
            required = self.args.get('required', True)
            if required:
                return FieldVal.REQUIRED_ERROR
            else:
                return FieldVal.NOT_REQUIRED_BUT_MISSING

        return self.type_check(value)
    
    def type_check(self, value):
        raise NotImplementedError('check method needs to overridden')


class String(TypeFVCheck):

    def type_check(self, value):
        if type(value) not in [str, unicode]:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')


class Boolean(TypeFVCheck):

    def type_check(self, value):
        parse = self.args.get('parse', False)

        if type(value) == bool:
            return

        if not parse:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')

        try:
            self.assign_new_value(bool(value))
        except:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')


class Integer(TypeFVCheck):

    @staticmethod
    def is_int(value):
        return type(value) == int

    def type_check(self, value):
        parse = self.args.get('parse', False)

        if Integer.is_int(value):
            return

        if not parse:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')

        try:
            self.assign_new_value(int(value))
        except:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')


class Float(TypeFVCheck):

    def type_check(self, value):
        parse = self.args.get('parse', False)

        if type(value) == float:
            return

        if not parse:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')

        try:
            self.assign_new_value(float(value))
        except:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')


class List(TypeFVCheck):

    def type_check(self, value):
        if type(value) != list:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')


class Dict(TypeFVCheck):

    def type_check(self, value):
        if type(value) != dict:
            return dict(error=FieldVal.INCORRECT_FIELD_TYPE, error_message='Incorrect field type')
