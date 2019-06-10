---
id: 594
title: Crypto Trading Framework
date: 2017-09-09T00:51:54+00:00
author: filip
layout: post
guid: https://filipfracz.net/?p=594
permalink: /2017/09/crypto-trading-framework/
image: /wp-content/uploads/11297228794_d1c5d01559_b1-680x510.jpg
categories:
  - Programming
  - Project
tags:
  - bitcoin
  - cryptocurrency
  - csharp
  - ethereum
  - gdax
---
<pre><strong><a href="https://github.com/itsff/m3f-trading-system">https://github.com/itsff/m3f-trading-system</a></strong></pre>

In my free time, I've been messing around with cryptocurrencies. Bitcoin, Ether, Litecoin as well as a couple of other, lesser known altcoins. I am mainly using [GDAX](https://gdax.com) and [Bitfinex](https://bitfinex.com) for my trades. It's a lot of fun!

Pretty much all exchanges offer some sort of API. I created a simple .NET client for the GDAX and wrote a simple trading framework. I decided to learn the Akka.net actor model for this project, as it makes writing trading bots easier. Speed is not an issue, as I've noticed GDAX's position tracking system cannot keep up with my apps.

Today I have open sourced my framework on GitHub under revised BSD license. You can [clone it from here](https://github.com/itsff/m3f-trading-system). It ships with a simple &#8220;buy low sell high&#8221; strategy which illustrates how to consume prices and interact with orders.  More exchange backends to come (or feel free to contribute more).