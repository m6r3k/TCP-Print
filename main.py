"""
MIT License

Copyright (c) 2024 M6r3k

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import tkinter as tk
import socket
import json

def send_message_tcp():
    host = host_entry.get()
    port = int(port_entry.get() or 9100)  # Use default port 9100 if not provided
    my_text = text_entry.get()

    selected_template = template_var.get()

    # Read message templates from config file
    with open('config.json') as f:
        templates = json.load(f)

    # Select the appropriate message template
    message_template = templates.get(selected_template)
    if message_template is None:
        return  # No template selected

    message = message_template.replace("{MYTEXT}", my_text)

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Connect to the server
            s.connect((host, port))
            # Send the message
            s.sendall(message.encode())
            status_label.config(text="Message sent successfully.")
        except Exception as e:
            # Adjusting the error message for newline
            status_label.config(text=f"Error: {e}", wraplength=200)


# Create the main window
root = tk.Tk()
root.title("SN re-printer")

# Set the dimensions of the main window
root.geometry("250x250")  # Set width=400 pixels and height=200 pixels

# Create and place widgets
host_label = tk.Label(root, text="Host:")
host_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
host_entry = tk.Entry(root)
host_entry.grid(row=0, column=1, padx=5, pady=5)

port_label = tk.Label(root, text="Port:")
port_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=5, pady=5)
port_entry.insert(tk.END, "9100")  # Set default port

text_label = tk.Label(root, text="Text:")
text_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
text_entry = tk.Entry(root)
text_entry.grid(row=2, column=1, padx=5, pady=5)

template_label = tk.Label(root, text="Select label size:")
template_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
template_var = tk.StringVar()
template_var.set("5x5")
template_menu = tk.OptionMenu(root, template_var, "5x5", "6x6", "15x15")
template_menu.grid(row=3, column=1, padx=5, pady=5)

send_button = tk.Button(root, text="Print", command=send_message_tcp)
send_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

status_label = tk.Label(root, text="", anchor="center", wraplength=200)
status_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Start the GUI main loop
root.mainloop()
