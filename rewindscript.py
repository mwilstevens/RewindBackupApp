import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import zipfile

class RewindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rewind Backup App")

        # Set background color for root window and palette
        self.root.configure(bg="#bb86fc")
        self.root.tk_setPalette(background='#bb86fc', foreground='#bb86fc', activeBackground='#bb86fc')

        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.1)
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # Create larger font
        font = ("Helvetica", 20)
        
        self.backup_button = tk.Button(root, text="Backup Rewind", command=self.backup, font=font)
        self.backup_button.pack(side=tk.LEFT, padx=5)
        
        self.restore_button = tk.Button(root, text="Restore Rewind from Zip", command=self.restore, font=font)
        self.restore_button.pack(side=tk.RIGHT, padx=5)
        
    def backup(self):
        try:
            backup_folder = os.path.expanduser("~/Library/Application Support/com.memoryvault.MemoryVault")
            if not os.path.exists(backup_folder):
                self.show_error("Backup folder not found")
                return

            now = datetime.now()
            timestamp = now.strftime("%d%m%Y_%H%M")
            backup_name = f"Rewind_backup_{timestamp}.zip"
            desktop_path = os.path.expanduser("~/Desktop")

            with zipfile.ZipFile(backup_name, "w") as zipf:
                for root, dirs, files in os.walk(backup_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, backup_folder))

            shutil.move(backup_name, os.path.join(desktop_path, backup_name))
            self.show_info("Backup completed and moved to Desktop")

        except Exception as e:
            self.show_error(str(e))

    def restore(self):
        try:
            zip_path = filedialog.askopenfilename(title="Select Rewind Backup ZIP", filetypes=[("ZIP files", "*.zip")])
            if not zip_path:
                return

            restore_folder = os.path.expanduser("~/Library/Application Support/com.memoryvault.MemoryVault")
            if os.path.exists(restore_folder):
                overwrite = messagebox.askyesno("Confirmation", "Restore folder already exists. Overwrite?")
                if not overwrite:
                    return
                shutil.rmtree(restore_folder)

            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(restore_folder)

            self.show_info("Restore completed")

        except Exception as e:
            self.show_error(str(e))

    def show_info(self, message):
        messagebox.showinfo("Info", message)

    def show_error(self, error_msg):
        messagebox.showerror("Error", error_msg, icon="error")

if __name__ == "__main__":
    gui = tk.Tk(className='Rewind Backup App')
    gui.geometry("400x200")
    gui['background']='#bb86fc'
    gui['bg']='#bb86fc'

    app = RewindApp(gui)
    gui.mainloop()
