from HW_12 import Record, AddressBook

# =============================================
#             test 1 (Classes)
# =============================================

if __name__ == '__main__':
    

    book = AddressBook()
    filename = 'book_test_1.bin'
    
    print(book.add_record(Record("helen", birthday="23-11-1999")))
    
    name = "bill"
    phone = "0677977166"
    b_day = "27-10-1968"
    rec = Record(name, phone, b_day)
    print(book.add_record(rec))
    
    result = rec.add_phone("0677977166")
    print(result)
    
    print(rec.add_phone("0933903357"))
    
    print(rec.edit_phone("1234567890", "1234567809"))
    
    print(rec.edit_phone("0677977166", "0677977166"))
    
    print(rec.edit_phone("0677977166", "0997058845"))
    
    print(rec.remove_phone("0677977166"))

    print(rec.remove_phone("0997058845"))
    
    print(rec.add_phone("0677977166"))

    print(rec.find_phone("0677977166"))
    
    print(rec.find_phone("0933903357"))

    print(rec.find_phone("0677977444"))

    print(book.add_record(Record("ivan franko", "0671234567")))
    
    print(book.add_record(Record("mary", "0671234555", "29-10-2000")))
    
    print(book.add_record(Record("жамбил жабаєв", "0672223344", birthday="12-12-2012")))
    
    print(book.find_name("bill"))

    print(book.find_name("ivan"))
    
    print("======= before delete =========")
    print(book)
    
    print(book.write_contacts_to_file(filename))
    
    print(book.delete_record("mary"))
    
    print(book.delete_record("ivan"))
    
    print(book.delete_record("bill"))

    print("======== after delete ========")
    print(book)
    
    book = book.read_contacts_from_file(filename)
    
    print("======== after restoring from a file ========")
    print(book)
    