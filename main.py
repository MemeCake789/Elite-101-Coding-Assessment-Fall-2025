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

    def returnBook(self) -> bool:
        """
        Returns the book, sets it as available, and clears the due date.
        """
        if not self.available:
            self.available = True
            self.due_date = None
            print(f"Book '{self.title}' has been returned.")
            return True
        else:
            print(f"Book '{self.title}' was already available.")
            return False


# convert book data into list of book classes
booksList = [Book(book_data) for book_data in library_books]


# helper functions
def cleanString(string: str) -> str:
    """
    simplifies a string to a no-space, lowercase word.
    EX: "Hello World" -> "helloworld"
    """
    # return string.replace(" ", "").lower()
    return string.strip().lower()
    # TODO : use trim instead of replace for clean function


def getBookById(id: str, books: list) -> list:
    """
    Returns a list containing the book with the matching id, or an empty list if not found.
    """
    for book in books:
        if book.id == cleanString(id):
            return [book]
    return []


def dateToDatetime(due_date):
    """
    Converts a due_date to a datetime object if it's a string, otherwise returns it as is.
    """
    if isinstance(due_date, str):
        try:
            return datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return None  # Or handle this error as appropriate for your application
    return due_date


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
        print("No books currently available.")
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
        bookAuthor = cleanString(book.author)
        bookGenre = cleanString(book.genre)
        if bookAuthor == cleanString(query) or bookGenre == cleanString(query):
            search_results.append(book)

    return search_results


# -------- Level 3 --------


def checkoutBook(id: str) -> list:
    """
    Checks out a book by ID using the Book object's checkout method.
    """
    bookList = getBookById(id, booksList)
    if not bookList:
        print(f"Book with ID {id} not found.")
        return []

    book = bookList[0]
    book.checkout()
    return bookList


# -------- Level 4 --------
def returnBook(id: str) -> list:
    """
    Returns a book by ID using the Book object's returnBook method.
    """
    bookList = getBookById(id, booksList)
    if not bookList:
        print(f"Book with ID {id} not found.")
        return []

    book = bookList[0]
    book.returnBook()
    return bookList


def listOverdue(books: list) -> list:
    """
    Returns a list of books that are checked out and past their due date.
    """
    overdueBooks = []
    for book in books:
        # Check if the book is unavailable (checked out), has a due date, and that date is in the past
        if not book.available and book.due_date:
            book.due_date = dateToDatetime(book.due_date)
            overdueBooks.append(book)
    return overdueBooks


def displayMenu():
    print("--- Library ---")
    print("1. View Available Books")
    print("2. Search for a Book")
    print("3. Check Out a Book")
    print("4. Return a Book")
    print("5. List Overdue Books")
    print("6. Exit")
    print("--------------------")


def main():
    while True:
        displayMenu()
        choice = input("Enter choice: ")

        match choice:
            case "1":
                print("\n--- Available Books ---")
                printAvailable(booksList)

            case "2":
                query = cleanString(input("Enter author or genre to search: "))
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
                book_id = cleanString(input("Enter book id to check out: "))
                checkoutBook(book_id)
            case "4":
                book_id = cleanString(input("Enter book id to return: "))
                returnBook(book_id)
            case "5":
                overdue = listOverdue(booksList)
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
    main()
