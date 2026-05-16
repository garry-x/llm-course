FROM nginx:alpine

# 复制静态文件
COPY index.html /usr/share/nginx/html/
COPY favicon.svg favicon.png favicon.ico /usr/share/nginx/html/
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/
COPY chapters/ /usr/share/nginx/html/chapters/
COPY images/ /usr/share/nginx/html/images/

# Nginx 配置：SPA 路由 + gzip + 缓存
RUN echo 'server { \
    listen 80; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    \
    # gzip 压缩文本资源 \
    gzip on; \
    gzip_types text/html text/css application/javascript image/svg+xml; \
    gzip_min_length 512; \
    \
    # 静态资源长缓存 \
    location /css/   { expires 30d; add_header Cache-Control "public, immutable"; } \
    location /js/    { expires 30d; add_header Cache-Control "public, immutable"; } \
    location /images/{ expires 30d; add_header Cache-Control "public, immutable"; } \
    \
    # HTML 不缓存（内容可能更新） \
    location / { \
        try_files $uri $uri/ /index.html; \
        add_header Cache-Control "no-cache"; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
