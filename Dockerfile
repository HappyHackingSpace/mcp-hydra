# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⠟⠙⠻⠿⠋⠙⠻⠷⠄⠀⠀⠀⠀⠀⠀⢸⣿
# ⣿⣿⣿⣿⣿⣿⠿⢿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿
# ⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣇⡀⠀⠈⠻⠿⣿⣿
# ⣿⣿⣿⠉⠉⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣷⣶⣶⣿⣿
# ⣿⠿⠟⠀⠀⠀⢀⣠⣾⣿⡿⠻⠿⠟⠙⠿⠟⠻⣿⡆⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⠀⠀⠀⠀⢀⣾⠏⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿
# ⣿⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⣠⣤⣶⣶⣶⣶⣦⡄⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿
# ⣿⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⣾⣿⣿⣆⣤⣾⣿⣿⣿
# ⣿⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣦⠈⣻⣿⣿⣿⣿⣿⣿⣿
# ⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢻⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⠀⠀⠀⠀⢀⣠⣤⣤⣤⣄⣀⠀⠀⠈⠛⠹⣿⠷⣄⠀⠀⠀⠀⠉⠉⠉⣹⣿⣿
# ⣿⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣶⣿⣿⣿
# ⣿⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣆⡀⠀⠈⠻⠿⣿⣿⣿
# ⣿⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿

# Start from official Kali Linux image
FROM kalilinux/kali-rolling

# Set working directory
WORKDIR /app

# Environment variable to suppress interaction during apt installs
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt update && apt install -y \
    gnupg \
    curl \
    wget \
    unzip \
    git \
    iproute2 \
    iputils-arping \
    iputils-ping \
    net-tools \
    zmap \
    nmap \
    sublist3r \
    wpscan \
    dnsrecon \
    sqlmap \
    ca-certificates \
    tesseract-ocr \
    build-essential \
    ruby-full \
    python3 \
    python3-pip \
    python3-venv \
    python3-setuptools \
    python3-pil \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Set up tools directory
RUN mkdir -p /tools
ENV PATH="/tools:${PATH}"

# Set up virtual environment for Python packages
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install setuptools in the virtual environment
RUN pip install --upgrade pip setuptools wheel

# Clone and install Holehe
RUN git clone https://github.com/megadose/holehe.git && \
    cd holehe && \
    python3 setup.py install


# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Make banner.sh executable
RUN chmod +x /app/banner.sh

# Create entrypoint script
RUN echo '#!/bin/bash\n/app/banner.sh\nexec "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Set the default command
CMD ["python", "server.py"]
