# FFRHAS

Farnsworth Fusion Reactor Hardware Access Service (FFRHAS) is a modular Python-based web application for monitoring and controlling a fusion reactor system. The project provides a web interface, RESTful APIs, and hardware communication modules to interact with various subsystems of the reactor.

## Features

- Modular architecture with clear separation of controllers, services, routes, and socket handlers
- Web-based user interface (HTML, CSS, JS) for real-time monitoring and control
- REST API endpoints for integration and automation
- Hardware communication modules for direct device access
- Real-time data updates via WebSockets
- Documentation generated with Doxygen

## Project Structure

```
HAS/
  app.py                # Main application entry point
  requirements.txt      # Python dependencies
  Controllers/          # Business logic and system controllers
  Routes/               # API and web route definitions
  Services/             # Service layer for business logic
  Socket_handler/       # WebSocket and real-time communication
  static/               # Static files (JS, CSS, images)
  templates/            # HTML templates
docs/
  overview.md           # Project overview and documentation
  doxygen/              # Doxygen config and generated docs
    Doxyfile
    html/
    latex/
```

## Getting Started

### Prerequisites

- Python 3.8+
- (Recommended) Run in a dev container or virtual environment

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/mendax0110/FFRHAS.git
   cd FFRHAS/HAS
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

```sh
python app.py
```

The web interface will be available at `http://localhost:5000` (or the port specified in your configuration).

### Development

- Static assets are in `HAS/static/`
- HTML templates are in `HAS/templates/`
- Main logic is in `HAS/app.py` and submodules
- Configuration is typically handled in `app.py` or via environment variables

### Documentation

- Project documentation is in [docs/overview.md](docs/overview.md)
- API and code documentation is generated with Doxygen and available in [docs/doxygen/html/](docs/doxygen/html/)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
