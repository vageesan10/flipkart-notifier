FROM mcr.microsoft.com/playwright:v1.54.1-jammy

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["node", "index.js"]
