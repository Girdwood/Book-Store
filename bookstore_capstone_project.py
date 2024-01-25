import sqlite3


class Bookstore:
    def __init__(self, db_name='ebookstore.db'):
        # Initialise the Bookstore object with a SQLite connection and cursor
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()
        # Create the database and populate it with initial data
        self.create_database()

    def create_database(self):
        # Create the 'book' table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                qty INTEGER
            )
        ''')

        # Check the number of existing books in the table
        self.cursor.execute('SELECT COUNT(*) FROM book')
        existing_books_count = self.cursor.fetchone()[0]

        # If no books exist, populate the table with initial data
        if existing_books_count == 0:
            books_data = [
                (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
                (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
                (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
            ]
            # Insert initial data into the 'book' table
            self.cursor.executemany('''
                INSERT INTO book (id, title, author, qty)
                VALUES (?, ?, ?, ?)
            ''', books_data)
            # Commit changes to the database
            self.db.commit()

        # Close the database connection
        self.db.close()

    def display_menu(self):
        # Display the menu
        while True:
            print("Menu:")
            print("1. Enter book")
            print("2. Update book")
            print("3. Delete book")
            print("4. Search books")
            print("0. Exit\n")

            choice = input("Enter your choice (0-4): ")

            if choice == "1":
                self.enter_book()
            elif choice == "2":
                self.update_book()
            elif choice == "3":
                self.delete_book()
            elif choice == "4":
                self.search_book()
            elif choice == "0":
                print("\nExiting the program.")
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 4.")

    def enter_book(self):
        # Method to allow the user to enter a new book into the database
        self.db = sqlite3.connect('ebookstore.db')
        self.cursor = self.db.cursor()

        # Get user input for book details
        title = input("\nEnter the book title: ")
        author = input("\nEnter the book author: ")

        try:
            qty = int(input("\nEnter the book quantity: "))
        except ValueError:
            print("\nInvalid, please make sure the quantity is a number.\n")
            return

        # Insert the new book into the 'book' table
        self.cursor.execute('''
            INSERT INTO book (title, author, qty)
            VALUES (?,?,?)
        ''', (title, author, qty))

        # Commit changes to the database and inform the user
        self.db.commit()
        print("\nBook entered successfully!\n")
        self.db.close()

    def update_book(self):
        # Method to allow the user to update the quantity of an existing book
        self.db = sqlite3.connect('ebookstore.db')
        self.cursor = self.db.cursor()

        try:
            book_id = int(
                input("\nEnter the book ID you would like to update: "))
            new_qty = int(input("\nEnter the new quantity: "))
        except ValueError:
            print("\nInvalid, Please make sure you've entered numbers only.\n")
            return

        # Check if the specified book ID exists
        self.cursor.execute('''
            SELECT id FROM book
            WHERE id IS ?
        ''', (book_id,))

        existing_book = self.cursor.fetchone()

        if existing_book is None:
            print(f"\nBook: {book_id} does not exist.\n")
        else:
            # Update the quantity of the specified book
            self.cursor.execute('''
                UPDATE book 
                SET qty = ?
                WHERE id = ?
            ''', (new_qty, book_id))
            # Commit changes to the database and inform the user
            self.db.commit()
            print(f"\n{book_id} updated successfully!\n")
            self.db.close()

    def delete_book(self):
        # Method to allow the user to delete an existing book from the database
        self.db = sqlite3.connect('ebookstore.db')
        self.cursor = self.db.cursor()

        try:
            book_id = int(
                input("\nEnter the book ID you would like to delete: "))
        except ValueError:
            print("\nInvalid, Please make sure you entered a number\n")
            return

        # Check if the specified book ID exists
        self.cursor.execute('''
            SELECT id FROM book
            WHERE id IS ?
        ''', (book_id,))

        existing_book = self.cursor.fetchone()

        if existing_book is None:
            print(f"\nBook: {book_id} does not exist.\n")
        else:
            # Delete the specified book from the 'book' table
            self.cursor.execute('''
                DELETE FROM book
                WHERE id = ?
            ''', (book_id,))
            # Commit changes to the database and inform the user
            self.db.commit()
            print("\nDeleted Sucessfully!\n")
            self.db.close()

    def search_book(self):
        # Method to allow the user to search for books based on title or author
        self.db = sqlite3.connect('ebookstore.db')
        self.cursor = self.db.cursor()

        search_book = input("\nPlease enter a Title or Author to search for: ")

        # Search for books with matching title or author
        self.cursor.execute('''
            SELECT * FROM book
            WHERE title LIKE ?
            OR author LIKE ?
        ''', ('%' + search_book + '%', '%' + search_book + '%'))

        books = self.cursor.fetchall()

        if not books:
            print("\nNo matching books found.\n")
        else:
            print("\nMatching books :\n")
            for book in books:
                print(book)
                print('\n')

        # Close the database connection
        self.db.close()


if __name__ == "__main__":
    # Create a Bookstore object and start the menu display
    bookstore = Bookstore()
    bookstore.display_menu()
