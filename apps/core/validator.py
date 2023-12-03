import re
from datetime import datetime


class Validator:
    valid_validation = [
        'required',
        'nullable',
        'email',
        'phone',
        'password',
        'username',
        'datetime',
        'date',
        'time',
        'number',
        'int',
        'integer',
        'string',
        'list',
        'include_params:?',
        'boolean',
        'bool',
        'in:?',
        'regex:?',
        'date_format:?',
        'file',
        'min:?',
        'max:?',
        'image'
    ]

    is_valid = True
    errors = {}

    def __init__(self, request, task):
        if request.method == 'GET':
            self.data = request.GET
        else:
            self.data = request.data

        self.task = task
        self.errors = {}
        self.is_valid = True
        self.validate()

    def push_error(self, key, message):
        if key in self.errors:
            self.errors[key].append(message)
        else:
            self.errors[key] = [message]

    def is_failed(self):
        return not self.is_valid

    def validate(self):
        for key, value in self.task.items():
            value = value if isinstance(value, list) else value.split('|')

            for segment in value:
                v = segment.split(':')
                v = v[0] if len(v) == 1 else v[0] + ':?'
                if v not in self.valid_validation:
                    raise Exception(f"{v} is not a valid validator")

                elif v == 'required':
                    if key not in self.data:
                        self.push_error(key, f"'{key.replace('_', ' ').title()}' field is required")
                    else:
                        if self.data[key] == None or self.data[key] == '':
                            self.push_error(key, f"'{key.replace('_', ' ').title()}' field is required")

                elif v == 'email':
                    if key in self.data:
                        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.data[key]):
                            self.push_error(key, 'Enter a valid email address.')

                elif v == 'password':
                    if key in self.data:
                        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', self.data[key]):
                            self.push_error(
                                key, 'Password must be at least 8 characters, contain at least one letter' \
                                     ' and one number.')

                elif v == 'username':
                    if key in self.data:
                        if not re.match(r'^[a-zA-Z0-9_.-]+$', self.data[key]):
                            self.push_error(key, 'Enter a valid username. Only letters, numbers, and ' \
                                                 'the following characters are allowed: . _ -')

                elif v == 'datetime':
                    if key in self.data:
                        try:
                            datetime.strptime(self.data[key], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            self.push_error(key, f"Enter a valid datetime for '{key.replace('_', ' ').title()}'")

                elif v == 'date':
                    if key in self.data:
                        try:
                            datetime.strptime(self.data[key], '%Y-%m-%d')
                        except ValueError:
                            self.push_error(key, f"Enter a valid date for '{key.replace('_', ' ').title()}'")

                elif v == 'time':
                    if key in self.data:
                        try:
                            datetime.strptime(self.data[key], '%H:%M:%S')
                        except ValueError:
                            self.push_error(key, f"Enter a valid time for '{key.replace('_', ' ').title()}'")

                elif v == 'number' or v == 'int' or v == 'integer':
                    if key in self.data:
                        if not isinstance(self.data[key], int):
                            self.push_error(key, f"Enter a valid number for '{key.replace('_', ' ').title()}'")

                elif v == 'string':
                    if key in self.data:
                        if not isinstance(self.data[key], str):
                            self.push_error(key, f"Enter a valid string for '{key.replace('_', ' ').title()}'")

                elif v == 'list':
                    if key in self.data:
                        if not isinstance(self.data[key], list):
                            self.push_error(key, f"Enter a valid list of '{key.replace('_', ' ').title()}'")

                elif v == 'list:int':
                    if key in self.data:
                        if not isinstance(self.data[key], list):
                            self.push_error(key, f"Enter a valid list for '{key.replace('_', ' ').title()}'")
                        else:
                            for i in self.data[key]:
                                if not isinstance(i, int):
                                    self.push_error(key, f"Enter a valid list of '{key.replace('_', ' ').title()}'")
                                    break

                elif v == 'list:str':
                    if key in self.data:
                        if not isinstance(self.data[key], list):
                            self.push_error(key, f"Enter a valid list for '{key.replace('_', ' ').title()}'")
                        else:
                            for i in self.data[key]:
                                if not isinstance(i, str):
                                    self.push_error(key, f"Enter a valid list for '{key.replace('_', ' ').title()}'")
                                    break

                elif v == 'list:float':
                    if key in self.data:
                        if not isinstance(self.data[key], list):
                            self.push_error(key, 'Enter a valid list.')
                        else:
                            for i in self.data[key]:
                                if not isinstance(i, float):
                                    self.push_error(key, f"Enter a valid list for '{key.replace('_', ' ').title()}'")
                                    break

                elif v == 'include_params:?':
                    includers = (segment.split(":")).split(',')

                    for k in includers:
                        if k not in self.data:
                            self.push_error(key, f"{k} is required")

                elif v == 'bool' or v == 'boolean':
                    if key in self.data:
                        if not isinstance(self.data[key], bool):
                            self.push_error(key, f"Enter a valid boolean for '{key.replace('_', ' ').title()}'")

                elif v == 'in:?':
                    if key in self.data:
                        data_list = segment.split(':')[1].split(',')
                        if self.data[key] not in data_list:
                            self.push_error(key, f"'{key.replace('_', ' ').title()}' must be one of {data_list}")

                elif v == 'regex:?':
                    if key in self.data:
                        if not re.match(segment.split(':')[1], self.data[key]):
                            self.push_error(key, f"'{key.replace('_', ' ').title()}' is not valid")

                elif v == 'date_format:?':
                    if key in self.data:
                        try:
                            datetime.strptime(self.data[key], segment.split(':')[1])
                        except ValueError:
                            self.push_error(key, f"Enter a valid date for '{key.replace('_', ' ').title()}'")

                elif v == 'file':
                    if key in self.data:
                        if 'mimetype' in segment:
                            if self.data[key].mimetype not in segment.split(':')[1].split(','):
                                self.push_error(key, f"'{key.replace('_', ' ').title()}' is not a valid file")

                elif v == 'min:?':
                    if key in self.data:
                        if len(self.data[key]) < int(segment.split(':')[1]):
                            self.push_error(key,
                                            f"'{key.replace('_', ' ').title()}' must be greater than {segment.split(':')[1]} characters")

                elif v == 'max:?':
                    if key in self.data:
                        if len(self.data[key]) > int(segment.split(':')[1]):
                            self.push_error(key,
                                            f"'{key.replace('_', ' ').title()}' must be less than {segment.split(':')[1]} characters")

                elif v == 'image':
                    if key in self.data:
                        if 'mimetype' in segment:
                            if self.data[key].mimetype not in segment.split(':')[1].split(','):
                                self.push_error(key, f"'{key.replace('_', ' ').title()}' is not a valid image")

        self.is_valid = False if self.errors else True
