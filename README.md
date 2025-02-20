# Module6Project-ITEC-2905
Module 6 Project: SQL and SQLite

## Features Implemented

### 1. Recipe Tagging System
* Created tags table with many-to-many relationship
* Implemented tag addition functionality
* Returns success/failure status for operations
* Example: `add_recipe_tags(conn, cookbook_id, ['foraging', 'sustainable'])`

### 2. Cookbook Borrowing Tracker
* Created borrowing history table
* Added borrowing record functionality
* Includes borrowing date tracking
* Example: `track_borrowed_cookbook(conn, cookbook_id, "Luna Moonbeam", "2024-02-19")`

## How to Run Your Code

1. Make sure Python is installed on your system
2. Open a terminal/command prompt
3. Navigate to the project directory
4. Run the command:
```shell
python cookbook_manager.py

Known Limitations/Issues
Database Limitations

Tables are dropped and recreated each time the program runs
Sample data is reinserted on every run

Tag System Limitations

Cannot delete or modify tags once added
Tags are automatically converted to lowercase
No way to search by tags

Borrowing System Limitations

No functionality to return books
Cannot modify borrowing records once created
Date must be in YYYY-MM-DD format only
