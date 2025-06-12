import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
import json
import os

BG_COLOR = "#121212"
FG_COLOR = "#e0e0e0"
ENTRY_BG = "#1e1e1e"
HIGHLIGHT = "#2e2e2e"
BUTTON_BG = "#292929"
BUTTON_FG = "#ffffff"

root = tk.Tk()
root.title("AstroLogger")
root.geometry("1000x700")
root.configure(bg=BG_COLOR)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = min(1000, int(screen_width * 0.9))
window_height = min(700, int(screen_height * 0.9))

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.configure("TNotebook.Tab", background=HIGHLIGHT, foreground=FG_COLOR, padding=10)
style.map("TNotebook.Tab", background=[("selected", BUTTON_BG)])
style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 11))
style.configure("TButton", background=BUTTON_BG, foreground=BUTTON_FG, padding=6)
style.map("TButton", background=[("active", HIGHLIGHT)])
style.configure("TEntry", fieldbackground=ENTRY_BG, background=ENTRY_BG, foreground=FG_COLOR)

tab_control = ttk.Notebook(root)
tab_current = tk.Frame(tab_control, bg=BG_COLOR)
tab_stored = tk.Frame(tab_control, bg=BG_COLOR)

tab_control.add(tab_current, text="Current Log")
tab_control.add(tab_stored, text="Stored Logs")
tab_control.pack(expand=1, fill="both", padx=5, pady=5)

# tabs layout
labels = ["Time/Date", "Weather", "Target", "Class", "Specs"]
entries = {}

for idx, field in enumerate(labels):
    ttk.Label(tab_current, text=f"{field}:").grid(row=idx + 1, column=0, sticky="e", padx=15, pady=10)
    entry = ttk.Entry(tab_current, width=50)
    entry.grid(row=idx + 1, column=1, sticky="w", padx=10, pady=10)
    entries[field] = entry

ttk.Label(tab_current, text="Notes:").grid(row=6, column=0, sticky="ne", padx=15, pady=10)
notes_box = scrolledtext.ScrolledText(tab_current, width=58, height=6, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, wrap=tk.WORD)
notes_box.grid(row=6, column=1, padx=10, pady=10, sticky="w")

ttk.Label(tab_current, text="Image Preview:",relief= "raised").grid(row=0, column=2, padx=20, pady=10)
preview_frame = tk.Frame(tab_current, width=300, height=300, bg=ENTRY_BG)
preview_frame.grid(row=2, column=2, rowspan=5, padx=20, pady=10)
preview_frame.grid_propagate(False)

image_preview = tk.Label(preview_frame, bg=ENTRY_BG, fg=FG_COLOR, relief="groove")
image_preview.place(relx=0.5, rely=0.5, anchor='center')
image_preview.config(text="[ No Image Loaded ]")

image_path = None  
thumbnail_cache = None

def upload_image():
    global image_path, thumbnail_cache
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if file_path:
        image_path = file_path
        img = Image.open(file_path)
        img.thumbnail((280, 280))
        thumbnail_cache = ImageTk.PhotoImage(img)
        image_preview.config(image=thumbnail_cache, text="")

upload_btn = ttk.Button(tab_current, text="Upload Image", command=upload_image)
upload_btn.grid(row=7, column=2, padx=20, pady=10)

def reset_log():
    for entry in entries.values():
        entry.delete(0, tk.END)

    notes_box.delete("1.0", tk.END)

    image_preview.config(image='', text="[ No Image Loaded ]")
    image_preview.image = None

    global image_path
    image_path = None

def save_log():
    log_data = {label: entries[label].get() for label in entries}
    log_data["Notes"] = notes_box.get("1.0", tk.END).strip()
    log_data["Image"] = image_path if image_path else None

    logs = []
    if os.path.exists("logs.json"):
        with open("logs.json", "r") as f:
            logs = json.load(f)

    logs.append(log_data)

    with open("logs.json", "w") as f:
        json.dump(logs, f, indent=4)

    print("🔭 Log Saved.")
    refresh_logs()

button_frame = tk.Frame(tab_current, bg=BG_COLOR)
button_frame.grid(row=9, column=0, columnspan=3, pady=20)

save_button = tk.Button(button_frame, text="Save Log", bg=BG_COLOR, fg= FG_COLOR,
                        font=("Helvetica", 10, "bold"), command=save_log)
save_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(button_frame, text="Reset", bg=BG_COLOR, fg= FG_COLOR,
                         font=("Helvetica", 10, "bold"), command=reset_log)
reset_button.grid(row=0, column=1, padx=5)

stored_logs = []
log_list_frame = tk.Frame(tab_stored, bg=BG_COLOR)
log_list_frame.pack(padx=20, pady=20, fill="both", expand=True)

