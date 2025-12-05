# Starter code for Data Centric Programming Assignment 2025

# os is a module that lets us access the file system

# Bryan Duggan likes Star Trek
# Bryan Duggan is a great flute player

import os 
import sqlite3
import pandas as pd

# sqlite for connecting to sqlite databases
# database steup 
def init_db(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tunes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_number INTEGER,
            file_name TEXT, 
            tune_index INTEGER,
            ref_number TEXT, 
            title TEXT, 
            tune_type TEXT, 
            meter TEXT, 
            key_sig TEXT, 
            raw_abc TEXT
        )
        """
    )
    conn.commit()

def insert_tunes(conn, tunes):
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO tunes(
            book_number,
            file_name,
            tune_index,
            ref_number,
            title,
            tune_type,
            meter,
            key_sig,
            raw_abc
        )
        VALUES (
            :book_number,
            :file_name,
            :tune_index,
            :ref_number,
            :title,
            :tune_type,
            :meter,
            :key_sig,
            :raw_abc
        )
        """,
        tunes
    )
    conn.commit()

# parsing function
def parse_abc_tune(lines):
    tune ={
        "ref_number": None,
        "title": None,
        "tune_type": None,
        "meter": None,
        "key_sig": None,
        "raw_abc": "\n".join(lines)
    }

    for line in lines:
        if line.startswith("X:"):
            tune["ref_number"] = line[2:].strip()
        elif line.startswith("T:"):
            tune["title"] = line[2:].strip()
        elif line.startswith("R:"):
            tune["tune_type"] = line[2:].strip()
        elif line.startswith("M:"):
            tune["meter"] = line[2:].strip()
        elif line.startswith("K:"):
            tune["key_sig"] = line[2:].strip()

    return tune


def parse_abc_file(file_path, book_number):
    with open(file_path, "r") as f:
        lines = f.readlines()

    all_tunes = []
    current = []
    tune_index = 0

    for line in lines:
        line_strip = line.rstrip("\n")

        if line_strip.startswith("X:") and current:
            tune = parse_abc_tune(current)
            tune["book_number"] = book_number
            tune["file_name"] = os.path.basename(file_path)
            tune["tune_index"] = tune_index
            all_tunes.append(tune)
            tune_index += 1
            current = []

        current.append(line_strip)

    if current:
        tune = parse_abc_tune(current)
        tune["book_number"] = book_number
        tune["file_name"] = os.path.basename(file_path)
        tune["tune_index"] = tune_index
        all_tunes.append(tune)

    return all_tunes
    
# An example of how to create a table, insert data
# and run a select query
def do_databasse_stuff():

    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)')

    # Insert data
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('John', 30))

    # Save changes
    conn.commit()

    cursor.execute('SELECT * FROM users')

    # Get all results
    results = cursor.fetchall()

    # Print results
    for row in results:
        print(row)    
        print(row[0])
        print(row[1])
    # Close
    
    df = pd.read_sql("SELECT * FROM users", conn)
    print(df.head())
    conn.close()    

books_dir = "abc_books"

def process_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    # list comprehension to strip the \n's
    lines = [line.strip() for line in lines]

    # just print the files for now
    for line in lines:
        # print(line)
        pass

# do_databasse_stuff()

# Iterate over directories in abc_books
for item in os.listdir(books_dir):
    # item is the dir name, this makes it into a path
    item_path = os.path.join(books_dir, item)
    
    # Check if it's a directory and has a numeric name
    if os.path.isdir(item_path) and item.isdigit():
        print(f"Found numbered directory: {item}")
        
        # Iterate over files in the numbered directory
        for file in os.listdir(item_path):
            # Check if file has .abc extension
            if file.endswith('.abc'):
                file_path = os.path.join(item_path, file)
                print(f"  Found abc file: {file}")
                process_file(file_path)
                
