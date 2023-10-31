from collections import UserDict
from datetime import datetime
import os.path
import pickle



TITLE = "\tPhoneBook\tversion 5.6.12"
LEN_OF_naME_FIELD = 12          # довжина поля для виводу імені 
FILENAME = 'addressbook.bin'

BLACK = "\033[30m"
RED =   "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE =  "\033[34m"
MAGENTA = "\033[35m"
CYAN =  "\033[36m"
WHITE = "\033[37m"
GRAY =  "\033[90m"  
RESET = "\033[0m"

class Field:
    
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value
        
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    
    def __init__(self, value: str) -> None:
        super().__init__(str(value).title())


class Phone(Field):
        
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone: str):
        
        new_phone = str(phone).strip()
        for char in '+( )-.':
            new_phone = new_phone.replace(char, "")
        if len(new_phone) >= 9 and new_phone.isdigit():
            new_phone = "+380" + new_phone[-9:]
        else:
            raise ValueError(f"{phone} - incorrect phone number")        
        self.__value = new_phone


class BirthDay(Field):
    
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, value):
        self.__value = datetime.strptime(value, '%d-%m-%Y').date()
        print(self.__value)
        

class Record:

    def __init__(self, name: Name, phone: Phone | None = None, birthday:BirthDay | None = None) -> None:
        self.name = Name(name)  
        phone = Phone(phone) if phone else None
        self.phones = [phone] if phone else []
        self.birthday = birthday if birthday else None

    def add_birthday(self, birthday: BirthDay):
        self.birthday = birthday
        return f"the date of birth for contact {self.name} is set to {self.birthday} \n\t{self}"

    def add_phone(self, phone: Phone) -> str:
        phone = Phone(phone)
        if phone in self.phones:
            return f"number {phone} is already present in {self.name}'s contact list  \n\t{self}"
        self.phones.append(phone)
        return f"phone number {phone} has been added to {self.name}'s contact list  \n\t{self}"
 
    def days_to_birthday(self, birthday: BirthDay):
        today_date = datetime.today().date()
        birth_date = datetime.strptime(birthday, "%d-%m-%Y")
        bd_next = datetime(day=birth_date.day, month=birth_date.month, year=today_date.year)
        age = today_date.year - birth_date.year
        if today_date > bd_next.date():
            bd_next = datetime(day=birth_date.day, month=birth_date.month, year=today_date.year + 1)
            age += 1
        days_until = (bd_next.date() - today_date).days
        return days_until, age
           
    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> str:
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)
        if old_phone == new_phone:
            return f"you are trying to replace the phone number {old_phone} with the same one {new_phone} \n\t{self}"
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone
            return f"phone number {old_phone} has been successfully changed to {new_phone} for contact {self.name} \n\t{self}"
        return f"phone number {old_phone} is not among the contact numbers of {self.name} \n\t{self}"
    
    def find_phone(self, phone: Phone):
        phone = Phone(phone)
        for ph in self.phones:
            if ph == phone:
                return f"phone number {phone} found among {self.name}'s contact numbers"
        return f"phone number {phone} not found"

    def remove_phone(self, phone: Phone) -> str:
        phone = Phone(phone)
        if phone in self.phones:
            self.phones.remove(phone)
            return f"phone number {phone} has been removed from {self.name}'s contact list \n\t{self}"
        return f"phone number {phone} is not among the contact numbers of {self.name} \n\t{self}"
    
    def seek_phone(self, phone: Phone):
        for p in self.phones:
            ph = p.value[:]
            if str(phone) in str(ph):
                return True
            else:
                return False

    def __str__(self) -> str:
        blanks = " " * (LEN_OF_naME_FIELD - len(str(self.name)))
        if self.birthday: 
            if int(self.days_to_birthday(self.birthday)[0]) == 0:
                return f"{self.name} {blanks}: {', '.join(str(p) for p in self.phones)} {MAGENTA} birthday: {RESET} {self.birthday} {MAGENTA}(today is {self.days_to_birthday(self.birthday)[1]}th birthday){RESET}"
            elif self.days_to_birthday(self.birthday)[0] <= 7:
                return f"{self.name} {blanks}: {', '.join(str(p) for p in self.phones)} {CYAN} birthday: {RESET} {self.birthday} {CYAN}({self.days_to_birthday(self.birthday)[0]} days until the {self.days_to_birthday(self.birthday)[1]}th birthday){RESET}"
            else:
                return f"{self.name} {blanks}: {', '.join(str(p) for p in self.phones)} {GRAY} birthday: {RESET} {self.birthday} {GRAY}({self.days_to_birthday(self.birthday)[0]} days until the {self.days_to_birthday(self.birthday)[1]}th birthday){RESET}"
        else: 
            return f"{self.name} {blanks}: {', '.join(str(p) for p in self.phones)}"
            
    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return f"contact {record.name} has been successfully added \n\t{record}"        
        
    def delete_record(self, name: Name):
        name = Name(name)
        for key, item in self.data.items():
            if str(key) == str(name):
                del self.data[key]
                return f"contact {name} has been successfully deleted"
        return f"contact {name} not found"    

    def find_name(self, name: Name):
        name = Name(name)
        for key, item in self.data.items():
            if str(key) == str(name):
                return f"contact {name} found \n\t{item}"
        return f"contact {name} not found"
    
    def iterator(self, n=None):
        counter = 0
        while counter < len(self):
            yield list(self.values())[counter: counter + n]
            counter += n
            
    def read_contacts_from_file(self, FILENAME):
        if os.path.exists(FILENAME):
            with open(FILENAME, "rb") as fh:
                self = pickle.load(fh)
        print(f"{GRAY}the contact book has been successfully restored from file{RESET}")
        return self

    def write_contacts_to_file(self, FILENAME):
        with open(FILENAME, "wb") as fh:
            pickle.dump(self, fh)
        return f"{GRAY}the contact book has been saved successfully{RESET}"

    def __str__(self):
        return "\n".join([str(r) for r in self.data.values()])


