import tkinter as tk
from tkinter import colorchooser
import objc
from Cocoa import NSApplication, NSApp, NSWindow, NSColor, NSView, NSGraphicsContext, NSNull

class FullscreenOverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Overlay App")

        
        self.root.geometry("800x600")
        

        control_frame = tk.Frame(root, bg='black')
        control_frame.pack(side=tk.TOP, fill=tk.X)

       
        self.choose_color_btn = tk.Button(control_frame, text="Choose Color", command=self.choose_color)
        self.choose_color_btn.pack(side=tk.LEFT, padx=5, pady=5)

  
        self.transparency_slider = tk.Scale(control_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, 
                                            label="Transparency", command=self.adjust_transparency)
        self.transparency_slider.set(0.5) 
        self.transparency_slider.pack(side=tk.LEFT, padx=5, pady=5)


        colors = ["blue", "green", "orange", "pink", "purple", "red", "yellow"]
        for color in colors:
            btn = tk.Button(control_frame, text=color.capitalize(), bg=color, command=lambda c=color: self.set_color(c))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

      
        self.root.config(bg='systemTransparent')

        
        self.setup_mac_transparency()

       
        self.root.bind("<Escape>", self.exit_fullscreen)

    def choose_color(self):

        self.root.attributes("-topmost", False)

        color_code = colorchooser.askcolor(title="Choose color")[1]
        
        if color_code:

            self.root.configure(background=color_code)

        if self.is_fullscreen:
            self.root.attributes("-topmost", True)

    def set_color(self, color):
      
        self.root.configure(background=color)

    def adjust_transparency(self, value):

        self.root.attributes("-alpha", float(value))

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        self.is_fullscreen = False
        self.root.destroy()

    def setup_mac_transparency(self):

        window_id = self.root.winfo_id()
        ns_app = NSApplication.sharedApplication()
        ns_window = None

        for window in ns_app.windows():
            if window.windowNumber() == window_id:
                ns_window = window
                break

        if ns_window:
            # Set the window to be transparent
            ns_view = ns_window.contentView()
            ns_view.setWantsLayer_(True)
            ns_view.layer().setOpaque_(False)
            ns_view.layer().setBackgroundColor_(NSColor.clearColor().CGColor())

         
            ns_view.setAlphaValue_(0.0)
            ns_view.setAllowsMouseInteraction_(False)

root = tk.Tk()

# create app
app = FullscreenOverlayApp(root)


root.mainloop()
