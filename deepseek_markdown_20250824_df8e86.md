# TV Wall Control Panel

A Dockerized web application to control a Samsung TV wall comprised of 4 displays.

## Prerequisites

- Docker
- Docker Compose

## Configuration

1. Update the TV IP addresses in the `docker-compose.yml` file or set the `TV_IPS` environment variable
2. If using MagicInfo/Optisigns, set the appropriate environment variables

## Building and Running

```bash
# Clone or download this project
cd tv-wall-control

# Build and start the container
docker-compose up -d

# The application will be available at http://localhost:8080