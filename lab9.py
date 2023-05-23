import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


cnx = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)
cursor = cnx.cursor()

with open('Marvel.txt', 'r') as file:
    for line in file:
        line = line.strip().split('   ')  # Use three spaces as the delimiter

        if len(line) == 4:
            movie_id, movie_name, movie_date, movie_phase = line

        cursor.execute("CREATE TABLE IF NOT EXISTS marvel_movies ("
                       "id INT PRIMARY KEY,"
                       "movie_name VARCHAR(255),"
                       "release_date VARCHAR(15),"
                       "mcu_phase VARCHAR(10)"
                       ")")

        insert_query = "INSERT INTO marvel_movies (id, movie_name, release_date, mcu_phase) " \
                           "VALUES (%s, %s, %s, %s)"
        data = (int(movie_id), movie_name.strip(), movie_date.strip(), movie_phase.strip())
        cursor.execute(insert_query, data)
        cnx.commit()

cursor.close()
cnx.close()


def add_button_clicked():
    popup_window = tk.Toplevel(root)
    popup_window.title("Add Data")
    popup_window.geometry("300x200")

    id_label = tk.Label(popup_window, text="ID:")
    id_label.pack()
    id_entry = tk.Entry(popup_window)
    id_entry.pack()

    movie_label = tk.Label(popup_window, text="Movie:")
    movie_label.pack()
    movie_entry = tk.Entry(popup_window)
    movie_entry.pack()

    date_label = tk.Label(popup_window, text="Date:")
    date_label.pack()
    date_entry = tk.Entry(popup_window)
    date_entry.pack()

    phase_label = tk.Label(popup_window, text="MCU Phase:")
    phase_label.pack()
    phase_entry = tk.Entry(popup_window)
    phase_entry.pack()

    def add_data_to_database():
        id_val = id_entry.get()
        movie_val = movie_entry.get()
        date_val = date_entry.get()
        phase_val = phase_entry.get()

        if id_val and movie_val and date_val and phase_val:
            connection = mysql.connector.connect(
                host="your_host",
                user="your_username",
                password="your_password",
                database="your_database"
            )

            cursor = connection.cursor()

            sql = "INSERT INTO marvel_movies (id, movie_name, release_date, mcu_phase) VALUES (%s, %s, %s, %s)"
            values = (id_val, movie_val, date_val, phase_val)
            cursor.execute(sql, values)
            connection.commit()

            messagebox.showinfo("Success", "Data added successfully")

            cursor.close()
            connection.close()

            popup_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled")

    button_frame = tk.Frame(popup_window)
    button_frame.pack(pady=10)

    ok_button = tk.Button(button_frame, text="Ok", command=add_data_to_database)
    ok_button.pack(side="left", padx=5)

    cancel_button = tk.Button(button_frame, text="Cancel", command=popup_window.destroy)
    cancel_button.pack(side="left", padx=5)

def list_all_button_clicked():
    try:
        cnx = mysql.connector.connect(
            host="your_host",
            user="your_username",
            password="your_password",
            database="your_database"
        )
        cursor = cnx.cursor()

        query = "SELECT * FROM marvel_movies"
        cursor.execute(query)
        rows = cursor.fetchall()

        textbox.delete(1.0, tk.END)

        for row in rows:
            textbox.insert(tk.END, f"{row}\n")

        cursor.close()
        cnx.close()

    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)


connection = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM marvel_movies")
rows = cursor.fetchall()
data = {str(row[0]): {'MOVIE': row[1], 'DATE': row[2], 'PHASE': row[3]} for row in rows}
options = [str(row[0]) for row in rows]

cursor.close()
connection.close()

def dropdown_selection_changed(event):
    selected_id = dropdown.get()
    textbox.delete(1.0, tk.END)
    if selected_id in data:
        movie = data[selected_id]['MOVIE']
        date = data[selected_id]['DATE']
        phase = data[selected_id]['PHASE']
        textbox.insert(tk.END, f"ID: {selected_id}\nMovie: {movie}\nDate: {date}\nPhase: {phase}")

root = tk.Tk()
root.title("Interface")
root.geometry("500x800")

container = ttk.Frame(root, padding=20)
container.grid()

dropdown = ttk.Combobox(container, values= options)
dropdown.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
dropdown.bind("<<ComboboxSelected>>", dropdown_selection_changed)

textbox = tk.Text(container, height=40, width=50)
textbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

add_button = ttk.Button(container, text="Add", command=add_button_clicked)
add_button.grid(row=2, column=0, padx=10, pady=5)

list_all_button = ttk.Button(container, text="List All", command=list_all_button_clicked)
list_all_button.grid(row=2, column=1, padx=10, pady=5)

root.mainloop()
