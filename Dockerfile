# Use official Node.js image
FROM node:22

# Create app directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Install Playwright browsers
RUN npx playwright install

# Copy app source
COPY . .

# Expose port (Render auto-detects this)
EXPOSE 10000

# Start server
CMD ["node", "index.js"]
