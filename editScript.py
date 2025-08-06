import pyautogui
import time
import tkinter as tk
import threading
import sys
import traceback

# ========== Configure these paths and coordinates as needed ==========

edit_image_path = 'edit.png'       # Image of the edit symbol without circle
not_edit_image_path = 'notedit.png'  # Image of the edit symbol with the circle around it

# Coordinates and other settings
initial_product_coords = (1725, 579)  # Replace with actual coordinates
last_product_coords = [
    (1725, 530),  # First product
    (1725, 614),  # Second product
    (1725, 702),  # Third product
    (1725, 783)   # Fourth product
]

edit_sale_coords = (1202, 663)     # The field to input sale percentage
apply_sale_coords = (1182, 683)    # "Apply Sale" button
save_button_coords = (1741, 976)   # "Save" button
next_page_coords = (1825, 863)     # "Next page" button

num_products = 21
loop_count = 10  # How many times you want to iterate through pages
scroll_distance_per_product = -87   # Adjust if needed
delay = 2

# ========== Image-based detection functions ==========

def is_circular_edit_symbol():
    """
    Detect if the 'notedit.png' (circular edit symbol) is visible,
    meaning we should NOT click.
    """
    try:
        circular_edit_location = pyautogui.locateCenterOnScreen(not_edit_image_path, confidence=0.100)
        if circular_edit_location:
            print("Circular edit symbol detected, avoiding click.")
            return True
        else:
            print("Circular edit symbol not detected.")
            return False
    except Exception as e:
        print(f"Error while detecting circular edit symbol: {e}")
        return False


def check_and_click_edit_symbol():
    """
    Checks if the circular edit symbol is visible. If it is,
    do not click. Otherwise, locate and click the normal edit symbol.
    """
    try:
        # First check for the circular edit symbol
        if is_circular_edit_symbol():
            print("Skipping click on the edit symbol because it has a circle.")
            return  # Do not click if the circular symbol is found

        # Otherwise, proceed to click the normal edit symbol
        edit_location = pyautogui.locateCenterOnScreen(edit_image_path, confidence=0.8)
        if edit_location:
            print(f"Edit symbol found at {edit_location}, clicking on it.")
            pyautogui.moveTo(edit_location, duration=0.5)
            pyautogui.click()
            time.sleep(2)  # Allow time for UI to process
        else:
            print("Edit symbol not found.")
    except Exception as e:
        print(f"Error while checking or clicking the edit symbol: {e}")

# ========== Core logic to update a single product price ==========

def update_product_price(product_coords, scroll_increment=0):
    """
    Clicks on a product, attempts to click the edit symbol (if allowed),
    inputs a 50% sale, applies, and saves. Optionally scrolls after saving.
    """
    try:
        # Click on the product using coordinates
        print(f"Clicking on product at {product_coords}")
        time.sleep(3)
        pyautogui.click(product_coords)
        time.sleep(4)

        # Check and click the edit symbol if allowed
        check_and_click_edit_symbol()
        time.sleep(1)
        # Scroll down to find the sale field
        pyautogui.scroll(-2500)
        time.sleep(2)

        # Click on the edit sale field
        pyautogui.click(edit_sale_coords)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')  # Select all text
        pyautogui.press('backspace')   # Delete the selected text
        time.sleep(.5)
        # Type the discount percentage (e.g., '50')
        pyautogui.typewrite('30')
        time.sleep(1.5)

        # Click the Apply Sale button
        pyautogui.click(apply_sale_coords)
        time.sleep(1.5)

        # Click the save button
        pyautogui.click(save_button_coords)
        time.sleep(6)

        # Optionally scroll to the next product
        if scroll_increment != 0:
            pyautogui.scroll(scroll_increment)
            time.sleep(3)

    except Exception as e:
        print(f"Error encountered while updating product price: {e}")

# ========== Main program logic in a function ==========

def run_program():
    """
    This function runs the entire update process in a loop. 
    We wrap it in try/except to log crashes to 'logfile.txt'.
    """
    start_time = time.time()  # For logging

    try:
        for page_index in range(loop_count):
            print(f"Processing page loop {page_index + 1}/{loop_count} ...")

            # Start with the initial product
            current_product_coords = initial_product_coords

            # Loop through the first 'num_products' (21) items
            for i in range(num_products):
                scroll_increment = scroll_distance_per_product * (i + 1)
                update_product_price(current_product_coords, scroll_increment)
                time.sleep(0.2)

            # Now handle the last 4 products
            for coords in last_product_coords:
                pyautogui.scroll(-2500)
                time.sleep(3)
                update_product_price(coords)
                time.sleep(3)

            # Scroll to bottom of page, then click on the next page
            pyautogui.scroll(-2500)
            time.sleep(3)
            pyautogui.click(next_page_coords)
            time.sleep(2)

        # If completed normally, log the finish time
        end_time = time.time()
        elapsed = end_time - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)

        with open("logfile.txt", "a") as f:
            f.write(f"Program finished successfully. "
                    f"Total run time: {hours:02d}:{minutes:02d}:{seconds:02d}\n")

    except Exception as e:
        # On crash, log info
        end_time = time.time()
        elapsed = end_time - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)

        with open("logfile.txt", "a") as f:
            f.write("Program crashed!\n")
            f.write(f"Run time before crash: {hours:02d}:{minutes:02d}:{seconds:02d}\n")
            f.write(f"Error: {e}\n")
            f.write(f"Traceback:\n{traceback.format_exc()}\n")

        raise  # re-raise to see error in console too


# ========== Tkinter GUI (Stopwatch + Stop Button) ==========

class AlwaysOnTopStopwatch:
    """
    A simple Tkinter window that is always on top, 
    displays elapsed time, and includes a 'Stop' button.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        # Keep the window on top
        self.root.attributes("-topmost", True)

        self.start_time = time.time()
        self.running = True

        # Create a label to display the time
        self.time_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 16))
        self.time_label.pack(padx=10, pady=10)

        # Create a Stop button to terminate the script
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_program)
        self.stop_button.pack(padx=10, pady=10)

        # Begin updating the timer display
        self.update_timer()

    def update_timer(self):
        """Updates the stopwatch display every 1 second."""
        if self.running:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            # Schedule the next update in 1 second
            self.root.after(1000, self.update_timer)

    def stop_program(self):
        """
        Stop the entire program and log to logfile (optional),
        then gracefully exit.
        """
        self.running = False
        end_time = time.time()
        elapsed = end_time - self.start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)

        # Optional: Log the stop time
        with open("logfile.txt", "a") as f:
            f.write(f"Program manually stopped. Total run time: "
                    f"{hours:02d}:{minutes:02d}:{seconds:02d}\n")

        # Close the Tk window and exit
        self.root.destroy()
        sys.exit(0)


# ========== Threaded startup so the UI doesn't freeze ==========

def start_main_thread():
    """
    Starts the main run_program function in a separate thread
    so the Tkinter GUI remains responsive.
    """
    thread = threading.Thread(target=run_program, daemon=True)
    thread.start()


# ========== The main entry point ==========

def main():
    root = tk.Tk()
    app = AlwaysOnTopStopwatch(root)

    # Start the run_program() logic in a separate thread
    start_main_thread()

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
