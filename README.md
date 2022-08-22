# Electronics store

This application is a student project which is a simple online store (without implemented payments).

## Description

This application is one of my first web app python projects, so it requires some code correction, including changing camelCase to snake_case and adding a few logistic fixes, moving CSS to separate files etc. Nevertheless, it is fully functional and resistant to attempts to spoil (e.g. buying more products than are available). Much of the security and procedures, including logging, are designed in the MySQL database. It includes a user view that can order products and an administrator view that can add, remove and edit products and manage orders. The assumption is that the administrator is the owner or employee of the store, and the payment for the products is made outside the software. To be honest, this application can only work with a properly created database, so the above source code cannot be run on its own, which means that the application works correctly only for me and for people who have the right database.

## Build With
* Python 3.9
* Flask
* mysql.connector
* HTML
* CSS

## Getting Started

Make sure you have python 3.9 or higher installed.

You can get it here:
https://www.python.org/downloads/

You also need a special configuration file with data including database, ip, user, password and access settings. An example file with fake data is in the source files and the correct config.txt file should be in the same place.

### Installing

1. Clone the repo
   ```sh
   git clone https://github.com/krasickiPawel/sklep_z_elektronika.git
   ```
2. Install requirements
   ```sh
   pip install -r reqirements.txt
   ```

### Executing program

In the src directory
   ```sh
   python main.py
   ```

## Usage

### 1. Run the database

### 2. Run the program using **python main.py** command in appropriate directory

### 3.1 Go to http://localhost:5000/ and register or login as a client and have fun searching and buying the available products.

### 3.2 Go to localhost:5000/emp/ and login as an employee and have fun editing products, finding the right ones, or adding new ones


## License

This project is licensed under the MIT License - see the LICENSE.md file for details
