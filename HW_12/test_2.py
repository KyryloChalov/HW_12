from collections import UserDict
from datetime import datetime
import os.path
import pickle

# =============================================
#             test 2 (functions)
# =============================================


title = "\tPhoneBook\tversion 5.5.49"
len_of_name_field = 12          # довжина поля для виводу імені (думаю, має бути 20)
filename = 'book_test_2.bin'    

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
        
    # зробити перевірку, що birthday - то є дата у форматі '%d-%m-%Y'
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

    def add_phone(self, phone: Phone) -> str:
        phone = Phone(phone)
        if phone in self.phones:
            return f"number {phone} is already present in {self.name}'s contact list  \n\t{self}"
        self.phones.append(phone)
        return f"phone number {phone} has been added to {self.name}'s contact list  \n\t{self}"

    def add_birthday(self, birthday: BirthDay):
        self.birthday = birthday
        return f"the date of birth for contact {self.name} is set to {self.birthday} \n\t{self}"

    def remove_phone(self, phone: Phone) -> str:
        phone = Phone(phone)
        if phone in self.phones:
            self.phones.remove(phone)
            return f"phone number {phone} has been removed from {self.name}'s contact list \n\t{self}"
        return f"phone number {phone} is not among the contact numbers of {self.name} \n\t{self}"
      
    def change_name_record(self, name: Name) -> str:
        old_name = self.name
        self.name = Name(name)
        return f"the name of the contact {old_name} has been changed to {self.name} \n\t{self}"
      
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
        for p in self.phones:
            if p == phone:
                return f"phone number {phone} found among {self.name}'s contact numbers"
        return f"phone number {phone} not found"
    
    def seek_phone(self, phone: Phone):
        for p in self.phones:
            ph = p.value[:]
            if str(phone) in str(ph):
                return True
            else:
                return False

    def __str__(self) -> str:
        blanks = " " * (len_of_name_field - len(str(self.name)))
        if self.birthday: 
            return f"{self.name} {blanks}: {', '.join(str(p) for p in self.phones)}  birthday: {self.birthday} ({self.days_to_birthday(self.birthday)} days before next)"
        else: 
            return f"{self.name} {blanks}: {', '.join(str(p) for p in self.phones)}"
            
    def __repr__(self) -> str:
        return str(self)
 
    # def days_to_birthday(self, birthday: BirthDay):
    def days_to_birthday(self, birthday):
        today_date = datetime.today().date()
        bd_split = str(self.birthday).split('-')
        bd_this_year = datetime(day=int(bd_split[0]), month=int(bd_split[1]), year=today_date.year).date()
        bd_next_year = datetime(day=int(bd_split[0]), month=int(bd_split[1]), year=today_date.year+1).date()
        return ((bd_next_year - today_date) if (bd_this_year < today_date) else (bd_this_year - today_date)).days

class AddressBook(UserDict):

    def add_record(self, record: Record):
        # self.data[record.name] = record
        self.data[record.name.value] = record
        return f"contact {record.name} has been successfully added \n\t{record}"        

    def find_name(self, name: Name):
        name = Name(name)
        for key, item in self.data.items():
            if str(key) == str(name):
                return f"contact {name} found \n\t{item}"
        return f"contact {name} not found"
        
    def delete_record(self, name: Name):
        name = Name(name)
        # print(self.data)
        for key, item in self.data.items():
            # print(str(key))
            # print(str(name))
            if str(key) == str(name):
                del self.data[key]
                return f"contact {name} has been successfully deleted"
        return f"contact {name} not found"

    # def delete_record(self, name: Name):
    #     name = Name(name)        
    #     print(name)
    #     if self.data.get(name):
    #         del self.data[name]
    #         return f"contact {name} has been successfully deleted"
    #     return f"contact {name} not found"        
    
    
    def iterator(self, n=None):
        counter = 0
        while counter < len(self):
            yield list(self.values())[counter: counter + n]
            counter += n
            
    def read_contacts_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as fh:
                self = pickle.load(fh)
        print(f"the contact book has been successfully restored from file")
        return self
        # return f"the contact book has been successfully restored from file \n{self}"

    def write_contacts_to_file(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)
        # return self
        return f"the contact book has been saved successfully"

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
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = book.get(str(name))
    if not rec:
        return f"contact {name} not found in address book"
    return rec.add_phone(phone)
    
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
    new_name = Name(args[1])
    rec: Record = book.get(str(name))
    print(f"{rec = }")
    if not rec:
        return f"contact {name} not found in address book"
    print(f"===>>> {name = }")
    print(f"===>>> {new_name = }")
    return rec.change_name_record(new_name)

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
    find = False
    result = ""
    seek = args[0].lower()
    for name, record in book.data.items():
        if seek.isdigit():
            if record.seek_phone(seek):
                result += "\t" + str(record) + "\n"
                find = True
        if seek in name.lower():
            result += "\t" + str(record) + "\n"
            find = True
    if result:
        return f"data found for your request '{seek}': \n{result[:-1]}"
    else:
        return f"Nothing was found for your request '{seek}'"
    
