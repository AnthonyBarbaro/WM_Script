import pyautogui
import time

# Path to the edit images
edit_image_path = 'edit.png'  # Image of the edit symbol without circle
not_edit_image_path = 'notedit.png'  # Image of the edit symbol with the circle around it

# Function to check if the circular "edit" symbol is found (not allowed to click)
def is_circular_edit_symbol():
    try:
        # Check if the circular edit symbol is visible on the screen
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

# Function to check if the "edit" symbol without the circle is found and click it if allowed
def check_and_click_edit_symbol():
    try:
        # First, check if the circular edit symbol is visible (and we should avoid clicking)
        if is_circular_edit_symbol():
            print("Skipping click on the edit symbol because it has a circle.")
            return  # Skip the click if the circular symbol is detected

        # Otherwise, proceed to check for and click the normal edit symbol
        edit_location = pyautogui.locateCenterOnScreen(edit_image_path, confidence=0.8)
        if edit_location:
            print(f"Edit symbol found at {edit_location}, clicking on it.")
            pyautogui.moveTo(edit_location, duration=0.5)
            pyautogui.click()
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
         # Click on the edit Sale field
        pyautogui.click(edit_sale_coords)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')  # Select all text
        pyautogui.press('backspace')   # Delete the selected text
        
        # Type the discount percentage
        pyautogui.typewrite('50')
        
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
edit_sale_coords = (1202, 663)
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

for i in range(0, 22):
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
