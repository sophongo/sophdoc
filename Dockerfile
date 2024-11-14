# 构建阶段
FROM python:3.12-slim AS builder

WORKDIR /docs

# 安装 mkdocs 和依赖
RUN pip install --no-cache-dir \
    mkdocs \
    mkdocs-material \
    mkdocs-minify-plugin \
    pymdown-extensions \
    mkdocs-swagger-ui-tag \
    mkdocs-static-i18n

# 复制项目文件
COPY . /docs

# 构建静态文件
RUN mkdocs build -f mkdocs.yml

# Nginx 阶段
FROM nginx:alpine

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从构建阶段复制构建好的静态文件
COPY --from=builder /docs/site /usr/share/nginx/html

# 暴露端口
EXPOSE 8000

# Nginx 使用 daemon off 模式运行
CMD ["nginx", "-g", "daemon off;"]