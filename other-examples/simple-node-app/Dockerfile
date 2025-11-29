# Use a lightweight Node.js image (Alpine Linux based)
FROM node:18-alpine

WORKDIR /app

# 1. Copy ONLY the package.json first
COPY package.json .

# 2. Install dependencies
# Docker will cache this step. If you change server.js but NOT package.json,
# Docker skips this step during re-builds, saving lots of time.
RUN npm install

# 3. Copy the rest of your source code
COPY . .

# Expose the port (optional, but good documentation)
EXPOSE 3000

# Start the application
CMD ["node", "server.js"]