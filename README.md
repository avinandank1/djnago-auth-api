
# Django Authentication API

This project provides a Django-based user authentication API with a range of features for seamless user management. Below are some key features:




## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Project Structure](#project-structure)
- [Features](#features)
- [Usage](#usage)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- Django
- Other dependencies (specified in requirements.txt)

## Installation

Follow the steps below to set up and run the project:

Clone the Repository
```bash
git clone https://github.com/kavinandan18/djnago-auth-api.git
```
Navigate to the Project Directory
```bash 
cd djnago-auth-api
```
Create a Virtual Environment
```bash
python -m venv venv
```
#### Activate the Virtual Environment
On Linux/macOS:
```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```
Install Dependencies
```bash
pip install -r requirements.txt
```

### Project Structure

```bash
django-auth-api/
|-- auth_api/
|   |-- migrations/
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- serializers.py
|   |-- tests.py
|   |-- urls.py
|   |-- utils.py
|   |-- views.py
|   |-- signals.py
|-- user-auth/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
    |-- asgi.py
|-- manage.py
|-- README.md
|-- requirements.txt
```
## Features

- **User Registration**
  - Users can register by providing a unique email address and a secure password.
  - Account activation emails are sent with activation links to verify user registration.

- **User Login**
  - Secure user login with email and password.
  - Accounts require activation before users can log in.

- **CSRF Token Retrieval**
  - Users can obtain a CSRF token for secure interaction with the API.

- **Check User Authentication**
  - Allows checking whether a user is currently authenticated.

- **Profile Management**
  - Users can create, retrieve, update, and delete their profiles.
  - Profile includes information such as mobile number, location, date of birth, bio, gender, and avatar.

- **Password Reset**
  - Users can request a password reset email.
  - Confirmation of password reset with a new password.

- **User Details**
  - Retrieve and update user details.
  - Users can view and modify their information.

- **Change Password**
  - Users can change their account password for enhanced security.

- **Delete Account**
  - Users have the option to delete their accounts permanently.

- **User Logout**
  - Allows users to log out securely.

- **Activation Confirmation**
  - Confirm user account activation with a provided activation link.

- **Token-Based Authentication**
  - Uses token-based authentication for secure user interactions.

- **Signal Handling**
  - Custom signals for user and profile creation.



## Usage

For detailed instructions on setting up and using the Django Authentication API, please refer to the Installation and Usage sections in the project's README file.

Feel free to explore and utilize the provided features for a robust user authentication experience in your Django project!


## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

We would like to express our gratitude to the following individuals and projects that contributed to the development of this authentication API:

- [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines.
- [Django Rest Framework](https://www.django-rest-framework.org/) - A powerful and flexible toolkit for building Web APIs.
- [Python Packages](https://pypi.org/) - Thank you to all the open-source packages that make Python development awesome.

Feel free to contribute, report issues, or suggest improvements to make this project even better!