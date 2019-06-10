---
id: 412
title: Docker Compose
date: 2016-01-06T18:00:35+00:00
author: filip
layout: post
guid: http://filipfracz.net/?p=412
permalink: /2016/01/docker-compose/
categories:
  - Personal
  - Programming
  - Project
tags:
  - cloud
  - docker
  - linux
  - programming
  - project
  - TT API
---
While I was working for Trading Technologies, we always planned on using Linux Containers to provide secure hosting of user-written TT SDK algos. Docker was supposed to be the way of ensuring proper isolation, resource management, as well as means of convenient deployment of client strategies. The infrastructure was in place, but I left before we had a chance to materialize our plans.

Recently I decided to give Docker another go, this time as a way of managing my various cloud projects. I was [happy with DigitalOcean's offering](http://filipfracz.net/2015/12/hacktoberfest/), so I began migrating my websites and jobs to their cloud. Everything, of course, is containerized and managed together. I am using Ubuntu 14.04 with Docker Compose.

I must say I am pleased with the results. The migration has been rather painless, and I like how simple the config ended up. I am running a container with a shared MariaDB (MySQL) database, a reverse-proxy Nginx to manage routing, several WordPress blog containers, few C# ASP.NET sites (Mono, not CoreCLR), some Python sites (Flask), and bunch of Python/C++ apps. A sample docker-compose.yml file is shown below.



As you can see, I am using [dmp1ce/nginx-proxy-letsencrypt](https://github.com/dmp1ce/nginx-proxy-letsencrypt) image as a web proxy. Just like with [jwilder/nginx-proxy](http://jasonwilder.com/blog/2014/03/25/automated-nginx-reverse-proxy-for-docker/), it's dead simple to configure routes. All a container needs to do is to specify _VIRTUAL_HOST=something.com_ variable, and the web traffic will be forwarded to its exposed port. Image [dmp1ce/nginx-proxy-letsencrypt](https://github.com/dmp1ce/nginx-proxy-letsencrypt) has [LetsEncrypt.org](https://letsencrypt.org/) support built right in. Specify _LETSENCRYPT_HOST_ and _LETSENCRYPT_EMAIL_ and voilà- free SSL for your site 🙂