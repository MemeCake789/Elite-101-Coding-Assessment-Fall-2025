from datetime import datetime, timedelta

from library_books import library_books

# Used info from here for python docstrings (documentation) : https://www.geeksforgeeks.org/python/python-docstrings/
# Used info from here for dateTime() : https://www.w3schools.com/python/python_datetime.asp


class Book:
    """
    Represents a book in the library system.
    """

    def __init__(self, book_data: dict):
        self.id = book_data["id"]
        self.title = book_data["title"]
        self.author = book_data["author"]
        self.genre = book_data["genre"]
        self.available = book_data["available"]
        self.due_date = book_data["due_date"]
        self.checkouts = book_data["checkouts"]

    def checkout(self) -> bool:
        """
        Checks out the book, sets it as unavailable, updates due date and checkout count.
        """
        if self.available:
            self.available = False
            self.due_date = datetime.now() + timedelta(days=14)
            self.checkouts += 1
            print(
                f"Book '{self.title}' has been checked out. Due date: {self.due_date.strftime('%Y-%m-%d')}"
            )
            return True
        else:
            print(f"Book '{self.title}' is currently unavailable.")
            return False

    def return_book(self) -> bool:
        """
        Returns the book, sets it as available, and clears the due date.
        """
        if not self.available:
            self.available = True
            self.due_date = None
            print(f"'{self.title}' has been returned.")
            return True
        else:
            print(f"'{self.title}' is already available.")
            return False


# convert book data into list of book classes
booksList = [Book(book_data) for book_data in library_books]


# helper functions
def clean_string(string: str) -> str:
    """
    simplifies a string to a no-space, lowercase word.
    EX: "Hello World" -> "helloworld"
    """
    return string.replace(" ", "").lower()


def get_book_by_id(id: str, books: list) -> list:
    """
    Returns a list containing the book with the matching id, or an empty list if not found.
    """
    for book in books:
        if book.id == id:
            return [book]
    return []


# -------- Level 1 --------


def viewAvailable(books: list) -> list:
    """
    Returns a list of books that have the "available" value as True
    """
    availableBooks = []

    for book in books:
        if book.available:
            availableBooks.append(book)

    return availableBooks


def printAvailable(books: list):
    """
    Prints a nicely formatted list of available books, only showing the book id, title, and author.
    """

    availableBooks = viewAvailable(books)

    if not availableBooks:
        print("No books available.")
        return

    for book in availableBooks:
        print(f"ID: {book.id} | Title: {book.title} | Author: {book.author}")


# -------- Level 2 --------


def searchBook(query: str, books: list) -> list:
    """
    Returns the book(s) with the author or genre given a query
    """

    search_results = []

    for book in books:
        bookAuthor = clean_string(book.author)
        bookGenre = clean_string(book.genre)
        if bookAuthor == clean_string(query) or bookGenre == clean_string(query):
            search_results.append(book)

    return search_results


# -------- Level 3 --------


def checkout_book(id: str) -> list:
    """
    Checks out a book by ID using the Book object's checkout method.
    """
    bookList = get_book_by_id(id, booksList)
    if not bookList:
        print(f"Book with ID {id} not found.")
        return []

    book = bookList[0]
    book.checkout()  # Use the Book class method
    return bookList


# -------- Level 4 --------
def return_book(id: str) -> list:
    """
    Returns a book by ID using the Book object's return_book method.
    """
    bookList = get_book_by_id(id, booksList)
    if not bookList:
        print(f"Book with ID {id} not found.")
        return []

    book = bookList[0]
    book.return_book()  # Use the Book class method
    return bookList


def list_overdue(books: list) -> list:
    """
    Returns a list of books that are checked out and past their due date.
    """
    overdueBooks = []
    for book in books:
        # Check if the book is unavailable (checked out), has a due date, and that date is in the past
        if not book.available and book.due_date and book.due_date < datetime.now():
            overdueBooks.append(book)
    return overdueBooks


def display_menu():
    print("\n--- Library ---")
    print("1. View Available Books")
    print("2. Search for a Book")
    print("3. Check Out a Book")
    print("4. Return a Book")
    print("5. List Overdue Books")
    print("6. Exit")
    print("---")


def main_menu():
    while True:
        display_menu()
        choice = input("Enter choice: ")

        match choice:
            case "1":
                print("\n--- Available Books ---")
                printAvailable(booksList)

            case "2":
                query = input("Enter author or genre to search: ")
                results = searchBook(query, booksList)
                if results:
                    print("\n--- Search Results ---")
                    for book in results:
                        print(
                            f"ID: {book.id} | Title: {book.title} | Author: {book.author} | Genre: {book.genre} | Available: {book.available}"
                        )
                else:
                    print(f"No books found matching '{query}'.")
            case "3":
                book_id = input("Enter book id to check out: ")
                checkout_book(book_id)
            case "4":
                book_id = input("Enter book id to return: ")
                return_book(book_id)
            case "5":
                overdue = list_overdue(booksList)
                if overdue:
                    print("\n--- Overdue Books ---")
                    for book in overdue:
                        print(
                            f"ID: {book.id} | Title: {book.title} | Due Date: {book.due_date.strftime('%Y-%m-%d')}"
                        )
                else:
                    print("No books currently overdue.")
            case "6":
                print("Exiting")
                break
            case _:
                print("Invalid choice")


if __name__ == "__main__":
    main_menu()