book = AddressBook()


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params.\nFormat: '<command> <name> <phone>'\nUse 'help' for information"
        except KeyError:
            return f"Unknown name {args[0]}. Try another or use help."
    return inner

def is_exist(value, result=False):
    for n in book:
        if str(n) == str(value):
            return True 
    return result

def find_str(name) -> str:
    for key, val in book.items():
        if str(key) == str(name):
            return str(val)

@user_error
def add_contact(*args):
    
    name = Name(args[0])
    if is_exist(name):
        str_1 = f"contact {str(name)} already exist\n\t{str(find_str(name))}"
        str_2 = f"\n\tUse 'add phone' or 'change' command to add or change the phone"
        return str_1 + str_2
    else:
        rec = Record(name)
        bd = str(args[-1])
        if bd[2] == "-" and bd[5] == "-":
            birthday = bd
            rec.birthday = birthday
            args = args[1:-1]
        else:
            args = args[1:]
            
        for phone in args:
            rec.add_phone(Phone(phone))
        
        return book.add_record(rec)

@user_error
def add_phone(*args):
    
    result = ""
    name = Name(args[0])
    rec: Record = book.get(str(name))
    if not rec:
        return f"contact {name} not found in address book"
    args = args[1:]
    print(args)
    for phone in args:
        rec.add_phone(phone)
        result += f"phone number {phone} has been added to {name}'s contact list\n"
    # phone = Phone(args[1])
    # return rec.add_phone(phone)
    return result + f"\t{rec}"
    
@user_error
def add_birthday(*args):
    
    name = Name(args[0])
    birthday = (args[1])
    rec: Record = book.get(str(name))
    if not rec:
        return f"contact {name} not found in address book"
    return rec.add_birthday(birthday)

@user_error
def change_name(*args):
    
    name = Name(args[0])
    name_new = Name(args[1])
    rec: Record = book.get(str(name))
    if not rec:
        return f"contact {name} not found in address book"
    rec_new = Record(name_new)
    for item in rec.phones:
        rec_new.add_phone(item)
    rec_new.birthday = rec.birthday if rec.birthday else None
    book.add_record(rec_new)
    book.delete_record(name)
    return f"the name of the contact {name} has been changed to {name_new} \n\t{rec_new}"

@user_error
def change_phone(*args):
    
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = book.get(str(name))
    if not rec:
        return f"contact {name} not found in address book"
    return rec.edit_phone(old_phone, new_phone)

@user_error
def del_phone(*args):
    
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = book.get(str(name))
    if not rec:
        return f"contact {name} not found in address book"
    return rec.remove_phone(Phone(phone))

@user_error
def del_record(*args):
    
    name = Name(args[0])
    rec: Record = book.get(str(name))
    if not rec:
        return f"Record with name {name} not found"
    return book.delete_record(name)

@user_error
def name_find(*args):
    
    name = Name(args[0])
    rec: Record = book.get(str(name))
    if not rec:
        return f"Record with name {name} not found"
    return book.find_name(name)

