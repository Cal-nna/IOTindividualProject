# CalWeb – Real-Time Day/Night Web Visuals via PubNub & Flask

![CalWeb Day Scene](./docs/screenshots/day-mode.png)
![CalWeb Night Scene](./docs/screenshots/night-mode.png)

🔗 **Live site:** https://calweb.online/

---

## Overview

**CalWeb** is a real-time, IoT-inspired web application designed to demonstrate the integration of frontend visuals, backend logic, databases, and real-time messaging.

Rather than focusing on a traditional practical web function, this project prioritises showcasing technical skills gained throughout the course—particularly how external hardware input could influence a live website for all connected users.

Although the physical hardware component was not completed, the system architecture and real-time communication layer were fully implemented, allowing seamless future integration with minimal changes.

---

## Core Concept

- A shared website displays a **day or night scene**
- Scene changes are broadcast in real time using **PubNub**
- All connected users see the visual update instantly
- User interactions are **authenticated and logged**
- The system is designed to accept **hardware input** (e.g. Raspberry Pi sensors)

---

User / Hardware
↓
PubNub
↓
Flask Web App (AWS EC2)
↓
SQLite Database


---

## Features

### 🌤️ Dynamic Day & Night Scenes
- Fully CSS-driven landscape scenes
- Smooth transitions between modes
- Sun, moon, hills, sky gradients, and animated clouds

### 🔐 User Authentication
- Secure user registration and login
- Passwords stored using hashed encryption
- Login-protected scene switching and logs

### 📡 Real-Time Messaging (PubNub)
- Bi-directional communication
- Shared state across all users
- Hardware-ready design

### 🗂️ Scene Change Logging
- Every scene change is logged with:
  - Timestamp
  - Username
  - Old scene → New scene
- Logs viewable on a dedicated page

---

## Technologies Used

### Backend
- Python Flask
- Flask-Login
- SQLAlchemy ORM
- SQLite
- Apache2 + mod_wsgi
- PubNub SDK
- AWS EC2 (Ubuntu)
- HTTPS / SSL

### Frontend
- HTML + Jinja2
- CSS (custom, no frameworks)
- CSS animations & transitions
- JavaScript (Fetch API + PubNub)

---

## Visual Design & CSS Implementation

### Scene-Based Styling

Each page dynamically applies a scene class to the `<body>` element:

```
<body class="{{ scene }}">
```

This allows every page (index, login, register, logs) to inherit the correct visual theme automatically.

Day Mode

Light blue → white sky gradient

Green layered hills

Yellow sun with glow

Soft white clouds drifting across the screen

Night Mode

Deep blue → black gradient sky

Dimmed landscape colours

Moon with subtle glow

Small star-like elements

Smooth Transitions

All scene changes use CSS transitions so the switch feels natural rather than abrupt.

Cloud Animation (Brief Explanation)

Clouds are animated entirely using CSS:

Each cloud is positioned absolutely

A @keyframes animation moves them horizontally

transform: translateX() enables smooth motion

The animation runs infinitely with linear timing

This creates the illusion of clouds drifting across the sky without JavaScript overhead.

Database Structure
Tables
user
Column	Description
id	Primary key
username	Unique username
password_hash	Encrypted password
scene_log
Column	Description
id	Primary key
timestamp	Time of change
username	User who triggered change
old_scene	Previous state
new_scene	New state
## System Architecture

