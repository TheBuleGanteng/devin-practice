# Streamlit OpenAI Demo

A simple Streamlit application that integrates with OpenAI's API to provide an interactive chat interface.

## Features

- Interactive chat interface with OpenAI models
- Configurable model selection (GPT-3.5, GPT-4, GPT-4 Turbo)
- Adjustable parameters (temperature, max tokens)
- Streaming responses for real-time interaction
- Branded for Kebayoran Technologies

## Setup

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

### Production Deployment (Docker Container)

1. **Add as submodule to your main repository:**
   ```bash
   cd /path/to/your/main/repo
   git submodule add https://github.com/your-username/devin-practice.git
   git submodule update --init --recursive
   ```

2. **Set up environment variables:**
   ```bash
   # Create or update your .env file in the main repository
   echo "OPENAI_API_KEY=your-api-key-here" >> .env
   ```

3. **Deploy with Docker Compose:**
   ```bash
   cd devin-practice

   # Build and start the container
   docker-compose up -d --build

   # Or if you have a main docker-compose.yml, add this service to it
   ```

4. **Configure nginx:**
   ```bash
   # Add the location block from nginx-demo.conf to your existing nginx configuration
   # This should go inside your server block for www.kebayorantechnologies.com

   sudo nano /etc/nginx/sites-available/your-site-config

   # Test nginx configuration
   sudo nginx -t

   # Reload nginx
   sudo systemctl reload nginx
   ```

5. **Verify deployment:**
   - Check container status: `docker-compose ps`
   - Check logs: `docker-compose logs -f streamlit-demo`
   - Visit: https://www.kebayorantechnologies.com/demo-devin

### Alternative: Integrate with Main Docker Compose

If you have a main `docker-compose.yml` file, you can add this service:

```yaml
services:
  # ... your existing services ...

  devin-streamlit-demo:
    build: ./devin-practice
    container_name: devin-streamlit-demo
    restart: unless-stopped
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    ports:
      - "8501:8501"
    networks:
      - your-main-network
```

## Configuration

The app uses the following environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required)

## File Structure

```
devin-practice/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Docker Compose setup
├── .dockerignore           # Docker ignore file
├── .envrc                  # Environment variables (for direnv)
├── streamlit-demo.service  # Systemd service configuration (legacy)
├── nginx-demo.conf         # Nginx location block
└── README.md              # This file
```

## Troubleshooting

### Docker Deployment
- **Container won't start**: Check `docker-compose logs streamlit-demo` for error logs
- **502 Bad Gateway**: Ensure the container is running and accessible on port 8501
- **API errors**: Verify your OpenAI API key is correctly set in the environment variables
- **Build issues**: Try `docker-compose build --no-cache` to rebuild from scratch

### Legacy Systemd Deployment
- **Service won't start**: Check `sudo journalctl -u streamlit-demo.service` for error logs
- **Path issues**: Make sure all paths in the service file are absolute and correct

### General Issues
- **Port conflicts**: Ensure port 8501 isn't already in use
- **Network issues**: Check that the container can reach external APIs (OpenAI)
- **Memory issues**: Streamlit apps can be memory-intensive with large conversations
