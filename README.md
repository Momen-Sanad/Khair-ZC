# Khair-ZC

A charity-based project designed to support and empower the "Khair-ZC" club. It serves as a platform for donors and volunteers to connect and work towards various humanitarian causes. This project consists of a **frontend** (React, in the `client` folder) and a **backend** (Python Flask, in the `server` folder).

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributors](#contributors)
- [License](#license)

## Project Overview

"Khair-ZC" is a club platform designed to connect donors and volunteers with charity projects and causes that need support. The platform aims to make it easier for individuals to contribute to their communities by donating, volunteering, or sharing resources with those in need. The project is split into two main parts:
- **Frontend**: Built with React, responsible for the user interface and user experience.
- **Backend**: Developed in Python with Flask, handles data processing, user authentication, and API services.

## Features

- User registration and authentication
- Browse, donate to, and volunteer for charity projects
- View past campaigns & media
- Participate in new campaigns
- Collect coins to claim our exclusive merchandise
- Participate in charity organizations

## Project Structure

- **client**: Contains the React frontend. This is where the user interface is built, including pages for charity projects, user profile, and donation history.
- **server**: Contains the Flask backend. This is where APIs are developed to handle user authentication, project listings, donation processing, and more.

```
Khair-ZC/
│                              # Frontend (client):
├── client/                    # Frontend React application
│   ├── node_modules/          # Required packages
│   ├── public/                # Public assets folder
│   │   ├── favicon.ico        # Favicon icon for the website
│   │   └── index.html         # Main HTML file for React
│   ├── src/                   # Source files for React components and styles
│   │   ├── App.css            # Styles for the main App component
│   │   ├── App.tsx            # Main App component
│   │   ├── custom.d.ts        # Type declarations for Typescript
│   │   ├── index.tsx          # Main entry file for React
│   │   ├── assets/            # Source files for React components and styles
│   │   │   ├── fonts/
│   │   │   ├── images/
│   │   │   ├── sounds/
│   │   │   └── stylesheets/
│   │   └── components/
│   │       ├── Home.tsx
│   │       ├── Campaigns.tsx
│   │       ├── Navbar.tsx
│   │       ├── Media.tsx
│   │       └── Shop.tsx
│   ├── .gitignore             # Git ignore file for client
│   ├── package-lock.json      # Lock file for npm dependencies
│   ├── package.json           # Package configuration file
│   └── tsconfig.json          # TypeScript configuration file
│                              # Backend (server):
├── server/                    # Backend Flask application
│   ├── app.py                 # Main Flask application file
│   └── requirements.txt       # Python dependencies file
│
├── README.md                  # Project-wide README file
└── setup.sh                   # Setup script for project installation
```

## Getting Started

### Prerequisites
Ensure you have the following installed:
- **Node.js** (for the frontend)
- **Python 3** and **pip** (for the backend)
- **Git** for version control

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/0x3mr/Khair-ZC.git
   cd Khair-ZC
   ```

2. **Frontend Setup:**
   - Navigate to the `client` folder:
     ```bash
     cd client
     ```
   - Install dependencies:
     ```bash
     npm install
     ```

3. **Backend Setup:**
   - Navigate to the `server` folder:
     ```bash
     cd ../server
     ```
   - Create a virtual environment and activate it:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # For Windows: venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## Usage

1. **Running the Frontend (React):**
   - Start the development server:
     ```bash
     npm start
     ```
   - The frontend should now be available at `http://localhost:3000`.

2. **Running the Backend (Flask):**
   - Start the Flask server:
     ```bash
     flask run
     ```
   - The backend will be running at `http://localhost:5000`.

3. **Accessing the Application:**
   - Visit `http://localhost:3000` to view and interact with the frontend, which will communicate with the backend at `http://localhost:5000`.

## Screenshots

Here are some early prototypes of the application:

- **Landing Page**: ![Landing Page]()![Khair-ZC(1)](https://github.com/user-attachments/assets/f2af469b-268e-4c2e-bb10-7a9259fdefd2))
- **Campaigns View**: ![Campaigns View]()![Khair-ZC(3)](https://github.com/user-attachments/assets/bc1e3678-87d0-46f6-806f-1f0cc296c8f8)
- **Sign In Page**: ![Sign In Page]()![Khair-ZC(4)](https://github.com/user-attachments/assets/dc802c5b-f14b-4c7b-b30b-aeb484b7b4ac)
- **Sign Up Page**: ![Sign Up Page]()![Khair-ZC(5)](https://github.com/user-attachments/assets/7833d85d-033c-4720-874b-0fcf012036cf)

## Contributors

This project is made possible by our dedicated team:
- Amr Abdelfattah
- Khaled Mohamed
- Momen Mahmoud
- Abdullah Ayman
- Mohammed Abbas


## License

TBD.
