FROM mcr.microsoft.com/playwright:v1.54.1-jammy

WORKDIR /app

COPY package*.json ./

RUN npm install

# THIS IS CRUCIAL!
RUN npx playwright install

COPY . .

CMD ["node", "index.js"]
