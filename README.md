# Pharmacy Management System

## Overview
This is a Pharmacy Management System built using Django. It provides a comprehensive solution for managing pharmacy inventory, sales, and customer records efficiently. The system allows pharmacists to keep track of stock, process sales, and generate invoices seamlessly.

## Features
- **User Authentication**: Secure login and user roles for admins and staff.
- **Medicine Inventory Management**: Add, update, and track medicine stock.
- **Sales & Billing**: Process customer purchases and generate invoices.
- **Order Management**: Manage supplier orders and restock inventory.
- **Customer Management**: Maintain customer records for returning customers.
- **Reports & Analytics**: Generate reports on sales and stock levels.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/al-ghalib/pharmacy-mgt-system.git
   cd pharmacy-mgt-system
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```sh
   python manage.py migrate
   ```

5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

7. Access the system at `http://127.0.0.1:8000/`

## Dependencies
This project requires the following:
- Python
- Django
- Django Rest Framework (if applicable)
- SQLite (default) or PostgreSQL (recommended for production)

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author
[al-ghalib](https://github.com/al-ghalib)

## Acknowledgments
- Built with Django for efficient pharmacy management.
- Inspired by real-world pharmacy operations.

