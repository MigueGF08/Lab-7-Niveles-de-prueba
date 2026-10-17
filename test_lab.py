import book 
import pytest
import user
import library

@pytest.mark.unit
def test_borrow_book():
    book1=book.Book('El alquimista','Paulo Coehlo',1967,'ISBN0001')
    assert book1.title == 'El alquimista'
    book1.borrow()
    assert book1.borrowed==True

@pytest.mark.unit
def test_re_borrow_book():
    book1=book.Book('El alquimista','Paulo Coehlo',1967,'ISBN0001')
    assert book1.title == 'El alquimista'
    book1.borrow()
    assert book1.borrowed==True
    with pytest.raises(ValueError,match="The book is already borrowed"):
        book1.borrow()

@pytest.mark.unit
def test_re_borrow_book():
    book1=book.Book('El alquimista','Paulo Coehlo',1967,'ISBN0001')
    assert book1.title == 'El alquimista'
    book1.borrow()
    assert book1.borrowed==True
    book1.return_book()
    assert book1.borrow==False

@pytest.mark.system
def test_library_borrow():
    book1=book.Book('El alquimista','Paulo Coehlo',1967,'ISBN0001')
    miguel = user.User('Miguel','ID0001')
    lib = library.Library()
    lib.add_book(book1)
    assert lib.books[0].title == 'El alquimista'
    lib.add_user(miguel)
    #corroborar que se agrego 
    lib.borrow_book('ID0001','ISBN0001')
    assert book1.borrowed==True


@pytest.fixture
def library_init():
    book1=book.Book('El alquimista','Paulo Coehlo',1967,'ISBN0001')
    miguel = user.User('Miguel','ID0001')
    lib = library.Library()
    lib.add_book(book1)
    lib.add_user(miguel)
    return lib

@pytest.mark.wip
def test_library_fixture(library_init):
    lib = library_init
    #corroborar que se agrego 
    lib.borrow_book('ID0001','ISBN0001')
    assert lib.books[0].borrowed==True






