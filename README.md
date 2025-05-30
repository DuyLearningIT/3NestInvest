3NestInvest
Project Overview
3NestInvest is a high-performance back-end application developed with FastAPI, tailored for a B2B (Business-to-Business) platform focused on investment product management. The system supports three distinct user roles—Admin, Sales, and Channels—with role-based access control (RBAC) to ensure secure and efficient operations. The application utilizes MySQL for data persistence, Alembic for database versioning, and incorporates advanced security features including JWT authentication, password hashing, and comprehensive CRUD operations. Designed for scalability and maintainability, 3NestInvest enables seamless collaboration between businesses for product rental and sales.
Project Structure

app/: Central directory containing the application’s core logic.
__pycache__: Stores Python bytecode cache files.
alembic/: Houses Alembic migration scripts for MySQL schema management.
api/: Defines API endpoints, controllers, and role-specific routing logic.
core/: Contains business logic, application configuration, and shared utilities.
crud/: Implements Create, Read, Update, and Delete operations for data persistence.
db/: Manages MySQL database connections, ORM models, and configurations.
env/: Stores environment-specific configuration files.
models/: Defines data models mapped to MySQL tables using an ORM.
schemas/: Contains Pydantic schemas for data validation and serialization.
utils/: Provides utility functions, including JWT handling and password hashing.


.env: Configuration file for environment variables (e.g., database credentials, JWT secret).
alembic.ini: Configuration file for Alembic database migrations.
main.py: Entry point for launching the FastAPI application.

User Roles and Permissions

Admin: Full administrative privileges, including the ability to add products, manage users, and oversee all platform operations.
Sales: Focused on customer engagement, with permissions to manage orders and customer interactions, but restricted from administrative tasks.
Channels: Represents partner businesses collaborating for product rental and sales, with access limited to their specific operational scope.

Key Features

CRUD Operations: Fully implemented Create, Read, Update, and Delete functionality for managing products, users, and orders.
JWT Authentication: Secure, token-based authentication to validate user sessions.
Password Hashing: Employs industry-standard hashing algorithms for secure password storage.
Role-Based Authorization: Enforces strict access control, ensuring only authorized users (e.g., Admins) can perform privileged actions.
B2B Collaboration: Facilitates partnerships with Channels for rental and sales operations, optimizing business workflows.

Prerequisites

Python 3.9 or higher
MySQL 8.0 or higher
pip for dependency management
Git for version control

Installation

Clone the Repository:git clone https://github.com/DuyLearningT3/3NestInvest.git


Navigate to the Project Directory:cd 3NestInvest


Set Up a Virtual Environment (recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:pip install -r requirements.txt


Configure Environment Variables:Copy the example environment file and update with your settings:cp .env.example .env

Edit .env to include MySQL connection details, JWT secret, and other necessary configurations.
Initialize the Database:Ensure MySQL is running, then apply migrations:alembic upgrade head



Usage

Launch the Application:Start the FastAPI server:python main.py

The API will be accessible at http://localhost:8000 by default.
Interact with the API:
Explore endpoints via the Swagger UI at http://localhost:8000/docs.
Authenticate using the /login endpoint to obtain a JWT token, required for protected routes.


Manage Database Migrations:Generate and apply migrations after schema changes:alembic revision -m "description of changes"
alembic upgrade head



Contributing
Contributions are highly encouraged to enhance 3NestInvest’s functionality. To contribute:

Fork the repository and create a feature branch (git checkout -b b back-end).
Adhere to PEP 8 style guidelines and include unit tests for new functionality.
Commit changes with clear messages (git commit -m "Add feature description").
Submit a pull request with a detailed description of your changes.
Await review and feedback from maintainers.

License
This project is licensed under the MIT License. Refer to the LICENSE file for complete terms and conditions.
Support and Contact
For inquiries, bug reports, or feature requests, please file an issue on the GitHub repository. For direct communication, reach out to the maintainers via the issue tracker.
Acknowledgments

Sincere appreciation to the FastAPI, Alembic, and MySQL communities for their exceptional tools and resources.
Gratitude to contributors who have invested time and expertise in advancing this project.

Development Guidelines

Ensure MySQL is properly configured and running before starting the application.
Regularly back up the database, especially in production environments, before applying migrations.
Test authentication, authorization, and role-based access thoroughly in a staging environment.
Monitor API performance and optimize endpoints as needed for high-traffic scenarios.

Version History

Initial Release: May 15, 2025
Last Updated: May 30, 2025