def show_all(*args):
    pages = int(args[0]) if args else len(book.data)
    print(f"  ==== Address book ====")
    count = 0
    for _ in book.iterator(pages):
        for item in _:
            print(item)
            count += 1
        if count < len(book):
            input(" >>> Press Enter for next records: ")
    return " >>> End of List "
    
def search(*args):
    result = ""
    seek = args[0].lower()
    for name, record in book.data.items():
        if seek.isdigit():
            if record.seek_phone(seek):
                result += "\t" + str(record) + "\n"
        if seek in name.lower():
            result += "\t" + str(record) + "\n"
    if result:
        return f"data found for your request '{seek}': \n{result[:-1]}"
    else:
        return f"Nothing was found for your request '{seek}'"
    
def help_page(*args):
    help_list = [TITLE]
    help_list.append(f'{YELLOW}add {CYAN}<name> <phone>{GRAY}*n {CYAN}<birthday>          {RESET} - add a new contact with a phone number(s) and birthday(optional)')
    help_list.append(f'{GRAY}                                                (you can enter several phone numbers for a contact){RESET}')
    help_list.append(f'{YELLOW}add_phone {CYAN}<name> <new_phone>{GRAY}*n           {RESET} - add the new phone number for an existing contact')
    help_list.append(f'{GRAY}                                                (you can enter several phone numbers for a contact){RESET}')
    help_list.append(f'{YELLOW}add_bd {CYAN}<name> <birthday>                 {RESET} - add the birthday data ("dd-mm-yyyy") for an existing contact')
    help_list.append(f'{YELLOW}change_name {CYAN}<name> <new_name>            {RESET} - change the name for an existing contact')
    help_list.append(f'{YELLOW}change_phone {CYAN}<name> <phone> <new_phone>  {RESET} - change the phone number for an existing contact')
    help_list.append(f'{YELLOW}change_bd {CYAN}<name> <new_birthday>          {RESET} - change the phone number for an existing contact')
    help_list.append(f'{YELLOW}delete_phone {CYAN}<name> <phone>              {RESET} - delete one phone number from an existing contact')    
    help_list.append(f'{YELLOW}delete_contact {CYAN}<name> <phone>            {RESET} - remove an existing contact')    
    help_list.append(f'{YELLOW}find {CYAN}<anything>                          {RESET} - search for any string (>= 3 characters) in the contact data')
    help_list.append(f'{YELLOW}name {CYAN}<name>                              {RESET} - search record by the name')
    help_list.append(f'{YELLOW}list {GRAY}<pages>                             {RESET} - show all contacts, {GRAY}<pages>(optional) - lines per page{RESET}')
    help_list.append(f'{YELLOW}hello                                    {RESET} - "hello-string"')
    help_list.append(f'{YELLOW}exit                                     {RESET} - exit from PhoneBook')
    help_list.append(f'{YELLOW}help                                     {RESET} - this help-page')
    return "\n".join(help_list)


def say_hello(*args):
    return "How can I help you?"


def say_good_bay(*args):
    print(book.write_contacts_to_file(FILENAME))
    exit("Good bye!")


def unknown(*args):
    return f"{RED}Unknown command. Try again{RESET}"

#=============================================
#                main
#=============================================



COMMANDS = {
    add_contact:    ("add_record", "add", "add_contact", "+"),
    add_phone:      ("add_phone", "phone_add"),
    change_phone:   ("change_phone", "change_phone", "edit_phone"),
    del_phone:      ("del_phone", "delete_phone"), 
    del_record:     ("delete_record", "delete", "del"),
    add_birthday:   ("add_birthday", "add_bd", "change_birthday", "change_bd"),
    change_name:    ("change_name", "name_change"),
    name_find:      ("name", "find_name"),
    search:         ("search", "seek", "find"),
    help_page:      ("help",),
    say_hello:      ("hello", "hi"),
    show_all:       ("show_all", "show", "list"),
    say_good_bay:    ("exit", "good_bay", "by", "close", "end")
            }

def parser(text:str):
    for func, cmd_tpl in COMMANDS.items():
        for command in cmd_tpl:
            data = text.strip().lower().split()
            if data[0] == command:
                return func, data[1:]
    return unknown, []


def main():
    global book
    book = book.read_contacts_from_file(FILENAME)
    print("\n" + BLUE + TITLE + RESET +"\t\tType 'help' for information")
    while True:
        user_input = input(">>>").strip().lower()
        func, data = parser(user_input)
        print(func(*data))
        if func not in [say_good_bay, show_all, say_hello, help_page, search, name_find]:
            book.write_contacts_to_file(FILENAME)


if __name__ == '__main__':
    
    main()
            