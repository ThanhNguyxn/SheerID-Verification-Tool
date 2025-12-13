FROM ghcr.io/puppeteer/puppeteer:latest

USER root

# Set working directory
WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start the application
CMD [ "node", "server.js" ]
