import tkinter as tk
from tkinter import ttk

def get_clarification(original_text=""):
    """
    Opens a small window to get spelling clarification from user
    Returns the corrected text or None if cancelled
    """
    result = {"text": None}
    
    def submit():
        result["text"] = text_entry.get()
        root.destroy()
    
    def cancel():
        root.destroy()
    
    # Create the main window
    root = tk.Tk()
    root.title("Clarification")
    
    # Set window position to center
    window_width = 400
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Add padding and configure grid
    root.configure(padx=20, pady=20)
    
    # Create and pack widgets
    label = ttk.Label(root, text="Please provide Clarification:")
    label.pack(pady=5)
    
    text_entry = ttk.Entry(root, width=40)
    text_entry.insert(0, original_text)  # Insert original text
    text_entry.pack(pady=10)
    text_entry.select_range(0, tk.END)  # Select all text
    text_entry.focus()  # Focus on entry
    
    # Buttons frame
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    
    submit_btn = ttk.Button(button_frame, text="Submit", command=submit)
    submit_btn.pack(side=tk.LEFT, padx=5)
    
    cancel_btn = ttk.Button(button_frame, text="Cancel", command=cancel)
    cancel_btn.pack(side=tk.LEFT, padx=5)
    
    # Bind Enter key to submit
    root.bind('<Return>', lambda e: submit())
    # Bind Escape key to cancel
    root.bind('<Escape>', lambda e: cancel())
    
    # Start the window
    root.mainloop()
    
    return result["text"]