def help_page(*args):
    
    help_list = [title]
    help_list.append('add <name> <phone>*n <birthday>   - add a new contact with a phone number(s) and birthday(optional)')
    help_list.append('                                  - you can enter several phone numbers for a contact')
    help_list.append('delete contact <name> <phone>     - remove an existing contact')    

    help_list.append('add phone <name> <new_phone>      - add the new phone number for an existing contact')
    help_list.append('add bd <name> <birthday>          - add the birthday data for an existing contact')
    help_list.append('change <name> <phone> <new_phone> - change the phone number for an existing contact')
    help_list.append('change name <name> <new_name>     - change the name for an existing contact')
    help_list.append('change bd <name> <new_birthday>   - change the phone number for an existing contact')
    help_list.append('delete phone <name> <phone>       - delete one phone number from an existing contact')    
    help_list.append('find <anything>                   - search for any string (>= 3 characters) in the contact data')
    help_list.append('phone <name>                      - search phone number by name')
    help_list.append('name <phone>                      - search name by phone number')

    help_list.append('list <pages>                      - show all contacts, <pages>(optional) - lines per page')
    help_list.append('hello                             - "hello-string"')
    help_list.append('exit                              - exit from PhoneBook')
    help_list.append('help                              - this help-page')
    
    return "\n".join(help_list)


def say_hello(*args):
    return "How can I help you?"


def say_goodbay(*args):
    exit("Good bye!")


if __name__ == '__main__':
    
     
       
    print(" ================== test 2 ===============")
    
    print(help_page())
    # print(say_hello())

    print(add_contact("Jill", "0677977166"))
    print(add_contact("Jill", "0677977167"))
    print(add_contact("Bill", "0997058845", "15-03-1999"))
    

    print(add_contact("Jill_t", "0677977176", "0956783423", "0669873456", "050 345 22 34"))
    print(add_contact("Bill_t", "0997078845", "099 745-12-35", "0964523265", "15-03-2002"))
    print(add_contact("Jill_t", "0677977176", "0679845321"))
    print(add_contact("Jill_t", "0677977188"))
    print(add_contact("Person_0", "(099)475-71-22"))
    
    print(change_phone("Jill_t", "0677977176", "0954122568"))
    print(change_phone("Jill_t", "0677977176", "0954122568"))
    print(change_phone("Jill_t", "0954122568", "0954122599"))

    print(del_phone("Jill_t", "0954122599"))
    print(del_phone("Jill_t", "0954122599"))
    print(del_phone("Jill_t", "0679845321"))
    print(del_phone("Jill_v", "0954122599"))

    print(add_birthday("Jill_t", "28-03-1968"))
    
    print(add_phone("Jill_t", "0677977199"))
    
    print(book.delete_record("Jill_t"))

    print(add_phone("Jill_t", "0677977199"))
    

    print(book.find_name("Bill_t"))

    print(search("45"))
    print(search("ill"))
    
    print(show_all())
    
    print(book.write_contacts_to_file(filename))
    
    print(show_all())
    
    
    print(del_record("Jill"))
    print(del_record("Bill"))
    print(del_record("Jill_v"))
    print(del_record("Bill_t"))

    print(show_all())

    book = book.read_contacts_from_file(filename)
    
    print(show_all())
    
    
    
    print(add_contact("Person_1", "(066)4525588", "22-03-1998"))
    print(add_contact("Person_2", "0675468899"))
    print(add_contact("Person_3", "+38(098)221-15-44", "14-08-1988"))
    print(add_contact("Person_4", "+380664589955", "22-01-1968"))
    print(add_contact("Person_5", "1234567890"))
    print(add_contact("Person_6", "0987654321", "11-05-2001"))
    print(add_contact("Person_7", "099 225 55 66", "22-04-1870"))
    print(add_contact("Person_8", "0958645548", "12-04-1967"))
    print(add_contact("Person_9", "(099)475-31-11"))

    print(show_all(8))
    
    
    print(say_goodbay())
  