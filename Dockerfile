FROM ghcr.io/puppeteer/puppeteer:latest

USER root

# Set working directory
WORKDIR /usr/src/app

# Copy package files from subdirectory
COPY auto-verify-tool/package*.json ./

# Install dependencies
RUN npm install

# Copy source code from subdirectory
COPY auto-verify-tool/ .

# Expose port
EXPOSE 3000

# Start the application
CMD [ "node", "server.js" ]
