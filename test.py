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
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext

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


def get_tunes_by_book(df, book_number):
    """
    return all tunes from the specified book number.
    """
    return df[df["book_number"] == book_number]

def get_tunes_by_type(df, tune_type):
    return df[df["tune_type"].str.lower() == tune_type.lower()]

def search_tunes(df, search_term):
    mask = df["title"].str.contains(search_term, case = False, na = False)
    return df[mask]


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

    #insert all parsed tunes
    insert_tunes(conn, all_tunes)
    conn.close()

    print(f"\nDone! Parsed and stored {len(all_tunes)} tunes.")

    # load dataframe for preview
    conn = sqlite3.connect("tunes.db")
    df = pd.read_sql("SELECT * FROM tunes", conn)
    print(df.head())
    conn.close()

#interactive menu
#load the tunes table into a pandas DataFrame.
def load_dataframe():
    conn = sqlite3.connect("tunes.db")
    df = pd.read_sql("SELECT * FROM tunes", conn)
    conn.close()
    return df

def show_menu():
    """Display the menu"""
    print("*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")
    print("\n--- ABC Tune Database ---")
    print("1) List all books")
    print("2) Get tunes by book")
    print("3) Get tunes by type")
    print("4) Search tunes by title")
    print("5) Show a tune's ABC text")
    print("0) Quit")
    print("*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")


def run_menu():
    """Run the interactive menu loop."""
    df = load_dataframe()  # Load data once at menu start

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\nAvailable books:")
            books = df["book_number"].unique()
            books = [int(b) for b in books]  # convert np.int64 → int
            print(sorted(books))

        elif choice == "2":
            book_num = int(input("Enter book number: "))
            result = get_tunes_by_book(df, book_num)
            print(result[["id", "title", "tune_type", "meter", "key_sig"]].head(20))

        elif choice == "3":
            tune_type = input("Enter tune type (e.g., air, reel, jig): ")
            result = get_tunes_by_type(df, tune_type)
            print(result[["id", "title", "meter", "key_sig"]].head(20))

        elif choice == "4":
            term = input("Enter title search term: ")
            result = search_tunes(df, term)
            print(result[["id", "title", "tune_type", "meter"]].head(20))

        elif choice == "5":
            tune_id = int(input("Enter tune ID: "))
            abc = df[df["id"] == tune_id]["raw_abc"]
            if abc.empty:
                print("Tune not found.")
            else:
                print("\n--- RAW ABC TEXT ---")
                print(abc.values[0])
                print("---------------------")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


def launch_gui():
    df = load_dataframe()

    root = tk.Tk()
    root.title("ABC Music Explorer")
    root.geometry("900X50")
    
    title_frame = tk.Frame(root, padx = 10, pady = 10)
    title_frame.pack(fill = "x")

    tk.label(
        title_frame, 
        text = "ABC Music Explorer",
        font = ("Times New Roman", 20, "bold")
    )



if __name__ == "__main__":
    main()
    #run_menu() #text based menu
    launch_gui()