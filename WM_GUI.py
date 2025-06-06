import cv2
import pyautogui
import numpy as np
import time
import tkinter as tk
import threading
import sys
import traceback

# ================ YOUR ORIGINAL CODE + MODIFICATIONS =================

# Load the images using OpenCV
edit_image_path = 'edit.png'
not_edit_image_path = 'notedit.png'

edit_template = cv2.imread(edit_image_path, 0)
not_edit_template = cv2.imread(not_edit_image_path, 0)

# Global coordinates (replace with your actual ones)
initial_product_coords = (1725, 579)  # Replace with actual coordinates
percent_sale_coords = (382, 844)      # Replace with actual coordinates
save_button_coords = (1741, 976)      # Replace with actual coordinates
apply_sale_coords = (1182, 683)       # Replace with actual coordinates

last_product_coords = [
    (1725, 530),  # First product
    (1725, 614),  # Second product
    (1725, 702),  # Third product
    (1725, 783)   # Fourth product
]

num_products = 21
delay = 2

next_page_coords = (1825, 863)  # Verify the coordinates are correct

# -------------- Functions for screenshot and template matching ----------------

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    return screenshot

def match_template(template, threshold=0.97):
    screenshot = take_screenshot()
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f"Matching score: {max_val}")
    print(f"Top-left corner of match: {max_loc}")  # Debugging info
    
    if max_val >= threshold:
        template_height, template_width = template.shape[:2]
        center_x = max_loc[0] + (template_width // 2)
        center_y = max_loc[1] + (template_height // 2)
        print(f"Center of match: ({center_x}, {center_y})")  # Debugging info
        return (center_x, center_y)
    
    return None

def is_circular_edit_symbol():
    location = match_template(not_edit_template, threshold=0.100)
    if location:
        print("Circular edit symbol detected, avoiding click.")
        return True
    else:
        print("Circular edit symbol not detected.")
        return False

def check_and_click_edit_symbol():
    try:
        # First, check if the circular edit symbol is visible (avoid clicking if found)
        if is_circular_edit_symbol():
            print("Skipping click on the edit symbol because it has a circle.")
            return

        # Otherwise, check for the normal edit symbol
        location = match_template(edit_template, threshold=0.90)
        if location:
            print(f"Edit symbol found at center: {location}, clicking on it.")
            pyautogui.moveTo(location[0], location[1], duration=0.5)
            pyautogui.click()
            time.sleep(2)  # time for UI to process
        else:
            print("Edit symbol not found.")
    except Exception as e:
        print(f"Error while checking or clicking the edit symbol: {e}")

def update_product_price(product_coords, scroll_increment=0):
    try:
        print(f"Clicking on product at {product_coords}")
        time.sleep(2)
        pyautogui.click(product_coords)
        time.sleep(3)

        # Click "edit" if possible
        check_and_click_edit_symbol()

        # Scroll down to find the Percent Sale field
        pyautogui.scroll(-2500)
        time.sleep(2)
        
        # Click on the Percent Sale field
        pyautogui.click(percent_sale_coords)
        time.sleep(1)
        
        # Type the discount percentage
        pyautogui.typewrite('30')
        time.sleep(1)
        
        # Click the Apply Sale button
        pyautogui.click(apply_sale_coords)
        time.sleep(1)
        
        # Click the save button
        pyautogui.click(save_button_coords)
        time.sleep(3)
        
        if scroll_increment != 0:
            # Scroll to the next product
            pyautogui.scroll(scroll_increment)
            time.sleep(2)
    
    except Exception as e:
        print(f"Error encountered: {e}")

# ------------------------ MAIN LOGIC IN A FUNCTION ----------------------------

def run_program():
    """
    Encapsulates the main logic of your script in a function so we can run it
    in a separate thread and still keep the Tkinter GUI responsive.
    """
    # Record the start time for crash-logging
    start_time = time.time()

    try:
        # Outer loop (30 iterations in your example)
        for loop_index in range(25):
            print(loop_index)
            
            current_product_coords = list(initial_product_coords)

            # Loop through the first 21 products
            for i in range(num_products):
                scroll_increment = -87 * (i + 1)
                update_product_price(tuple(current_product_coords), scroll_increment)
                time.sleep(2)

            # Handle the last 4 products
            for coords in last_product_coords:
                pyautogui.scroll(-2500)
                time.sleep(3)
                update_product_price(coords)
                time.sleep(3)

            # Scroll to bottom, click next page
            pyautogui.scroll(-2500)
            time.sleep(3)
            pyautogui.click(next_page_coords)
            time.sleep(2)

        # If the program completes normally, log the finish time
        end_time = time.time()
        elapsed = end_time - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)

        with open("logfile.txt", "a") as f:
            f.write(f"Program finished successfully. "
                    f"Total run time: {hours:02d}:{minutes:02d}:{seconds:02d}\n")

    except Exception as e:
        end_time = time.time()
        elapsed = end_time - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)

        # Log crash info
        with open("logfile.txt", "a") as f:
            f.write("Program crashed!\n")
            f.write(f"Run time before crash: {hours:02d}:{minutes:02d}:{seconds:02d}\n")
            f.write(f"Error: {e}\n")
            f.write(f"Traceback:\n{traceback.format_exc()}\n")

        # Re-raise so you can see it in the console
        raise

# ========================== TKINTER GUI SECTION ===============================

class AlwaysOnTopStopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        # Keep the window on top
        self.root.attributes("-topmost", True)
        # Optionally remove the maximize button if you like:
        # self.root.resizable(False, False)

        # Variables to track time
        self.start_time = time.time()
        self.running = True

        # GUI elements
        self.time_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 16))
        self.time_label.pack(padx=10, pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_program)
        self.stop_button.pack(padx=10, pady=10)

        # Start updating the time display
        self.update_timer()

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            # Schedule next update in 1 second
            self.root.after(1000, self.update_timer)

    def stop_program(self):
        """Stop the entire program and log the final time."""
        self.running = False
        end_time = time.time()
        elapsed = end_time - self.start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)

        # Log the stop time
        with open("logfile.txt", "a") as f:
            f.write(f"Program manually stopped. Total run time: "
                    f"{hours:02d}:{minutes:02d}:{seconds:02d}\n")

        # Exit the program gracefully
        self.root.destroy()
        sys.exit(0)

def start_main_thread():
    """
    Starts the main run_program function in a separate thread
    so the GUI remains responsive.
    """
    thread = threading.Thread(target=run_program, daemon=True)
    thread.start()

# =========================== LAUNCH EVERYTHING ================================

def main():
    # Create the Tkinter root
    root = tk.Tk()

    # Create the stopwatch UI
    app = AlwaysOnTopStopwatch(root)

    # Start the main program logic in a separate thread
    start_main_thread()

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
