---
id: 117
title: SafeBuffer and UnmanagedMemoryStream
date: 2013-10-10T01:11:53+00:00
author: filip
layout: post
guid: http://filipfracz.net/?p=117
permalink: /2013/10/safebuffer/
categories:
  - Programming
tags:
  - C
  - c++/cli
  - csharp
  - managed
  - native
  - programming
---
At work I have a situation where I have some binary data allocated in the native code. It's pretty much a raw `char*`. I then would like to access that same information from the managed side. But how? Of course I can just copy the data to a `byte[]` but that's just wasteful.

I did some googling around and found the obvious solution - UnmanagedMemoryStream. It can take pointers, or a SafeBuffer. The latter is basically a smart wrapper around memory handle. Take a look at the code I came up with. I hope somebody will find it useful. It's still work in progress and can use some love, so any comments are welcome.

<script src="https://gist.github.com/itsff/6818217.js"></script>

I needed to pass the `std::unique_ptr` as r-value, otherwise the linker complains (thunks for non-existent copy constructor). I still need to clean this code up to handle custom deleters. But it serves my needs for now.

Edit: There is a bug in this code. Can you spot it? ;)