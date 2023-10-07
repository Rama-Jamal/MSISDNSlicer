from tkinter import filedialog
import tkinter as tk
import configparser
import math
import os

config = configparser.ConfigParser()
config.read('config.txt')

count1 = config.get('General','count1') #100
count2 = config.get('General','count2') #200
count3 = config.get('General','count3') #300
count4 = config.get('General','count4') #400
results_path = config.get('General','results_path')

file_path = ""

def clear_output():
    output_text.delete("1.0", "end")
    message_entry.delete("1.0", "end")
    Browse_entry.delete("1.0", "end")

def browse_file_path():
    global file_path
    file_path = filedialog.askopenfilename()
    file_name = file_path.split('/')[-1]
    file_size = os.path.getsize(file_path)
    file_size = file_size/1024

    Browse_entry.insert("1.0", f"File Name : {file_name}\n")
    Browse_entry.insert("end", f"File Size : {file_size:,.0f} KB\n")

def browse_file():
    global file_path
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.readlines()
            content = [line.strip() for line in content]
        file_name = file_path.split('/')[-1]
        file_name = file_name.split('.')[0]
        return content, file_name

def read_message():
    message = list(message_entry.get("1.0", "end-1c"))
    num_of_char = len(message)
    split_level = math.ceil((num_of_char/70))
    return num_of_char,split_level

def split_content(chunk_size,new_list,file_name):
    final_list = list()
    start = 0
    end = chunk_size

    data_per_file = len(new_list) / chunk_size
    num_of_files = math.ceil(data_per_file)  # 5

    num_of_char, split_level = read_message()

    output_text.delete("1.0", "end")  # Clear previous content
    output_text.insert("1.0", f"Message Body = {num_of_char}\n")
    output_text.insert("end", f"Number of Parts = {split_level}\n")
    output_text.insert("end", f"Number of MSISDNs = {len(new_list)}\n")
    output_text.insert("end", f"MSISDNs Per File = {chunk_size}\n")
    output_text.insert("end", f"Number of Files = {num_of_files}\n")

    for i in range(num_of_files):
        path_of_file = os.path.join(results_path, f"{file_name}_{i+1}.txt")
        if i < (num_of_files-1):
            final_list.append(new_list[start:end - 1])
            with open(path_of_file, 'w') as file:
                for val in final_list[i]:
                    file.write(val + '\n')
            start += chunk_size  # 100
            end += chunk_size  # 200

        elif i == (num_of_files-1):
            final_list.append(new_list[start:])
            with open(path_of_file, 'w') as file:
                for val in final_list[i]:
                    file.write(val + '\n')

def num_pattern():
    new_list = list()
    content,file_name = browse_file()

    for num in content:
        num.strip()
        if num.startswith("79"):
            new_list.append('962'+num)
        elif num.startswith("0"):
            val = num.split('0')[1]
            new_list.append('962'+val)
        elif num.startswith("962"):
            new_list.append(num)

    num_of_char,split_level = read_message()

    if split_level == 1:
        chunk_size = int(count1)
        split_content(chunk_size,new_list,file_name)
    elif split_level == 2:
        chunk_size = int(count2)
        split_content(chunk_size, new_list,file_name)
    elif split_level == 3:
        chunk_size = int(count3)
        split_content(chunk_size, new_list,file_name)
    elif split_level == 4:
        chunk_size = int(count4)
        split_content(chunk_size, new_list,file_name)

# Create the main window
root = tk.Tk()
root.title("File and message Reader")

# Set the background color of the window
root.configure(bg="light gray")  # Change "light gray" to your desired color

# Make the window bigger
window_width = 700
window_height = 700
root.geometry(f"{window_width}x{window_height}")

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"+{x_coordinate}+{y_coordinate}")

message_label = tk.Label(root, text="Enter message:")
message_label.pack(pady=(10, 0))

message_entry = tk.Text(root, width=60, height=10, borderwidth=2, relief="solid")
message_entry.pack(pady=(5, 0))

run_label = tk.Label(root, text="Browse File:")
run_label.pack(pady=(20, 0))

browse_button = tk.Button(root, text="Browse", command=browse_file_path, borderwidth=1, relief="solid")
browse_button.pack(pady=(5, 0))

Browse_entry = tk.Text(root, width=40, height=3, borderwidth=2, relief="solid")
Browse_entry.pack(pady=(5, 0))

run_label = tk.Label(root, text="Press the Button:")
run_label.pack(pady=(30, 0))

run_button = tk.Button(root, text="RUN", command=num_pattern, borderwidth=1, relief="solid")
run_button.pack(pady=(5, 0))

#,font=("Helvetica", 14, "bold")
output_label = tk.Label(root, text="Output:")
output_label.pack(pady=(35, 0))

output_text = tk.Text(root, width=60, height=6, borderwidth=2, relief="solid")
output_text.pack(pady=(5, 0))

clear_button = tk.Button(root, text="Clear", command=clear_output, borderwidth=1, relief="solid")
clear_button.pack(pady=(40, 0))

# Start the GUI event loop
root.mainloop()