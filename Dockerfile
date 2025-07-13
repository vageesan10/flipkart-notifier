# ✅ Use Playwright's official image with ALL deps!
FROM mcr.microsoft.com/playwright:v1.54.1-jammy


WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "start"]
