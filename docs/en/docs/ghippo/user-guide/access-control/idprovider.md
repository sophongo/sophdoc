# Identity provider

Global management supports single sign-on based on LDPA and OIDC protocols. If your enterprise or organization has its own account system and you want to manage members in the organization to use AI platform resources, you can use the identity provider feature provided by global management. Instead of having to create username/passwords for every organization member in your AI platform. You can grant permissions to use AI platform resources to these external user identities.

## Basic concept

- Identity Provider (IdP for short)

    Responsible for collecting and storing user identity information, usernames, and passwords, and responsible for authenticating users when they log in. In the identity authentication process between an enterprise and AI platform, the identity provider refers to the identity provider of the enterprise itself.

- Service Provider (SP)

    The service provider establishes a trust relationship with the identity provider IdP, and uses the user information provided by the IDP to provide users with specific services. In the process of enterprise authentication with AI platform, the service provider refers to AI platform.

- LDAP

    LDAP refers to Lightweight Directory Access Protocol (Lightweight Directory Access Protocol), which is often used for single sign-on, that is, users can log in with one account password in multiple services. Global management supports LDAP for identity authentication, so the enterprise IdP that establishes identity authentication with AI platform through the LDAP protocol must support the LDAP protocol. For a detailed description of LDAP, please refer to: [Welcome to LDAP](ldap.md).

- OIDC

    OIDC, short for OpenID Connect, is an identity authentication standard protocol based on the OAuth 2.0 protocol. Global management supports the OIDC protocol for identity authentication, so the enterprise IdP that establishes identity authentication with AI platform through the OIDC protocol must support the OIDC protocol. For a detailed description of OIDC, please refer to: [Welcome to OpenID Connect](https://openid.net/connect/).

- OAuth 2.0

    OAuth 2.0 is the abbreviation of Open Authorization 2.0. It is an open authorization protocol. The authorization framework supports third-party applications to obtain access permissions in their own name.

## Features

- Administrators do not need to recreate AI platform users

    Before using the identity provider for identity authentication, the administrator needs to create an account for the user in the enterprise management system and AI platform respectively; after using the identity provider for identity authentication, the enterprise administrator only needs to create an account for the user in the enterprise management system, Users can access both systems at the same time, reducing personnel management costs.

- Users do not need to remember two sets of platform accounts

    Before using the identity provider for identity authentication, users need to log in with the accounts of the two systems to access the enterprise management system and AI platform; after using the identity provider for identity authentication, users can log in to the enterprise management system to access the two systems.
