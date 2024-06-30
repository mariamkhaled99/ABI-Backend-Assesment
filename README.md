# ABI-Backend-Assessment

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)


## Project Overview

ABI-Backend-Assessment is a Django-based backend application designed to manage bookings and integrate with the Zoom API. It includes features for user management, booking creation, listing, updating, and deletion.

## Features

- **User Management**: Create, authenticate, and manage users.
- **Booking Management**: Create, list, update, and delete bookings.
- **Zoom Integration**: Integration with the Zoom API for meeting management.
- **Swagger Documentation**: API documentation using Swagger.

## Setup and Installation

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)
- virtualenv (optional but recommended)
- Docker (optional for containerized setup)

### Installation Steps

1. **local using venv and Django**
   ```bash
   git clone <repository-url>
   cd ABI-Backend-Assessment
   python -m venv venv 
   venv\Scripts\activate
   python manage.py makemigrations
   python manage.py migrate
   ```
2. **local using Docker**
```bash
  docker-compose build
  docker-compose up
   ```



### Testing
```bash
pytest booking/tests
```

