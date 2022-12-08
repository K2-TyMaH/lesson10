from collections import UserDict


class AddressBook(UserDict):

    def add_record(self, name, *args):
        new_user = Record(name, args)
        self.data[new_user.name.value] = new_user.phones

class Field:
    pass

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, phone):
        self.phone = phone

class Record:

    def __init__(self, name, *args):
        self.name = Name(name)
        for item in args:
            self.add_phone(item)
        #return self.name, self.phones

    def add_phone(self, phone):
        self.phones = []
        phone = Phone(phone)
        self.phones.append(phone.phone)

    def change_phone(self):
        pass

    def remove_phone(self):
        pass

        # if self.phones:
        #     showing = dict(enumerate(self.phones, 1))
        #     print(f'What phone you want to remove? {showing}')
        #     choosing = int(input('Choose № of this phone >>>'))
        #     self.phones.remove(showing[choosing])
        #     print(f'{showing[choosing]} removed')
        # else:
        #     print('Phones list is empty')

        # if phone_to_remove in self.phones:
        #     self.phones.remove(phone_to_remove)
        # else:
        #     print(f'I didn\'t find {phone_to_remove}')


USERS = AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it exists already'
        except TypeError:
            return 'Unknown command or parameters, please try again.'
    return inner


@input_error
def add_user(args):
    name, *phones = args
    USERS.add_record(name, phones)
    return f"User {name} added"

def remove_phone(args):
    pass

@input_error
def change_phone(args):
    name, *phones = args
    old_phones = USERS.data[name]
    USERS.add_record(name, phones)
    return f"User {name} have a new phone numbers {phones}, old was: {old_phones}"

@input_error
def show_number(args):
    user = args[0]
    phones = USERS.data[user]
    return f"{user}: {phones}"

def show_all(_):
    result = ""
    for name, phones in USERS.data.items():
        result += f"{name}: {phones}\n"
    return result

def hello(_):
    return "How can I help you?"


HANDLERS = {
    "hello": hello,
    "add": add_user,
    "change": change_phone,
    "show": show_all,
    "phone": show_number,
}

EXIT_COMMANDS = ("exit", "close", "good bye", "off", "stop", "quit")


def parser_input(user_input):
    cmd, *args = user_input.split()
    handler = HANDLERS[cmd.lower()]
    return handler, args

#@input_error
def main():
    while True:
        user_input = input(">>>")
        if user_input.lower() in EXIT_COMMANDS:
            print("Good bye!")
            break

        try:
            handler, *args = parser_input(user_input)
            result = handler(*args)
        except KeyError:
            result = f'Unknown command "{user_input}", please try again.'

        print(result)


if __name__ == "__main__":
    main()