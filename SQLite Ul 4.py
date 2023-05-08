import sqlite3
import tkinter as tk
from tkinter import ttk
from ttkbootstrap.tableview import Tableview as TV

class Tableview(TV):
    _headerbg = "gray50"

    def __init__(self, *args, **kwargs):
        TV.__init__(self, *args, **kwargs)
        self._coldata = kwargs.get("coldata", [])
        self._searchable = kwargs.get("searchable", False)
        self._searchframe = None
        self._original_data = []
        self._current_data = []
        self._sorted_column = None
        self._sort_descending = False
        self._pagesize = tk.IntVar(value=kwargs.get("pagesize", 25))
        self._page_index = 0
        self._pages = []
        self._colsizes = []
        self._colanchors = []  # add this line to initialize the _colanchors attribute
        self._headerframe = None
        self._headerfont = ('Helvetica', 10, 'bold')
        self._headerfg = kwargs.get("headerfg", "black")
        self._unstretchable_columns = []
        self._displayed_rows = 0

        # Initialize the Tableview widget
        self._create_header()
        self._create_rows()

    def _sort_data(self):
        if self._sorted_column is not None:
            self._current_data.sort(key=lambda row: row[self._sorted_column], reverse=self._sort_descending)

    def update_data(self, data):
        self._original_data = data
        self._sort_data()
        self._filter_data()
        self._paginate_data()
        self._display_data()

    def _create_header(self):
        for i, col in enumerate(self._coldata):
            text = col.get("text", "")
            stretch = col.get("stretch", True)
            width = col.get("width", 100)
            anchor = col.get("anchor", "center")
            col_id = col.get("id", i)

            self._colsizes.append(width)
            self._colanchors.append(anchor)

            cell = ttk.Label(
                self._headerframe,
                text=text,
                font=self._headerfont,
                foreground=self._headerfg,
                background=self._headerbg,
                anchor=anchor,
            )

            if stretch:
                cell.grid(row=0, column=i, sticky="nsew")
                self.columnconfigure(col_id, weight=1)
            else:
                cell.grid(row=0, column=i)
                self._unstretchable_columns.append(col_id)

    def _create_rows(self):
        for i, row_data in enumerate(self._current_data):
            row_id = i + 1
            for j, value in enumerate(row_data):
                cell = ttk.Label(self, text=value, anchor=self._colanchors[j])
                cell.grid(row=row_id, column=j)

    def _display_data(self):
        for row in self.winfo_children():
            if row != self._headerframe:
                row.destroy()

        for row_data in self._pages[self._page_index]:
            row_id = self._displayed_rows + 1
            self._displayed_rows += 1
            for i, value in enumerate(row_data):
                cell = ttk.Label(self, text=value, anchor=self._colanchors[i])
                cell.grid(row=row_id, column=i)
                
    def _filter_data(self):
        if self._searchable and self._searchframe is not None:
            search_text = self._searchframe.searchbox.get()
            if search_text:
                self._current_data = [row for row in self._original_data if any(search_text.lower() in str(cell).lower() for cell in row)]
            else:
                self._current_data = self._original_data
        else:
            self._current_data = self._original_data
            
    def _paginate_data(self):
        self._pages = [self._current_data[i:i + self._pagesize.get()] for i in range(0, len(self._current_data), self._pagesize.get())]

        self._page_index = min(self._page_index, len(self._pages) - 1)
        self._display_data()



# Connect to the SQLite database file
conn = sqlite3.connect("epood_ktonisson.db")
cursor = conn.cursor()

# Fetch rows from the database
cursor.execute("SELECT * FROM ktonisson")
rows = cursor.fetchall()

# Close the database connection
conn.close()

# Create the window and the Tableview widget
my_w = tk.Tk()
my_w.geometry("800x600")  # width and height
my_w.title("Tabel")
my_w.resizable(True, True)

style = ttk.Style()
style.configure(".", font=("Helvetica", 10))
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), foreground="white", background="gray50")
style.configure("Treeview", rowheight=25, font=("Helvetica", 10), background="gray90", foreground="black")
style.map("Treeview", background=[("selected", "gray75")], foreground=[("selected", "black")], highlightthickness=[("selected", 2)])
style.configure("Horizontal.TScrollbar", gripcount=0, troughcolor="#d9d9d9", bordercolor="#d9d9d9", arrowcolor="gray50", dark=True)

# Create the insert boxes
enimi_box = ttk.Entry(my_w)
pnimi_box = ttk.Entry(my_w)
email_box = ttk.Entry(my_w)
amark_box = ttk.Entry(my_w)
amudel_box = ttk.Entry(my_w)
aaasta_box = ttk.Entry(my_w)
ahind_box = ttk.Entry(my_w)

# Add a button to submit the data to the database
def submit_data():
    # Connect to the SQLite database file
    conn = sqlite3.connect("epood_ktonisson.db")
    cursor = conn.cursor()

    # Get the values from the insert boxes
    enimi = enimi_box.get()
    pnimi = pnimi_box.get()
    email = email_box.get()
    amark = amark_box.get()
    amudel = amudel_box.get()
    aaasta = aaasta_box.get()
    ahind = ahind_box.get()

    # Insert the values into the database
    cursor.execute("INSERT INTO ktonisson (enimi, pnimi, email, amark, amudel, aaasta, ahind) VALUES (?, ?, ?, ?, ?, ?, ?)", (enimi, pnimi, email, amark, amudel, aaasta, ahind))
    conn.commit()

    # Fetch rows from the database and update the Tableview widget
    cursor.execute("SELECT * FROM ktonisson")
    rows = cursor.fetchall()
    dv.update_data(rows)

    # Close the database connection and clear the insert boxes
    conn.close()
    enimi_box.delete(0, "end")
    pnimi_box.delete(0, "end")
    email_box.delete(0, "end")
    amark_box.delete(0, "end")
    amudel_box.delete(0, "end")
    aaasta_box.delete(0, "end")
    ahind_box.delete(0, "end")

submit_button = ttk.Button(my_w, text="Submit", command=submit_data)

# Set the positions of the insert boxes and button
enimi_box.grid(row=1, column=0, padx=5, pady=5)
pnimi_box.grid(row=2, column=0, padx=5, pady=5)
email_box.grid(row=3, column=0, padx=5, pady=5)
amark_box.grid(row=4, column=0, padx=5, pady=5)
amudel_box.grid(row=5, column=0, padx=5, pady=5)
aaasta_box.grid(row=6, column=0, padx=5, pady=5)
ahind_box.grid(row=7, column=0, padx=5, pady=5)
submit_button.grid(row=8, column=0, padx=5, pady=5)

l1 = [
    {"text": "ID", "stretch": False},
    {"text":"enimi","stretch":True},
    {"text":"pnimi","stretch":True},
    {"text":"email","stretch":True},
    {"text":"amark","stretch":True},
    {"text":"amudel","stretch":True},
    {"text":"aaasta","stretch":True},
    {"text":"ahind","stretch":True},
]  # Columns with Names and style 

dv = Tableview(
    master=my_w,
    coldata=l1,
    rowdata=rows,
    searchable=True,
    pagesize=10,
    height=10,
    stripecolor=("white", None),
)

dv.grid(row=0, column=0, padx=10, pady=5)
dv.autofit_columns()


# Run the Tkinter event loop
my_w.mainloop()