# Vue (frontend)
# Use an official Python runtime as a parent image
FROM node:alpine3.16

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the application
RUN npm run build

# Expose port 8080 to the outside world
EXPOSE 8080

# Define the command to run the application when the container starts
CMD ["npm", "run", "serve"]