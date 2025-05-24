# Orderoo

Digital Ordering System

## Features

### Admin Page

-   Food Item Management
    -   Add, edit, or remove food items.
    -   Set prices
    -   Upload images for food items.
-   Category Customization
    -   Create and manage categories
    -   Assign food items to categories.
-   Order Management
    -   View orders history
-   Customer Data Statistics
    -   Graphs (most picked items)

### Customer Page

-   Menu Browsing
    -   Display food items in a user-friendly UI.
    -   Organized by category.
-   Ordering System
    -   Customers can select multiple items and adjust quantities.
    -   Review order before confirming.
-   Receipt Printing
    -   After order submission, print a receipt.
    -   Printing is done with a specific printer (MXW01 cat printer)

---

## Cat Printer MXW01

A sub-project for printing receipts using the MXW01 Bluetooth Cat Printer.

A dirty and minimalistic derivation of [eerimoq's](https://github.com/eerimoq/moblin/tree/main/Moblin/Integrations/CatPrinter) and [werwolv's](https://github.com/WerWolv/PythonCatPrinter) cat printer implementation, focused only on doing the bare minimum print sequence needed for the cat printer to print.

_is tested to work on windows, linux (ubuntu), and macOS_

special thanks to [sophie's](https://sophi.ee/posts/2022-04-23-hacking-cat-printers-for-fun-and-likes-on-twitter/?fbclid=IwY2xjawJQ5R9leHRuA2FlbQIxMAABHfhxUYfZKv-ij9jEC1qI1MfM4nQPohKQBBR6IGtas_JfDtRYmzqaBGoslA_aem_q-8Pm0_XAxPbgYxSOSv3-w) and [werwolv's](https://werwolv.net/blog/cat_printer) cat printer blogs, and [eerimoq's](https://github.com/eerimoq/moblin/tree/main/Moblin/Integrations/CatPrinter) working implementation for MXW01 model.

---

## setting up:

download or clone this repo, then

1. create environment : `python -m venv env`

2. activate environment

    - Linux/macOS : `source env/bin/activate`
    - Windows : `env\Scripts\activate.bat`

3. install pyqt6 : `pip install pyqt6`

4. install dependencies : `pip install -r requirements.txt`
