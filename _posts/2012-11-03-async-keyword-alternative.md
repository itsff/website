---
id: 34
title: Async keyword alternative
date: 2012-11-03T09:09:00+00:00
author: filip
layout: post
guid: http://filipfracz.net.holly.arvixe.com/?p=34
permalink: /2012/11/async-keyword-alternative/
tumblr_filipfracz_permalink:
  - http://filipfracz.tumblr.com/post/63249700887/async-keyword-alternative
  - http://filipfracz.tumblr.com/post/63249700887/async-keyword-alternative
tumblr_filipfracz_id:
  - "63249700887"
  - "63249700887"
categories:
  - Programming
  - Uncategorized
---
Unfortunately, both MonoTouch and Mono for Android still don't support the async keyword. Raw TPL is rather inconvenient to use. You have to remember to catch exceptions, return faulted tasks, etc. ContinueWith can also be inefficient due to thread switching.

Today while browsing the interwebs I came across Brad Wilson's [blog post](http://bradwilson.typepad.com/blog/2012/04/tpl-and-servers-pt4.html "TPL") which led me to these [two](http://aspnetwebstack.codeplex.com/SourceControl/changeset/view/6b5687093715#src%2fCommon%2fTaskHelpers.cs) [files](http://aspnetwebstack.codeplex.com/SourceControl/changeset/view/6b5687093715#src%2fCommon%2fTaskHelpers.cs). [TaskHelpers](http://aspnetwebstack.codeplex.com/SourceControl/changeset/view/6b5687093715#src%2fCommon%2fTaskHelpers.cs) are (no pun intended) very very helpful! The extension methods emulate the await goodness pretty well.

I modified them a little bit. [Here is a gist](https://gist.github.com/4681026).