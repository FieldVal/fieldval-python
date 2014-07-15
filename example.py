import bval
from fieldval import FieldVal, FVCheck

#Missing and unrecognized
validating = dict(unrecognized_field='123')
validator = FieldVal(validating)
validator.get('missing_field', bval.String())
print validator.end()

#Incorrect type
validating = dict(test='123')
validator = FieldVal(validating)
validator.get('test', bval.Integer())
print validator.end()

#String validation
validating = dict(test='123')
validator = FieldVal(validating)
validator.get('test', bval.String())
print validator.end()


#Integer validation
validating = dict(test=123)
validator = FieldVal(validating)
validator.get('test', bval.Integer())
print validator.end()


#Integer validation with parsing
validating = dict(test='123')
validator = FieldVal(validating)
validator.get('test', bval.Integer(parse=True))
print validator.end()


#Custom check
class SortedNumbers(FVCheck):

    def check(self, numbers):
        ascending = self.args.get('ascending', True)

        for i in range(1, len(numbers)):
            if ascending:
                if numbers[i] < numbers[i-1]:
                    return dict(error=1234, error_message='Numbers are not in the right order!')
            else:
                if numbers[i] > numbers[i-1]:
                    return dict(error=1234, error_message='Numbers are not in the right order!')


class ListOfIntegers(FVCheck):

    def check(self, value):
        numbers_str = value.split(' ')
        numbers = []

        for number_str in numbers_str:
            try:
                number = int(number_str)
            except:
                return dict(error=1234, error_message='Numbers are invalid!')

            numbers.append(number)

        self.assign_new_value(numbers)


validating = dict(test='1 2 3 4 5 6 7 8 9 10')
validator = FieldVal(validating)
validator.get('test', bval.String(), ListOfIntegers(), SortedNumbers(ascending=True))
print validator.end()


validating = dict(test='5 4 3 2 1')
validator = FieldVal(validating)
validator.get('test', bval.String(), ListOfIntegers(), SortedNumbers(ascending=False))
print validator.end()


validating = dict(test='1 3 2')
validator = FieldVal(validating)
validator.get('test', bval.String(), ListOfIntegers(), SortedNumbers(ascending=True))
print validator.end()


validating = dict(test=[1, 2, 3])
validator = FieldVal(validating)
validator.get('test', bval.String(), ListOfIntegers(), SortedNumbers(ascending=True))
print validator.end()
