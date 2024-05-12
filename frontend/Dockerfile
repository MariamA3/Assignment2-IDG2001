# Use an official node runtime as a base image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your app's source code
COPY . .

# Build your app
RUN npm run build

# Install serve to serve the build folder
RUN npm install -g serve

# Expose the port the app will run on
EXPOSE 3000

# Serve the app
CMD ["serve", "-s", "build", "-l", "3000"]
