# Posture Corrector App/ Gym Management System

## Overview
The **Posture Corrector App/ Gym Management System** is a web-based application designed to help users correct their posture through visual feedback and AI-based recommendations. This app uses **MediaPipe** and **OpenCV** for posture detection, along with **Linear Regression** for analyzing body alignment. The frontend is built using HTML, CSS, JavaScript, and Bootstrap for a responsive design, while Django powers the backend. It supports both **SQLite** and **MySQL** databases.



## Features
- User authentication (login, signup, password reset)
- Video posture analysis with **MediaPipe** and **OpenCV**
- Real-time visual feedback with performance metrics
- Linear Regression model for accurate posture analysis
- Responsive UI with Bootstrap
- Performance tracking (correct and incorrect posture counts)
- Exercise history and statistics
- Multi-database support (SQLite & MySQL)
- Admin panel for managing exercises and user data

## Technologies Used
### Frontend
- **HTML**: Markup language for creating the structure of the application.
- **CSS**: Styling for the application to make it visually appealing.
- **JavaScript**: Adds interactivity and visual feedback for the user.
- **Bootstrap**: Provides a responsive and mobile-first layout.

### Backend
- **Django**: Python web framework used for backend logic, database interaction, and routing.

### Posture Detection & Analysis
- **MediaPipe**: Used for real-time pose estimation and keypoint detection.
- **OpenCV**: Handles video processing and frame analysis.
- **Linear Regression**: Utilized to evaluate and correct posture alignment based on detected body landmarks.

### Databases
- **SQLite**: Default database for development.
- **MySQL**: Production database for handling larger datasets.

