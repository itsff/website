---
id: 10
title: 'Diamond – Java 7 new feature'
date: 2009-06-05T10:40:00+00:00
author: filip
layout: post
guid: http://filipfracz.net.holly.arvixe.com/?p=10
permalink: /2009/06/diamond-java-7-new-feature/
tumblr_filipfracz_permalink:
  - http://filipfracz.tumblr.com/post/63249707903/diamond-java-7-new-feature
  - http://filipfracz.tumblr.com/post/63249707903/diamond-java-7-new-feature
tumblr_filipfracz_id:
  - "63249707903"
  - "63249707903"
categories:
  - Programming
  - Uncategorized
tags:
  - java
  - programming
---
I spotted an <a href="http://www.infoq.com/news/2009/06/openjdk7-m3">article on InfoQ</a> summarizing new futures of the upcoming JDK 7. Coming from a Java background, I was really curious to see what's in store. The article noted several `small language enhancements`, so I binged around (yes, I actually used <a href="http://bing.com">bing</a>), and found the <a href="http://blogs.sun.com/darcy/entry/javaone_2009_project_coin_slides">presentation slides</a> from JavaOne by Joe Darcy.

<p>While many of the enhancements make sense, I was really stunned by the &#8220;diamond operator&#8221; (page 64 of the slides). The point of it is to reduce typing when declaring generic types. Why specify the type twice, if you can do it in one spot?</p>
<script src="https://gist.github.com/itsff/fff3cc6e10ca7d62c67c.js" type="text/javascript"></script>


<p>This reminded my of the <a href="http://msdn.microsoft.com/en-us/library/bb383973.aspx">var keyword in C#</a> and the C++0x's new incarnation of the <a href="http://en.wikipedia.org/wiki/C%2B%2B0x">auto keyword</a>. The difference is that the diamond operator occurs on the right-hand-side, while the type is specified on the left. Doesn't seem like a big deal, but in my opinion this idea is very short sighted.</p>

By having the type on the right-hand-side, both C# and C++ allow much more flexibility. They can handle not only type inference of generics, but pretty much of anything. Specifying type on the right is very natural, and mimics assignment `from right to left`. It seems silly of Java to ignore this obvious and proven strategy and instead introduce a new operator. This will be confusing for those programmers who do work with many different languages, and will make Java feel out of place and underpowered. For comparison, this is what Java could have had if it adopted the `auto` keyword:

<script src="https://gist.github.com/itsff/ca094fe0aa73625baf4b.js" type="text/javascript"></script>


<p>The above (or their equivalents) are already available in C# 3.0 and in draft C++0x. Unfortunately (<a href="http://blogs.sun.com/darcy/entry/javaone_2009_project_coin_slides#comments">judging by Joe's comments</a>) Java 7 will be released without such type inference mechanisms. Disappointing, very disappointing&#8230;</p>