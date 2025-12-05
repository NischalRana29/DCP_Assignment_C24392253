# Starter code for Data Centric Programming Assignment 2025

# os is a module that lets us access the file system
# This program:
# 1. Recursively loads all .abc tune files from the abc_books/ folder
# 2. Parses them into dictionaries
# 3. Stores them in a SQLite database (tunes.db)
# 4. Loads them into pandas for quick preview
#
# Author: Nischal Rana

import os 
import sqlite3
import pandas as pd

# Path to the folder containing book directories
books_dir = "abc_books"

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


def process_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    # list comprehension to strip the \n's
    lines = [line.strip() for line in lines]

    # just print the files for now
    for line in lines:
        # print(line)
        pass


def main():
    conn = sqlite3.connect("tunes.db")
    init_db(conn)

    all_tunes = []

    for folder in os.listdir(books_dir):
        folder_path = os.path.join(books_dir, folder)

        if os.path.isdir(folder_path) and folder.isdigit():
            book_number = int(folder)
            print(f"Found book: {book_number}")

            for file in os.listdir(folder_path):
                if file.endswith(".abc"):
                    file_path = os.path.join(folder_path, file)
                    print(f"  Parsing: {file}")

                    tunes = parse_abc_file(file_path, book_number)
                    all_tunes.extend(tunes)

    insert_tunes(conn, all_tunes)
    conn.close()

    print(f"\nDone! Parsed and stored {len(all_tunes)} tunes.")

    # Load into pandas
    conn = sqlite3.connect("tunes.db")
    df = pd.read_sql("SELECT * FROM tunes", conn)
    print(df.head())
    conn.close()

if __name__ == "__main__":
    main()
