# CalWeb – Real-Time Day/Night Web Visuals via PubNub & Flask

🔗 **Live site:** https://calweb.online/

---

## Overview

**CalWeb** is a real-time, IoT-inspired web application designed to demonstrate the integration of frontend visuals, backend services, databases, and real-time messaging.

Rather than solving a traditional practical problem, the project focuses on showcasing technical skills developed throughout the course—particularly how **external hardware input** (such as a Raspberry Pi) could influence a live website shared by multiple users.

Although the physical hardware component was not completed, the system architecture and real-time communication layer were fully implemented, allowing **seamless future hardware integration with minimal changes**.

---

## Core Concept

- A shared website displays either a **day** or **night** scene
- Scene changes are broadcast in real time using **PubNub**
- All connected clients see visual updates instantly
- User interactions are **authenticated and logged**
- The system is designed to accept **external hardware input** (e.g. Raspberry Pi sensors)

---

## Features

### 🌤️ Dynamic Day & Night Scenes
- Fully CSS-driven animated landscapes
- Smooth transitions between day and night modes
- Visual elements include:
  - Sky gradients
  - Layered hills
  - Sun and moon with glow effects
  - Animated drifting clouds

### 🔐 User Authentication
- Secure user registration and login
- Passwords stored using **hashed encryption**
- Scene switching and log access restricted to authenticated users

### 📡 Real-Time Messaging (PubNub)
- Bi-directional publish/subscribe communication
- Shared visual state across all users
- Architecture ready for hardware-based publishers

### 🗂️ Scene Change Logging
- Every scene change is recorded with:
  - Timestamp
  - Username
  - Previous scene → New scene
- Logs displayed on a dedicated webpage

---

## Technologies Used

### Backend
- Python Flask
- Flask-Login
- SQLAlchemy ORM
- SQLite
- Apache2 with mod_wsgi
- PubNub SDK
- AWS EC2 (Ubuntu)
- HTTPS / SSL

### Frontend
- HTML with Jinja2 templating
- Custom CSS (no frameworks)
- CSS animations and transitions
- JavaScript (Fetch API + PubNub SDK)

---

## Visual Design & CSS Implementation

### Scene-Based Styling

Each page dynamically applies a scene class to the `<body>` element:

```html
<body class="{{ scene }}">
```
### Scene Propagation Across Pages

Once the scene class is applied to the `<body>` element, **all child elements automatically inherit the visual context** defined in the CSS.

From this point onward, page-specific content (buttons, forms, logs, etc.) is layered *on top* of the scene without needing to redefine styles.

Example (index.html):


<body class="{{ scene }}">
    <h1>{{ scene | capitalize }} Mode</h1>

    <div class="controls">
        <button onclick="setMode('day')">Day</button>
        <button onclick="setMode('night')">Night</button>
    </div>
</body>