log_listbox = tk.Listbox(log_list_frame, bg=ENTRY_BG, fg=FG_COLOR, font=("Segoe UI", 11),
                         selectbackground=HIGHLIGHT, activestyle="none")
log_listbox.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(log_list_frame, command=log_listbox.yview)
scrollbar.pack(side="right", fill="y")
log_listbox.config(yscrollcommand=scrollbar.set)

log_preview_frame = tk.Frame(tab_stored, bg=BG_COLOR)
log_preview_frame.pack(pady=10, fill="both")

log_text = tk.Text(log_preview_frame, width=60, height=15, bg=ENTRY_BG, fg=FG_COLOR, wrap=tk.WORD)
log_text.pack(side="left", padx=10)

log_image_label = tk.Label(log_preview_frame, bg=BG_COLOR)
log_image_label.pack(side="left", padx=10)

thumbnail_cache_stored = None

def refresh_logs():
    log_listbox.delete(0, tk.END)
    global stored_logs
    stored_logs = []

    if not os.path.exists("logs.json"):
        return

    with open("logs.json", "r") as f:
        stored_logs = json.load(f)

    for log in stored_logs:
        date = log.get("Time/Date", "No Date")
        target = log.get("Target", "No Target")
        log_listbox.insert(tk.END, f"{date} - {target}")

def on_log_select(event):
    global thumbnail_cache_stored
    selection = log_listbox.curselection()
    if not selection:
        return

    idx = selection[0]
    log = stored_logs[idx]

    log_text.delete("1.0", tk.END)
    for key, value in log.items():
        if key != "Image":
            log_text.insert(tk.END, f"{key}: {value}\n")

    image_path = log.get("Image")
    if image_path and os.path.exists(image_path):
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        thumbnail_cache_stored = ImageTk.PhotoImage(img)
        log_image_label.config(image=thumbnail_cache_stored)
    else:
        log_image_label.config(image="", text="[ No Image ]")

def delete_log():
    selection = log_listbox.curselection()
    if not selection:
        return
    
    idx = selection[0]
 
    confirm = tk.messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this log?")
    if not confirm:
        return
    
    stored_logs.pop(idx)

    with open("logs.json", "w") as f:
        json.dump(stored_logs, f, indent=4)
 
    refresh_logs()
    log_text.delete("1.0", tk.END)
    log_image_label.config(image="", text="")

def edit_log():
    selection = log_listbox.curselection()
    if not selection:
        return
    
    idx = selection[0]
    log = stored_logs[idx]
    
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Log")
    edit_window.configure(bg=BG_COLOR)
    edit_window.geometry("600x500")

    edit_window.geometry(f"+{root.winfo_rootx() + 50}+{root.winfo_rooty() + 50}")

    edit_entries = {}
    row = 0
    
    for key, value in log.items():
        if key != "Image" and key != "Notes":
            ttk.Label(edit_window, text=f"{key}:").grid(row=row, column=0, sticky="e", padx=15, pady=10)
            entry = ttk.Entry(edit_window, width=50)
            entry.insert(0, value)
            entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
            edit_entries[key] = entry
            row += 1
    
    ttk.Label(edit_window, text="Notes:").grid(row=row, column=0, sticky="ne", padx=15, pady=10)
    notes_edit = scrolledtext.ScrolledText(edit_window, width=50, height=6, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, wrap=tk.WORD)
    notes_edit.grid(row=row, column=1, padx=10, pady=10, sticky="w")
    notes_edit.insert("1.0", log.get("Notes", ""))
    
    def save_edit():
        for key in edit_entries:
            log[key] = edit_entries[key].get()
        
        log["Notes"] = notes_edit.get("1.0", tk.END).strip()
        
        with open("logs.json", "w") as f:
            json.dump(stored_logs, f, indent=4)
        
        print("🔭 Log Edited.")
        refresh_logs()
        edit_window.destroy()
    
    save_edit_btn = ttk.Button(edit_window, text="💾 Save Changes", command=save_edit)
    save_edit_btn.grid(row=row+1, column=1, pady=20, sticky="e")

log_buttons_frame = tk.Frame(tab_stored, bg=BG_COLOR)
log_buttons_frame.pack(pady=10)

edit_btn = ttk.Button(log_buttons_frame, text="✏️ Edit Log", command=edit_log)
edit_btn.pack(side="left", padx=10)

delete_btn = ttk.Button(log_buttons_frame, text="🗑️ Delete Log", command=delete_log)
delete_btn.pack(side="left", padx=10)

log_listbox.bind("<<ListboxSelect>>", on_log_select)

#load the logs
refresh_logs()

root.mainloop()
