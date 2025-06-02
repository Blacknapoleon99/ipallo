#!/usr/bin/env python3
"""
Simple GUI test to verify Tkinter is working
"""

import tkinter as tk
from tkinter import messagebox

def test_button_click():
    messagebox.showinfo("Test", "GUI is working! Click OK to continue.")

def main():
    print("Creating test GUI window...")
    
    root = tk.Tk()
    root.title("BlackzAllocator - GUI Test")
    root.geometry("400x300")
    root.configure(bg='#2b2b2b')
    
    # Make window appear on top
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    # Create content
    tk.Label(root, text="BlackzAllocator GUI Test", 
             font=('Arial', 16, 'bold'), 
             fg='white', bg='#2b2b2b').pack(pady=30)
    
    tk.Label(root, text="If you can see this window, Tkinter is working!", 
             font=('Arial', 12), 
             fg='white', bg='#2b2b2b').pack(pady=10)
    
    tk.Button(root, text="Test Button", 
              command=test_button_click,
              font=('Arial', 12),
              bg='#0078d4', fg='white',
              padx=20, pady=10).pack(pady=20)
    
    tk.Button(root, text="Close", 
              command=root.destroy,
              font=('Arial', 12),
              bg='#d13438', fg='white',
              padx=20, pady=10).pack(pady=10)
    
    print("GUI window created. It should be visible now.")
    print("Close the window to continue...")
    
    root.mainloop()
    print("GUI window closed.")

if __name__ == "__main__":
    main() 