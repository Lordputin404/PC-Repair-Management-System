# PC Repair Management System

A desktop-based PC Repair Management System built with Python, CustomTkinter, and MySQL. The application provides a simple interface for managing customers, devices, repair records, repair status, technicians, and repair costs.

## Features

### Customer Management
- Add new customers
- Edit customer information
- Delete customers
- Search customers
- Customer input validation
- Phone number validation

### Device Management
- Add devices
- Edit device information
- Delete devices
- Search devices
- Link devices with customers
- Device input validation
- Serial number validation

### Repair Management
- Add repair records
- Edit repair records
- Delete repair records
- Search repair records
- Track repair status
- Assign technicians
- Track repair costs
- Record received date
- Automatically record delivery date when a repair is marked as Delivered

### Dashboard
- Customer count
- Device count
- Repair count
- Repair summary
- Recent repair information

### Reports & Export
- Export application data to CSV
- Generate basic reports from the application

### User Interface
- Modern CustomTkinter interface
- Light and Dark appearance modes
- Sidebar navigation
- Active navigation highlighting
- Form validation
- Search functionality

## Technologies Used

- Python 3.x
- CustomTkinter
- MySQL
- mysql-connector-python
- python-dotenv

## Project Structure

## Project Structure

```text
PC-Repair-Management-System/
│
├── database.sql
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
└── src/
    ├── main.py
    ├── database.py
    ├── export.py
    │
    └── ui/
        ├── __init__.py
        ├── customers.py
        ├── dashboard.py
        ├── devices.py
        ├── repairs.py
        └── reports.py
```

## Requirements

Before running the application, make sure the following are installed:

- Python 3.x
- MySQL Server
- MySQL Workbench
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Lordputin404/PC-Repair-Management-System.git
cd PC-Repair-Management-System
```

### 2. Install Dependencies

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

## Database Setup

Open the `database.sql` file in MySQL Workbench and execute it.

This will automatically create the required database and tables.

The database contains the following tables:

- `customers`
- `devices`
- `repairs`

### Database Relationships

```text
Customers
    │
    │ 1
    │
    │ N
Devices
    │
    │ 1
    │
    │ N
Repairs
```

A customer can have multiple devices, and a device can have multiple repair records.

## Database Configuration

Create a `.env` file in the project root:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=pc_repair_system
```

Replace `your_mysql_password` with your local MySQL password.

Do not commit the `.env` file to GitHub.

## Run the Application

After completing the database and environment configuration, run:

```bash
python src/main.py
```

The application will launch as a desktop GUI.

## Repair Workflow

The repair process follows these statuses:

```text
Pending
   ↓
In Progress
   ↓
Completed
   ↓
Delivered
```

When a repair is marked as **Delivered**, the delivery date is recorded automatically.

## Input Validation

The application includes validation for important input fields.

### Customer
- Name accepts letters and spaces
- Phone number must contain exactly 10 digits

### Device
- Brand accepts letters and spaces
- Model accepts alphanumeric characters and spaces
- Serial number accepts alphanumeric characters, `-`, and `_`
- Serial number is automatically converted to uppercase

### Repair
- Technician name accepts letters and spaces
- Repair cost accepts numeric values and decimal points
- Date received follows the `YYYY-MM-DD` format

## Database Schema

### Customers

Stores customer information such as:

- Customer ID
- Name
- Phone number

### Devices

Stores device information such as:

- Device ID
- Customer ID
- Brand
- Model
- Serial number
- Problem description

### Repairs

Stores repair information such as:

- Repair ID
- Device ID
- Repair status
- Technician
- Repair cost
- Date received
- Date delivered

## Appearance

The application supports:

- Light mode
- Dark mode
- System appearance mode

## Future Improvements

Possible future improvements include:

- User authentication
- Automated database backup
- Invoice generation
- PDF report generation
- Advanced repair analytics
- Improved reporting features

## Author

**Amar Suleman Kujur**

GitHub:
https://github.com/Lordputin404

## License

This project is developed for educational and academic purposes.