from robocorp.tasks import task
from robocorp import browser, http, excel
from RPA.Tables import Tables


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=100,
    )

    open_robot_order_website()
    # download_oreders_excel_file()
    orders = get_orders()
    for row in orders:
        print(row)
        fill_the_form(row)
    
def open_robot_order_website():
    """Opens RobotSpareBin Industries Inc website for Robot orders"""
    page = browser.goto("https://robotsparebinindustries.com/#/robot-order")
        
def get_orders():
    """Download the orders CSV file, read it as a table, and return the result"""
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    # Create new empty table and read order rows from downloaded csv
    orders = Tables()
    order_rows = orders.read_table_from_csv(path="orders.csv")
    return order_rows

def fill_the_form(row):
    close_annoying_modal()
    page = browser.page()

    # 1. Head: Selected from dropdown using dropdown name (head) and input value for selection: 1,2,3,4,5,6
    page.select_option("//select[@name='head']", str(row["Head"]))
    # 2. Body: Selected from checkbox using id field with text id-body-# where # is dynamic part from input
    page.check("#id-body-" + str(row["Body"]))
    # 3. Legs: Selected from number field using placeholder text as locator and input data as value
    page.fill("//input[@placeholder='Enter the part number for the legs']", str(row["Legs"]))
    # 4, Address: Fill is done by field type and name and value is from input data
    page.fill("//input[@name='address']", str(row["Address"]))
    # 5. Click Preview button
    page.click("button:text('Preview')")

    """
    browser.close()
    """    


def close_annoying_modal():
    page = browser.page()
    page.click("button:text('Yep')")