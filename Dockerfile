FROM ghcr.io/puppeteer/puppeteer:latest

USER root

# Set working directory
WORKDIR /usr/src/app

# Copy package files from subdirectory
COPY auto-verify-tool/package*.json ./

# Skip Chromium download for Puppeteer (using base image's Chrome)
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Install dependencies
RUN npm install

# Copy source code from subdirectory
COPY auto-verify-tool/ .

# Expose port
EXPOSE 3000

# Start the application
CMD [ "node", "server.js" ]
