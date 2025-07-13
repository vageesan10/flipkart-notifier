FROM node:22

WORKDIR /app

COPY package*.json ./
RUN npm install

# Install Playwright browsers & dependencies
RUN npx playwright install --with-deps

COPY . .

EXPOSE 10000

CMD ["node", "index.js"]
