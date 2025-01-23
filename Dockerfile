# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install http-server globally
RUN npm install -g http-server

# Copy all files
COPY . .

# Expose port 8000
EXPOSE 8000

# Start the application
CMD ["http-server", "-p", "8000"]
