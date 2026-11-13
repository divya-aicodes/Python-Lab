"""Manage a library collection with Book and Library classes."""

from dataclasses import dataclass


@dataclass
class Book:
    """Represent a book and its borrowing status."""

    isbn: str
    title: str
    author: str
    is_borrowed: bool = False


class Library:
    """Manage books indexed by ISBN."""

    def __init__(self) -> None:
        self._books: dict[str, Book] = {}

    @property
    def books(self) -> tuple[Book, ...]:
        """Return books ordered by title."""
        return tuple(sorted(self._books.values(), key=lambda book: book.title.casefold()))

    def add_book(self, book: Book) -> None:
        """Add a uniquely identified book."""
        normalized_isbn = book.isbn.strip().casefold()
        if not normalized_isbn or not book.title.strip() or not book.author.strip():
            raise ValueError("ISBN, title, and author are required.")
        if normalized_isbn in self._books:
            raise ValueError("A book with this ISBN already exists.")
        book.isbn = book.isbn.strip()
        book.title = book.title.strip()
        book.author = book.author.strip()
        self._books[normalized_isbn] = book

    def find_by_isbn(self, isbn: str) -> Book | None:
        """Return a book matching an ISBN."""
        return self._books.get(isbn.strip().casefold())

    def search(self, query: str) -> list[Book]:
        """Return books whose title or author contains a query."""
        normalized_query = query.strip().casefold()
        if not normalized_query:
            return []
        return [
            book
            for book in self.books
            if normalized_query in book.title.casefold()
            or normalized_query in book.author.casefold()
        ]

    def borrow_book(self, isbn: str) -> Book:
        """Borrow an available book."""
        book = self.find_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found.")
        if book.is_borrowed:
            raise ValueError("Book is already borrowed.")
        book.is_borrowed = True
        return book

    def return_book(self, isbn: str) -> Book:
        """Return a borrowed book."""
        book = self.find_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found.")
        if not book.is_borrowed:
            raise ValueError("Book is already available.")
        book.is_borrowed = False
        return book


def display_books(books: tuple[Book, ...] | list[Book]) -> None:
    """Display a collection of books."""
    if not books:
        print("No books found.")
        return
    print(f"{'ISBN':<16} {'Title':<30} {'Author':<24} Status")
    print("-" * 86)
    for book in books:
        status = "Borrowed" if book.is_borrowed else "Available"
        print(f"{book.isbn:<16} {book.title:<30} {book.author:<24} {status}")


def main() -> None:
    """Run the library management menu."""
    library = Library()
    while True:
        print("\n========== LIBRARY MANAGEMENT ==========")
        print("1. Add book")
        print("2. Display all books")
        print("3. Search by title or author")
        print("4. Borrow book")
        print("5. Return book")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                library.add_book(
                    Book(
                        input("Enter ISBN: "),
                        input("Enter title: "),
                        input("Enter author: "),
                    )
                )
                print("Book added successfully.")
            elif choice == "2":
                display_books(library.books)
            elif choice == "3":
                display_books(library.search(input("Enter title or author: ")))
            elif choice == "4":
                book = library.borrow_book(input("Enter ISBN: "))
                print(f"Borrowed: {book.title}")
            elif choice == "5":
                book = library.return_book(input("Enter ISBN: "))
                print(f"Returned: {book.title}")
            elif choice == "6":
                print("Library management system closed.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 6.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()
