# FFRHAS Project Overview

## Introduction

**Farnsworth Fusion Reactor Hardware Access Service (FFRHAS)** is a modular Python web application designed for monitoring and controlling a fusion reactor system. It provides a web-based interface, RESTful APIs, and hardware communication modules to interact with various subsystems of the reactor.

---

## Architecture

The project follows a modular structure:

- **Controllers**: Handle business logic and system operations.
- **Routes**: Define API and web endpoints using Flask Blueprints.
- **Services**: Contain reusable logic, database access, and hardware communication.
- **Socket_handler**: Manages real-time data updates via WebSockets.
- **static/**: Contains JavaScript, CSS, and image assets for the frontend.
- **templates/**: HTML templates for rendering web pages.

---

## Main Components

### Web Interface

- Built with Flask and Jinja2 templates.
- Uses Bootstrap for styling.
- Real-time visualization and control via GoJS diagrams and Socket.IO.

### REST API

- Modular endpoints for reactor subsystems (vacuum, high voltage, system status, etc.).
- Easily extendable via Blueprints in the `Routes/` directory.

### Hardware Communication

- Service classes in `Services/` manage direct communication with hardware devices.
- Designed for easy adaptation to new hardware protocols.

### Real-Time Data

- WebSockets (Socket.IO) push live updates to the frontend.
- Example: The overview dashboard updates sensor and system status in real time.

---

## Development Workflow

1. **Clone the repository** and enter the `HAS/` directory.
2. **Install dependencies** with `pip install -r requirements.txt`.
3. **Run the application** using `python app.py`.
4. **Access the web interface** at [http://localhost:5000](http://localhost:5000).

---

## Directory Structure

```
HAS/
  app.py                # Main Flask application
  requirements.txt      # Python dependencies
  Controllers/          # Business logic and system controllers
  Routes/               # API and web route definitions
  Services/             # Service layer for business logic and hardware
  Socket_handler/       # WebSocket and real-time communication
  static/               # Static files (JS, CSS, images)
  templates/            # HTML templates
docs/
  overview.md           # This file
  doxygen/              # Doxygen config and generated docs
    Doxyfile
    html/
    latex/
```

---

## Extending the System

- **Add a new subsystem**: Create a controller in `Controllers/`, a route in `Routes/`, and update templates/static files as needed.
- **Add a new API endpoint**: Define a new route in the appropriate Blueprint.
- **Add new frontend features**: Place JS/CSS in `static/` and update templates.

---

## Documentation

- This overview: [`docs/overview.md`](overview.md)
- API and code documentation: [`docs/doxygen/html/`](doxygen/html/)

---

## License

This project is licensed under the MIT