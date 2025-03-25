import cv2
import pyautogui
import numpy as np
import time

# Load the images using OpenCV
edit_image_path = 'edit.png'
not_edit_image_path = 'notedit.png'

edit_template = cv2.imread(edit_image_path, 0)
not_edit_template = cv2.imread(not_edit_image_path, 0)

# Function to take a screenshot using OpenCV
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    return screenshot

# Function to match template with screenshot and check if it's found
def match_template(template, threshold=0.97):
    # Take a screenshot of the current screen
    screenshot = take_screenshot()
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Print matching score for debugging
    print(f"Matching score: {max_val}")
    print(f"Top-left corner of match: {max_loc}")  # Debugging info
    
    # If the match is above the threshold, calculate the center of the match
    if max_val >= threshold:
        # Get the width and height of the template
        template_height, template_width = template.shape[:2]
        
        # Calculate the center of the matched region
        center_x = max_loc[0] + (template_width // 2)
        center_y = max_loc[1] + (template_height // 2)
        
        print(f"Center of match: ({center_x}, {center_y})")  # Debugging info
        
        # Return the center coordinates
        return (center_x, center_y)
    
    # Return None if no match was found
    return None

# Function to check if the circular "edit" symbol is found (not allowed to click)
def is_circular_edit_symbol():
    location = match_template(not_edit_template, threshold=0.97)
    if location:
        print("Circular edit symbol detected, avoiding click.")
        return True
    else:
        print("Circular edit symbol not detected.")
        return False

# Function to check if the "edit" symbol without the circle is found and click it once
def check_and_click_edit_symbol():
    try:
        # First, check if the circular edit symbol is visible (and we should avoid clicking)
        if is_circular_edit_symbol():
            print("Skipping click on the edit symbol because it has a circle.")
            return  # Skip the click if the circular symbol is detected

        # Otherwise, check for the normal edit symbol
        location = match_template(edit_template, threshold=0.90)
        if location:
            print(f"Edit symbol found at center: {location}, clicking on it.")
            pyautogui.moveTo(location[0], location[1], duration=0.5)  # Move to center
            pyautogui.click()  # Click in the center
            time.sleep(2)  # Allow time for the UI to process the click
        else:
            print("Edit symbol not found.")
    except Exception as e:
        print(f"Error while checking or clicking the edit symbol: {e}")

# Function to update the price of each product
def update_product_price(product_coords, scroll_increment=0):
    try:
        # Click on the product using coordinates
        print(f"Clicking on product at {product_coords}")
        time.sleep(2)
        pyautogui.click(product_coords)
        time.sleep(3)

        # After clicking the product, check if the circular edit symbol is found and avoid clicking if so
        check_and_click_edit_symbol()

        # Scroll down to find the Percent Sale field
        pyautogui.scroll(-2500)  # Adjust as needed
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

# Coordinates for the initial product
initial_product_coords = (1725, 579)  # Replace with actual coordinates
percent_sale_coords = (382, 844)  # Replace with actual coordinates
save_button_coords = (1741, 976)  # Replace with actual coordinates
apply_sale_coords = (1182, 683)  # Replace with actual coordinates

# Coordinates for the last 4 products
last_product_coords = [
    (1725, 530),  # First product
    (1725, 614),  # Second product
    (1725, 702),  # Third product
    (1725, 783)   # Fourth product
]

# Number of products to update
num_products = 21
delay = 2

for i in range(0, 30):
    print(i)
    
    # Start with the initial product coordinates
    current_product_coords = list(initial_product_coords)

    # Loop through the first 21 products
    for i in range(0, num_products):
        scroll_increment = -87 * (i + 1)  # Calculate the scroll increment
        update_product_price(tuple(current_product_coords), scroll_increment)
        time.sleep(2)

    # Now handle the last 4 products
    for coords in last_product_coords:
        pyautogui.scroll(-2500)
        time.sleep(3)
        update_product_price(coords)
        time.sleep(3)

    # Scroll to the bottom of the page and click on the next page button
    pyautogui.scroll(-2500)  # Adjust to reach the bottom of the page
    time.sleep(3)
    next_page_coords = (1825, 863)  # Verify the coordinates are correct
    pyautogui.click(next_page_coords)
    time.sleep(2)
