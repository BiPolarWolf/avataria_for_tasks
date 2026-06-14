# ЭТАП 1: Собираем проект (нужен тяжелый Node.js)
FROM node:22-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build   
# <--- ТУТ рождается папка /app/dist с готовым сайтом

# ЭТАП 2: Раздаем проект (Node.js больше не нужен, нужен легкий Nginx)
FROM nginx:stable-alpine as production-stage
# 1. Выкидываем из контейнера всё лишнее, берем чистый Nginx
# 2. Заменяем стандартный конфиг Nginx на наш собственный:
COPY nginx.conf /etc/nginx/conf.d/default.conf
# 3. Копируем результат сборки из ЭТАПА 1 в папку, откуда Nginx раздает файлы:
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]