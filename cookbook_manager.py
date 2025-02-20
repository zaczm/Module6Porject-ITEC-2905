# Use sqlite database
import sqlite3
from sqlite3 import Error
from datetime import datetime

def create_connection():
    """Create a database connection"""
    conn = None
    try:
        conn = sqlite3.connect('hipster_cookbooks.db')
        print("Successfully connected to SQLite database")
        return conn
    except Error as e:
        print(f"Error establishing connection with the void: {e}")
        return None

def drop_all_tables(conn):
    """Drop all existing tables to start fresh"""
    try:
        cursor = conn.cursor()
        # Drop tables in correct order (due to foreign key constraints)
        cursor.execute("DROP TABLE IF EXISTS cookbook_tags")
        cursor.execute("DROP TABLE IF EXISTS tags")
        cursor.execute("DROP TABLE IF EXISTS borrowing_history")
        cursor.execute("DROP TABLE IF EXISTS cookbooks")
        conn.commit()
        print("All tables dropped successfully")
    except Error as e:
        print(f"Error dropping tables: {e}")

def create_table(conn):
    """Create a table structure"""
    try:
        sql_create_cookbooks_table = """
        CREATE TABLE IF NOT EXISTS cookbooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year_published INTEGER,
            aesthetic_rating INTEGER,
            instagram_worthy BOOLEAN,
            cover_color TEXT
        );"""

        # Calling the contructor for the cursor object to create a new cursor
        cursor = conn.cursor()
        cursor.execute(sql_create_cookbooks_table)
        print("Successfully created a database structure")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_cookbook(conn, cookbook):
    """Add a new cookbook to your shelf"""
    sql = '''INSERT INTO cookbooks(title, author, year_published, aesthetic_rating, instagram_worthy, cover_color)
             VALUES(?,?,?,?,?,?)'''
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, cookbook)
        conn.commit()
        print(f"Successfully curated cookbook with id: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"Error adding to collection: {e}")
        return None

def get_all_cookbooks(conn):
    """Browse your entire collection"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cookbooks")
        books = cursor.fetchall()
        
        for book in books:
            print(f"ID: {book[0]}")
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Published: {book[3]} (vintage is better)")
            print(f"Aesthetic Rating: {'✨' * book[4]}")
            print(f"Instagram Worthy: {'📸 Yes' if book[5] else 'Not aesthetic enough'}")
            print(f"Cover Color: {book[6]}")
            print("---")
        return books
    except Error as e:
        print(f"Error retrieving collection: {e}")
        return []

def create_tag_tables(conn):
    """Create tables for recipe tagging"""
    try:
        # Create tags table
        sql_create_tags = """
        CREATE TABLE IF NOT EXISTS tags (
            tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name TEXT NOT NULL UNIQUE
        );"""

        # Create cookbook-tags relationship table
        sql_create_cookbook_tags = """
        CREATE TABLE IF NOT EXISTS cookbook_tags (
            cookbook_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (cookbook_id) REFERENCES cookbooks (id),
            FOREIGN KEY (tag_id) REFERENCES tags (tag_id),
            PRIMARY KEY (cookbook_id, tag_id)
        );"""

        cursor = conn.cursor()
        cursor.execute(sql_create_tags)
        cursor.execute(sql_create_cookbook_tags)
        print("Successfully created tag tables")
    except Error as e:
        print(f"Error creating tag tables: {e}")

def add_recipe_tags(conn, cookbook_id, tags):
    """Add tags to a cookbook (e.g., 'gluten-free', 'plant-based', 'artisanal')"""
    try:
        cursor = conn.cursor()
        # Validate cookbook exists
        cursor.execute("SELECT id FROM cookbooks WHERE id = ?", (cookbook_id,))
        if not cursor.fetchone():
            print(f"Error: Cookbook {cookbook_id} not found")
            return False

        # Add each tag
        for tag in tags:
            cursor.execute("INSERT OR IGNORE INTO tags (tag_name) VALUES (?)", (tag.lower(),))
            cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (tag.lower(),))
            tag_id = cursor.fetchone()[0]
            
            # Link tag to cookbook
            cursor.execute("""
                INSERT OR IGNORE INTO cookbook_tags (cookbook_id, tag_id)
                VALUES (?, ?)
            """, (cookbook_id, tag_id))

        conn.commit()
        print(f"Successfully added tags {tags} to cookbook {cookbook_id}")
        return True
    except Error as e:
        print(f"Error adding tags: {e}")
        return False

def create_borrowing_table(conn):
    """Create table for tracking borrowed cookbooks"""
    try:
        sql_create_borrowing = """
        CREATE TABLE IF NOT EXISTS borrowing_history (
            borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cookbook_id INTEGER,
            friend_name TEXT NOT NULL,
            date_borrowed DATE NOT NULL,
            date_returned DATE,
            FOREIGN KEY (cookbook_id) REFERENCES cookbooks (id)
        );"""
        
        cursor = conn.cursor()
        cursor.execute(sql_create_borrowing)
        print("Successfully created borrowing history table")
    except Error as e:
        print(f"Error creating borrowing table: {e}")

def track_borrowed_cookbook(conn, cookbook_id, friend_name, date_borrowed):
    """Track which friend borrowed your cookbook and when"""
    try:
        # Input validation
        if not friend_name or not friend_name.strip():
            print("Error: Friend name cannot be empty")
            return False
            
        cursor = conn.cursor()
        # Validate cookbook exists
        cursor.execute("SELECT id FROM cookbooks WHERE id = ?", (cookbook_id,))
        if not cursor.fetchone():
            print(f"Error: Cookbook {cookbook_id} not found")
            return False
            
        # Check if already borrowed
        cursor.execute("""
            SELECT borrow_id FROM borrowing_history 
            WHERE cookbook_id = ? AND date_returned IS NULL
        """, (cookbook_id,))
        if cursor.fetchone():
            print(f"Error: Cookbook {cookbook_id} is already borrowed")
            return False
            
        # Record the borrowing
        cursor.execute("""
            INSERT INTO borrowing_history (cookbook_id, friend_name, date_borrowed)
            VALUES (?, ?, ?)
        """, (cookbook_id, friend_name, date_borrowed))
            
        conn.commit()
        print(f"Successfully tracked cookbook {cookbook_id} borrowed by {friend_name}")
        return True
    except Error as e:
        print(f"Error tracking borrowed cookbook: {e}")
        return False

def main():
    # Establish connection to our artisanal database
    conn = create_connection()
    
    if conn is not None:
        # Drop existing tables first
        drop_all_tables(conn)
        
        # Create all necessary tables
        create_table(conn)
        create_tag_tables(conn)
        create_borrowing_table(conn)
        
        # Insert some carefully curated sample cookbooks
        cookbooks = [
            ('Foraged & Found: A Guide to Pretending You Know About Mushrooms', 
             'Oak Wavelength', 2023, 5, True, 'Forest Green'),
            ('Small Batch: 50 Recipes You will Never Actually Make', 
             'Sage Moonbeam', 2022, 4, True, 'Raw Linen'),
            ('The Artistic Toast: Advanced Avocado Techniques', 
             'River Wildflower', 2023, 5, True, 'Recycled Brown'),
            ('Fermented Everything', 
             'Jim Kombucha', 2021, 3, True, 'Denim'),
            ('The Deconstructed Sandwich: Making Simple Things Complicated', 
             'Juniper Vinegar-Smith', 2023, 5, True, 'Beige')
        ]
        
        print("\nCurating your cookbook collection...")
        cookbook_ids = []
        for cookbook in cookbooks:
            cookbook_id = insert_cookbook(conn, cookbook)
            if cookbook_id:
                cookbook_ids.append(cookbook_id)
        
        # Test new features
        print("\nTesting new features...")
        add_recipe_tags(conn, cookbook_ids[0], ['foraging', 'sustainable'])
        add_recipe_tags(conn, cookbook_ids[1], ['minimalist', 'artisanal'])
        
        track_borrowed_cookbook(conn, cookbook_ids[0], "Luna Moonbeam", "2024-02-19")
        track_borrowed_cookbook(conn, cookbook_ids[2], "Cedar Starlight", "2024-02-15")
        
        print("\nYour carefully curated collection:")
        get_all_cookbooks(conn)
        
        conn.close()
        print("\nDatabase connection closed")
    else:
        print("Error! The universe is not aligned for database connections right now.")

if __name__ == '__main__':
    main()