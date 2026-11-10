# Этап 1: Сборка Vue-приложения
FROM node:20-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Этап 2: Раздача статики через Nginx
FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
# Копируем конфиг nginx, который будет раздавать статику
COPY nginx.conf /etc/nginx/conf.d/default.conf