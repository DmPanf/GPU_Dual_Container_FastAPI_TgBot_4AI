## AUTH

# MiniDLNA Server Setup in Docker 🐳🎞️

Welcome to our guide on setting up a MiniDLNA (Digital Living Network Alliance) server in Docker. This will allow you to stream your media files to any DLNA-compatible devices on your network. 🎶📺

## Prerequisites 📋

Before you start, ensure you have:

- Docker and Docker Compose installed on your system.
- Basic knowledge of Docker, Docker Compose, and networking.
- Media files you want to share using DLNA.

## Installation 🛠️

### Step 1: Clone the Repository

Clone this repository to get the Dockerfile and docker-compose.yml:

```bash
git clone [URL-to-this-repository]
cd [Repository-Name]
```

### Step 2: Build the Docker Image

First, modify the provided Dockerfile to set up MiniDLNA instead of the Python bot. Your Dockerfile should look something like this:

```Dockerfile
# Use a base image with MiniDLNA installed
FROM alpine:latest

# Install MiniDLNA
RUN apk add --no-cache minidlna

# Copy the MiniDLNA configuration file
COPY minidlna.conf /etc/minidlna.conf

# Expose DLNA ports
EXPOSE 8200 1900/udp

# Start MiniDLNA
CMD ["minidlnad", "-d"]
```

### Step 3: Configure MiniDLNA

Create a `minidlna.conf` file with your MiniDLNA configuration. Make sure to specify the media directories and port numbers.

### Step 4: Set Up Docker Compose

Modify `docker-compose.yml` to set up the MiniDLNA service:

```yaml
version: '3'

services:
  minidlna:
    build: .
    container_name: minidlna
    ports:
      - "8200:8200"
      - "1900:1900/udp"
    volumes:
      - /path/to/your/media:/media
    restart: unless-stopped
```

Replace `/path/to/your/media` with the path to your media files on the host machine.

### Step 5: Start the MiniDLNA Server

Run the following command to start the MiniDLNA server:

```bash
docker-compose up -d
```

## Accessing Your Media 📺🎵

Once the MiniDLNA server is running, you can access your media files from any DLNA-compatible device on the same network. Just look for the server named 'MiniDLNA' on your device.

## Maintenance Commands 🧰

- To check the status of your MiniDLNA container:
  ```bash
  docker ps -a
  ```

- To view the logs of your MiniDLNA server:
  ```bash
  docker logs minidlna
  ```

- To restart the MiniDLNA server:
  ```bash
  docker-compose restart
  ```

- To stop the MiniDLNA server:
  ```bash
  docker-compose down
  ```

## Troubleshooting 🛠

- **No Media Files Found**: Ensure your media files are correctly placed in the specified directory and the directory is correctly mounted in Docker.
- **Networking Issues**: Verify if the ports are correctly exposed and not blocked by any firewall.

## Contribution and Support 🤝

Feel free to contribute to this project by submitting pull requests or opening issues for any improvements or suggestions.

For support, please open an issue in this repository.

## License 📜

This project is licensed under [LICENSE-NAME]. See the [LICENSE](LICENSE) file for details.
