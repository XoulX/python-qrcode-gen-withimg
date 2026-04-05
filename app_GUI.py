import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import io
import os

class SimpleQRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Logo QR Code Generator")
        self.root.geometry("400x520")
        self.root.resizable(False, False)
        
        self.logo_path = None
        self.generated_image = None
        
        # URL Input
        tk.Label(root, text="Enter URL:").pack(pady=(20, 5))
        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.pack(pady=5)
        
        # Logo Selection
        tk.Label(root, text="Select Logo Image:").pack(pady=(15, 5))
        self.select_btn = tk.Button(root, text="Browse...", command=self.select_logo)
        self.select_btn.pack(pady=5)
        
        self.logo_label = tk.Label(root, text="No file selected")
        self.logo_label.pack()
        
        # Generate Button
        self.generate_btn = tk.Button(
            root, 
            text="Generate QR Code", 
            command=self.generate_qr,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            height=2,
            width=20
        )
        self.generate_btn.pack(pady=20)
        
        # Preview Area
        self.preview_label = tk.Label(root, text="")
        self.preview_label.pack(pady=10)
        
        # Save Button (initially hidden)
        self.save_btn = tk.Button(
            root,
            text="Save QR Code",
            command=self.save_qr,
            state=tk.DISABLED
        )
        self.save_btn.pack(pady=5)
        
    def select_logo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.logo_path = file_path
            filename = os.path.basename(file_path)
            self.logo_label.config(text=f"Selected: {filename}")
            
    def generate_logo_qr(self, data, logo_image):
        img = qrcode.make(data)
        type(img)
        print("QR code created")

        img = img.convert('RGBA')
        width, height = img.size
      
        logo_size = min(width, height) // 5 
        xmin = (width - logo_size) // 2
        ymin = (height - logo_size) // 2
        logo = logo_image.resize((logo_size, logo_size) , Image.Resampling.LANCZOS)

        # Change RGB value to appropriate background colour you want
        background = Image.new('RGBA', (logo_size, logo_size), (255, 255, 255, 230))
        img.paste(background, (xmin, ymin), background)
        img.paste(logo, (xmin, ymin), logo)

        
        
        return img
        
    def generate_qr(self):
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        if not self.logo_path:
            messagebox.showerror("Error", "Please select a logo image")
            return
            
        # Add https if no protocol
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
            
        try:
            # Load logo
            logo = Image.open(self.logo_path)
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')

            print("loaded")
            
            # Generate QR
            qr_image = self.generate_logo_qr(url, logo)
            self.generated_image = qr_image

            print("generated")
            
            # Display preview (resized for GUI)
            display_size = (200, 200)
            preview = qr_image.copy()
            preview.thumbnail(display_size, Image.Resampling.LANCZOS)

            print("preview ready")
            
            # Convert to Tkinter format
            tk_image = ImageTk.PhotoImage(preview)
            self.preview_label.config(image=tk_image, text="")
            self.preview_label.image = tk_image  # Keep reference

            print("preview displayed")
            
            # Enable save button
            self.save_btn.config(state=tk.NORMAL)
            
            messagebox.showinfo("Success", "QR Code generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code:\n{str(e)}")
            
    def save_qr(self):
        if not self.generated_image:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="qr_code.png"
        )
        
        if file_path:
            try:
                self.generated_image.save(file_path, 'PNG')
                messagebox.showinfo("Success", f"Saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{str(e)}")

def main():
    root = tk.Tk()
    app = SimpleQRGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()