ARG LISTEN_PORT=80

FROM nginx:alpine

ARG LISTEN_PORT

# 复制静态文件
COPY index.html /usr/share/nginx/html/
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/
COPY chapters/ /usr/share/nginx/html/chapters/
COPY images/ /usr/share/nginx/html/images/

# Nginx 配置：端口可配 + gzip + 缓存
RUN echo "server { \
    listen ${LISTEN_PORT}; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    \
    gzip on; \
    gzip_types text/html text/css application/javascript image/svg+xml; \
    gzip_min_length 512; \
    \
    location /css/   { expires 30d; add_header Cache-Control \"public, immutable\"; } \
    location /js/    { expires 30d; add_header Cache-Control \"public, immutable\"; } \
    location /images/{ expires 30d; add_header Cache-Control \"public, immutable\"; } \
    \
    location / { \
        try_files \$uri \$uri/ /index.html; \
        add_header Cache-Control \"no-cache\"; \
    } \
}" > /etc/nginx/conf.d/default.conf

EXPOSE ${LISTEN_PORT}

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://localhost:${LISTEN_PORT}/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
