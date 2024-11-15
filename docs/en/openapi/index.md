# OpenAPI Documentation

This is some OpenAPI documentation aimed at developers.

- [CloudHost OpenAPI Documentation](./virtnest/index.md)
- [AI Lab OpenAPI Documentation](./baize/index.md)
- [Container Management OpenAPI Documentation](./kpanda/index.md)
- [Insight OpenAPI Documentation](./insight/index.md)
- [Global Management OpenAPI Documentation](./ghippo/index.md)

## Obtaining OpenAPI Access Keys

Access Keys can be used to access the OpenAPI and for continuous publishing.
You can follow the steps below to obtain their keys and access the API in their personal center.

Log in to the AI platform, find __Personal Center__ in the dropdown menu at
the top right corner, and manage your account's access keys on the __Access Keys__ page.

![ak list](../admin/ghippo/images/platform02.png)

![created a key](../admin/ghippo/images/platform03.png)

!!! info

    Access key information is displayed only once. If you forget the access key information, you will need to create a new access key.

## Using the Key to Access the API

When accessing the AI platform's OpenAPI, include the request header `Authorization:Bearer ${token}`
in the request to identify the visitor's identity, where `${token}` is the key obtained in the previous step.

**Request Example**

```bash
curl -X GET -H 'Authorization:Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkRKVjlBTHRBLXZ4MmtQUC1TQnVGS0dCSWc1cnBfdkxiQVVqM2U3RVByWnMiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2NjE0MTU5NjksImlhdCI6MTY2MDgxMTE2OSwiaXNzIjoiZ2hpcHBvLmlvIiwic3ViIjoiZjdjOGIxZjUtMTc2MS00NjYwLTg2MWQtOWI3MmI0MzJmNGViIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJncm91cHMiOltdfQ.RsUcrAYkQQ7C6BxMOrdD3qbBRUt0VVxynIGeq4wyIgye6R8Ma4cjxG5CbU1WyiHKpvIKJDJbeFQHro2euQyVde3ygA672ozkwLTnx3Tu-_mB1BubvWCBsDdUjIhCQfT39rk6EQozMjb-1X1sbLwzkfzKMls-oxkjagI_RFrYlTVPwT3Oaw-qOyulRSw7Dxd7jb0vINPq84vmlQIsI3UuTZSNO5BCgHpubcWwBss-Aon_DmYA-Et_-QtmPBA3k8E2hzDSzc7eqK0I68P25r9rwQ3DeKwD1dbRyndqWORRnz8TLEXSiCFXdZT2oiMrcJtO188Ph4eLGut1-4PzKhwgrQ' https://demo-dev.daocloud.io/apis/ghippo.io/v1alpha1/users?page=1&pageSize=10 -k
```

**Request Result**

```json
{
    "items": [
        {
            "id": "a7cfd010-ebbe-4601-987f-d098d9ef766e",
            "name": "a",
            "email": "",
            "description": "",
            "firstname": "",
            "lastname": "",
            "source": "locale",
            "enabled": true,
            "createdAt": "1660632794800",
            "updatedAt": "0",
            "lastLoginAt": ""
        }
    ],
    "pagination": {
        "page": 1,
        "pageSize": 10,
        "total": 1
    }
}
```
