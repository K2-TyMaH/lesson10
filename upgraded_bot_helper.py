from collections import UserDict


class AddressBook(UserDict):

    def add_record(self, name):
        new_user = Record(name)
        while True:
            user_phone = input(f'What phone you wanna add to {name} (skip it if you don\'t want): ')
            if user_phone:
                new_user.add_phone(user_phone)
                print(f'{user_phone} added to {name}')
            else:
                break
        self.data[new_user.name.value] = new_user

    def find_user(self, name):
        return self.data.get(name)

    def show_all_records(self):
        result = ""
        for name, phones in self.data.items():
            result += f"{name}: {phones.phones}\n"
        print(result)

    def remove_phones(self, name):
        checking = self.find_user(name)
        if checking:
            checking.remove_phone()
        else:
            print(f'{name} doesn\'t exist')

    def change_phones(self, name):
        checking = self.find_user(name)
        if checking:
            checking.change_phone()
            print(f'New phone added to {name}!')
        else:
            print(f'{name} doesn\'t exist')

class Field:
    pass

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, phone):
        self.phone = phone

class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        added_phone = Phone(phone)
        self.phones.append(added_phone.phone)

    def change_phone(self):
        new_phone = input('Input new phone: ')
        self.add_phone(new_phone)
        return new_phone

    def remove_phone(self):
        if self.phones:
            showing = dict(enumerate(self.phones, 1))
            while True:
                try:
                    print(f'What phone you want to remove? {showing}')
                    choosing = int(input('Choose № of this phone >>>'))
                    self.phones.remove(showing[choosing])
                    print(f'{showing[choosing]} removed')
                    break
                except ValueError:
                    print(f'{choosing} is not a number!')
                except KeyError:
                    print(f'{choosing} is out of range!')
            return True
        else:
            print('Phones list is empty')

        # if phone_to_remove in self.phones:
        #     self.phones.remove(phone_to_remove)
        # else:
        #     print(f'I didn\'t find {phone_to_remove}')


USERS = AddressBook()

# def input_error(func):
#     def inner(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except KeyError:
#             return 'This contact doesnt exist, please try again.'
#         except ValueError as exception:
#             return exception.args[0]
#         except IndexError:
#             return 'This contact cannot be added, it exists already'
#         except TypeError:
#             return 'Unknown command or parameters, please try again.'
#     return inner


#@input_error
def add_user(name):
    USERS.add_record(name)
    return f"User {name} added"

def remove_phone(name):
    USERS.remove_phones(name)
    return f'Do you wanna do something else?'

#@input_error
def change_phone(name):
    USERS.change_phones(name)
    return f'Do you wanna do something else?'

#@input_error
def show_number(name):
    result = USERS.find_user(name)
    if result:
        return f"{name}: {result.phones}"
    else:
        print(f'User {name} doesn\'t exist.')
        return f'Do you wanna do something else?'


HANDLERS = {

    "add": add_user,
    "change": change_phone,
    "remove": remove_phone,
    "phone": show_number,
}

EXIT_COMMANDS = ("exit", "close", "good bye", "off", "stop", "quit")
SHOW_ALL_LIST_COMMANDS = ("show", "show_all", "show all")


def parser_input(user_input):
    try:
        inputed = user_input.split()
        cmd = inputed[0]
        name = inputed[1]
        handler = HANDLERS[cmd.lower()]
        return handler, name
    except IndexError:
        print('Write something else')


def main():
    while True:
        user_input = input(">>>")
        if user_input.lower() in EXIT_COMMANDS:
            print("Good bye!")
            break
        elif user_input.lower() in SHOW_ALL_LIST_COMMANDS:
            USERS.show_all_records()
            continue

        try:
            handler, name = parser_input(user_input)
            result = handler(name)
        except KeyError:
            result = f'Unknown command "{user_input}", please try again.'
        except TypeError:
            result = f'You wrote something strange'

        print(result)


if __name__ == "__main__":
    main()