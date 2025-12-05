# Data Centric Programming Assignment 2025

- [Assignment Brief](assignment.md)

Name: Nischal Rana

Student Number: C24392253

#Folder structure
DCP_ASSIGNMENT_C24392253/
│
├── abc_books/
│   ├── 1/
│   │    ├── *.abc
│   ├── 2/
│        ├── *.abc
│
├── images/
│   ├── screenshot1.png
│   ├── SSChoice1.png
│   ├── SSChoice2.png
│   ├── SSChoice3.png
│   ├── SSChoice4.png
│   ├── SSChoice5.png
│   ├── SSforchoice0.png
│   ├── SSParsingBook1.png
│   └── SSParsingBook2.png
├── starter_code.py      
├── main.py              
├── test.py 
├──	star_map3.py
├── albums_lab.py             
├── tunes.db             
├── README.md            
├── assignment.md        
├── LICENSE
└── .gitignore


# Screenshots
![MAIN MENU](images/screenshot1.png)
![Choice1](images/SSChoice1.png)
![Choice2](images/SSChoice2.png)
![Choice3](images/SSChoice3.png)
![Choice4](images/SSChoice4.png)
![Choice5](images/SSforchoice5.png)
![Choice0](images/SSforchoice0.png)
![ParsingBook1](images/SSParsingBook1.png)
![ParsingBook2](images/SSParsingBook2.png)


# Description of the project
The project is a complete data-driven program that evaluates and processes classic songs in the format of abc notation. A directory of music "books", each of which has several.abc files, is automatically scanned by the application. The program must accurately recognise and parse tune borders using ABC headers like X:, T:, R:, M:, and K: because each file may include one or more songs.

Each song is processed, then stored in a SQLite database (tunes.db) as a structured Python dictionary. All significant metadata, such as the book number, tune index, title, tune type, meter, key signature, and the complete raw ABC text, are recorded in the database structure.

The stored data is subsequently loaded and analysed using a pandas DataFrame, allowing queries like:
*Listing every song in a particular book
*Sorting music by genre (air, reel, jig, etc.)
*Title-based music search (case-insensitive)
*Seeing the complete ABC notation for any song

Additionally, the project has an interactive user interface that can be accessed as an optional Tkinter GUI or as a text-based menu. Without writing any code, these interfaces make it simple for users to browse books, find music, filter results, and display ABC notation.

# Instructions for use
Menu Options
1) List all books
	Displays all available book numbers found in the dataset.

2) Get tunes by book
	Prompts you to enter a book number (e.g., 0, 1, 2).
	The program then displays the first 20 tunes from that book, including:
		*Tune ID
		*Title
		*Tune type
		*Meter
		*Key signature

3) Get tunes by type

4) Search tunes by title

5) Show a tune’s ABC text
	Prompts you to enter a Tune ID.
	You can see Tune IDs in results from options 2–4.

0) Quits the program

# How it works:
This project processes traditional music tunes in ABC notation, utilizing file handling, text parsing, SQL databases, and user interaction to automatically load, parse, store, analyze, and display these tunes through a multi-stage workflow.

for folder in os.listdir(books_dir): scans the ABC_books and loads the ABC files.

# List of files in the project

| Files | Source |
|-----------|-----------|
| main.py | Self written |
| starter_code.py | Modified from [reference]() |
| test.py | From [reference](albums_lab.py) |

# References
* ![w3schools](https://www.w3schools.com/python/pandas/default.asp)
* [![YouTube](http://img.youtube.com/vi/lyoyTlltFVU/0.jpg)](https://www.youtube.com/watch?v=lyoyTlltFVU)
* ![Stack Overflow](https://stackoverflow.com/questions/110923/how-do-i-close-a-tkinter-window)


# What I am most proud of in the assignment
- Built a complete data pipeline from raw ABC text files to working database. 
- Parsed hundreds of tunes into a structure format.

# What I learned
I learn how to read and combine data from multiple files, parse plain text to extract structured values, and store everything in a SQLite database using tables, inserts, and queries. i also gained experience loading and filtering data with Pandas, building an interactive menu for searching the data.






