import pyautogui
import time

# Paths to the edit images
edit_image_path = 'edit.png'         # Image of the edit symbol without circle
not_edit_image_path = 'notedit.png'  # Image of the edit symbol with the circle around it

# Function to check if the circular "edit" symbol is found (not allowed to click)
def is_circular_edit_symbol():
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

# Function to check if the "edit" symbol without the circle is found and click it if allowed
def check_and_click_edit_symbol():
    try:
        if is_circular_edit_symbol():
            print("Skipping click on the edit symbol because it has a circle.")
            return

        edit_location = pyautogui.locateCenterOnScreen(edit_image_path, confidence=0.8)
        if edit_location:
            print(f"Edit symbol found at {edit_location}, clicking on it.")
            pyautogui.moveTo(edit_location, duration=0.5)
            pyautogui.click()
            time.sleep(2)
        else:
            print("Edit symbol not found.")
    except Exception as e:
        print(f"Error while checking or clicking the edit symbol: {e}")

# Function to update the price of each product
def update_product_price(product_coords, scroll_increment=0):
    try:
        print(f"Clicking on product at {product_coords}")
        time.sleep(2)
        pyautogui.click(product_coords)
        time.sleep(3)

        check_and_click_edit_symbol()

        pyautogui.scroll(-2500)
        time.sleep(2)

        pyautogui.click(edit_sale_coords)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')

        pyautogui.typewrite('50')

        pyautogui.click(apply_sale_coords)
        time.sleep(1)

        pyautogui.click(save_button_coords)
        time.sleep(3)

        if scroll_increment != 0:
            pyautogui.scroll(scroll_increment)
            time.sleep(2)

    except Exception as e:
        print(f"Error encountered: {e}")

# Coordinates and configuration
initial_product_coords = (1725, 579)
edit_sale_coords = (1202, 663)
apply_sale_coords = (1182, 683)
save_button_coords = (1741, 976)
next_page_coords = (1825, 863)

last_product_coords = [
    (1725, 530),
    (1725, 614),
    (1725, 702),
    (1725, 783)
]

num_products = 21
delay = 2

# Main loop for 22 pages
for page_index in range(22):
    print(f"Page {page_index + 1}")

    current_product_coords = list(initial_product_coords)

    for i in range(num_products):
        scroll_increment = -87 * (i + 1)
        update_product_price(tuple(current_product_coords), scroll_increment)
        time.sleep(delay)

    for coords in last_product_coords:
        pyautogui.scroll(-2500)
        time.sleep(3)
        update_product_price(coords)
        time.sleep(3)

    pyautogui.scroll(-2500)
    time.sleep(3)
    pyautogui.click(next_page_coords)
    time.sleep(2)
