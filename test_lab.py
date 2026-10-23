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
def test_return_book():
    book1=book.Book('El alquimista','Paulo Coehlo',1967,'ISBN0001')
    assert book1.title == 'El alquimista'
    book1.borrow()
    assert book1.borrowed==True
    book1.return_book()
    assert book1.borrowed is False

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

@pytest.mark.unit
@pytest.mark.parametrize("title, isbn, esperado", [
    ("Cien años de soledad", "ISBN0002", "Borrwed: Cien años de soledad"),
    ("Pedro Páramo",         "ISBN0003", "Borrwed: Pedro Páramo"),
    ("Rayuela",              "ISBN0004", "Borrwed: Rayuela"),
])
def test_borrow_states(library_init, title, isbn, esperado):
    lib = library_init
    lib.add_book(book.Book(title, "Autor", 2000, isbn))

    lib.borrow_book('ID0001', isbn)

    miguel = lib.users[0]
    assert miguel.get_history() == [esperado]


# TEMA 1 - monkeypatch.setattr()

@pytest.mark.monkey
def test_library_borrow_setattr(monkeypatch, library_init):
    llamadas = []

    def fake_borrow(self):
        llamadas.append(self.title)
        self.borrowed = True

    monkeypatch.setattr(book.Book, "borrow", fake_borrow)

    library_init.borrow_book('ID0001', 'ISBN0001')

    assert llamadas == ['El alquimista']            # se usó el falso
    assert library_init.books[0].borrowed == True
    assert library_init.users[0].get_history() == ["Borrwed: El alquimista"]


# TEMA 2 - monkeypatch.delattr()

@pytest.mark.monkey
def test_borrow_delattr(monkeypatch, library_init):
    monkeypatch.delattr(user.User, "register_borrow")

    with pytest.raises(AttributeError):
        library_init.borrow_book('ID0001', 'ISBN0001')

    assert library_init.books[0].borrowed == True     # sí se prestó
    assert library_init.users[0].get_history() == []  # pero no se registró


# TEMA 3 - monkeypatch.setitem()

@pytest.mark.monkey
def test_loans_disabled_setitem(monkeypatch, library_init):
    monkeypatch.setitem(library.settings, "loans_enabled", False)

    resultado = library_init.borrow_book('ID0001', 'ISBN0001')

    assert resultado is None
    assert library_init.books[0].borrowed == False
    assert library_init.users[0].get_history() == []



# TEMA 11 - capsys

@pytest.mark.unit
def test_loans_disabled_capsys(monkeypatch, capsys, library_init):
    monkeypatch.setitem(library.settings, "loans_enabled", False)

    library_init.borrow_book('ID0001', 'ISBN0001')

    captured = capsys.readouterr()
    assert captured.out == "Loans are disabled\n"


# TEMA 9 - pytest.raises()

@pytest.mark.unit
def test_return_not_borrowed_raises(library_init):
    with pytest.raises(ValueError, match="The book is not currently borrowed"):
        library_init.return_book('ID0001', 'ISBN0001')


# TEMA 10 - try-except

@pytest.mark.system
def test_user_not_found_try_except(library_init):
    mensaje = None
    try:
        library_init.borrow_book('ID9999', 'ISBN0001')   # usuario no existe
    except ValueError as e:
        mensaje = str(e)                                 # se CAPTURA

    assert mensaje == "User not found"
    assert library_init.books[0].borrowed == False       # no se prestó


@pytest.mark.system
def test_borrow_twice_propagates(library_init):
    library_init.borrow_book('ID0001', 'ISBN0001')

    # La excepción nace en Book.borrow y se PROPAGA por Library.borrow_book
    with pytest.raises(ValueError, match="The book is already borrowed"):
        library_init.borrow_book('ID0001', 'ISBN0001')


# TEMA 8 - COBERTURA DE CAJA BLANCA

@pytest.mark.system
def test_library_return_book_coverage(library_init):
    library_init.borrow_book('ID0001', 'ISBN0001')
    library_init.return_book('ID0001', 'ISBN0001')

    assert library_init.books[0].borrowed == False
    assert library_init.users[0].get_history() == [
        "Borrwed: El alquimista",
        "Reurned: El alquimista",
    ]




