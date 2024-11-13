# 如何将AI 算力中心集成到客户系统（OEM OUT）

OEM OUT 是指将 AI 算力中心作为子模块接入其他产品，出现在其他产品的菜单中。
用户登录其他产品后可直接跳转至 AI 算力中心无需二次登录。实现 OEM OUT 共分为 5 步，分别是：

* [统一域名](#_1)
* [打通用户体系](#_2)
* [对接导航栏](#_3)
* [定制外观](#_4)
* [打通权限体系(可选)](#_5)

## 统一域名

1. 部署 AI 算力中心（假设部署完的访问地址为 `https://10.6.8.2:30343/`）

1. 客户系统和 AI 算力中心前可以放一个 nginx 反代来实现同域访问，
   __/__ 路由到客户系统， __/dce5 (subpath)__ 路由到 AI 算力中心系统， __vi /etc/nginx/conf.d/default.conf__ 示例如下：

    ```nginx
    server {
        listen       80;
        server_name  localhost;
    
        location /dce5/ {
          proxy_pass https://10.6.8.2:30343/;
          proxy_http_version 1.1;
          proxy_read_timeout 300s; # 如需要使用 kpanda cloudtty功能需要这行，否则可以去掉
          proxy_send_timeout 300s; # 如需要使用 kpanda cloudtty功能需要这行，否则可以去掉
    
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    
          proxy_set_header Upgrade $http_upgrade; # 如需要使用 kpanda cloudtty功能需要这行，否则可以去掉
          proxy_set_header Connection $connection_upgrade; # 如需要使用 kpanda cloudtty功能需要这行，否则可以去掉
        }
        
        location / {
            proxy_pass https://10.6.165.50:30443/; # 假设这是客户系统地址(如意云)
            proxy_http_version 1.1;
    
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

1. 假设 nginx 入口地址为 10.6.165.50，按[自定义 AI 算力中心反向代理服务器地址](../../install/reverse-proxy.md)把
   AI_PROXY 反代设为 `http://10.6.165.50/dce5`。确保能够通过 `http://10.6.165.50/dce5`访问 AI 算力中心。
   客户系统也需要进行反代设置，需要根据不同平台的情况进行处理。
  
    ![反向代理](https://docs.daocloud.io/daocloud-docs-images/docs/zh/docs/ghippo/best-practice/oem/images/agent.png)

## 打通用户体系

将客户系统与 AI 算力中心平台通过 OIDC/OAUTH 等协议对接，使用户登录客户系统后进入 AI 算力中心时无需再次登录。
在拿到客户系统的 OIDC 信息后填入 __全局管理__ -> __用户与访问控制__ -> __身份提供商__ 中。

![身份提供商](https://docs.daocloud.io/daocloud-docs-images/docs/zh/docs/ghippo/best-practice/oem/images/idp.png)

对接完成后，AI 算力中心登录页面将出现 OIDC（自定义）选项，首次从客户系统进入 AI 算力中心时选择通过 OIDC 登录，
后续将直接进入 AI 算力中心无需再次选择。

![登录页](https://docs.daocloud.io/daocloud-docs-images/docs/zh/docs/ghippo/best-practice/oem/images/login.png)

## 对接导航栏

对接导航栏是指 AI 算力中心出现在客户系统的菜单中，用户点击相应的菜单名称能够直接进入 AI 算力中心。
因此对接导航栏依赖于客户系统，不同平台需要按照具体情况进行处理。

## 定制外观

通过 __全局管理__ -> __平台设置__ -> __外观定制__ 可以自定义平台背景颜色、logo、名称等，
具体操作请参照[外观定制](../../user-guide/platform-setting/appearance.md)。

## 打通权限体系（可选）

打通权限较为复杂，如有需求请联系全局管理团队。

## 参考

- [OEM IN 文档](./oem-in.md)
