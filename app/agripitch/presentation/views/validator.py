from agripitch.utils import get_sub_criteria_item_by_label


def validate_not_empty(value):
    if value and not value.isspace():
        return True


def validate_file_extension(value):
    return True


class AgripitchValidator():

    def __init__(self) -> None:
        self.errors = {}
        self.error_messages = {
            'empty': {
                'error': 'This field should not be empty',
                'code': 'invalid'
            },
            'file_extension': {
                'error': 'The file extension is not valid',
                'code': 'invalid'
            },
        }

    def validate(self, form):
        form.pop('csrfmiddlewaretoken')
        for key, value in form.items():
            sub_criteria_item = get_sub_criteria_item_by_label(key)
            self.errors[key] = []
            for validator in sub_criteria_item.validators.all():
                if validator.validator.name == 'validate_not_empty':
                    if not validate_not_empty(value[0]):
                        self.errors[key].append(self.error_messages['empty'])
            if validator.validator.name == 'validate_file_extension':
                if not validate_file_extension(value[0]):
                    self.errors[key].append(
                        self.error_messages['file_extension'])
