---
id: 22
title: Android code generation
date: 2010-07-19T09:01:00+00:00
author: filip
layout: post
guid: http://filipfracz.net.holly.arvixe.com/?p=22
permalink: /2010/07/android-code-generation/
tumblr_filipfracz_permalink:
  - http://filipfracz.tumblr.com/post/63249704349/android-code-generation
  - http://filipfracz.tumblr.com/post/63249704349/android-code-generation
tumblr_filipfracz_id:
  - "63249704349"
  - "63249704349"
categories:
  - Programming
  - Uncategorized
tags:
  - android
  - java
---
<p>I started looking more seriously into Android development, especially after a great training session with <a href="http://commonsware.com/Android/">Mark Murphy</a> organized by <a href="http://chicagoandroid.com">Chicago Android</a>. Right now I am experimenting with simple user interfaces (buttons, lists, etc) and learning how to utilize various phone's sensors.</p>

<p>What's caught my attention is the way Android's build tools generate code. The layout for activities, templates, styles and controls is defined in XML files. These are then parsed at build time to extract the IDs, which then become available off the generated &#8220;R&#8221; class. The layout is &#8220;inflated&#8221; at runtime given a numeric ID. That's also how one can get a reference to UI elements.</p>

<p>The use of XML files for UI layout is not unique to Android. In the past I used Glade, Mozilla's XUL and Microsoft's XAML. Lately especially I've been playing XAML. It was a surprise to me that pretty much every single Java sample contains code like this:</p>

<script src="https://gist.github.com/itsff/6850632.js" type="text/javascript"></script>

<p>Seems very repetitive and a lot of silly code to write. Tooling for other frameworks take slightly different approaches. In XAML there is a special namespace used by the XAML parser that allows the user to specify a name for the class member referencing the layout element. For example:</p>

<script src="https://gist.github.com/itsff/6850650.js" type="text/javascript"></script>

<p>results in creation of member variable &#8220;ClearButton&#8221; in the class &#8220;MyCoolWindow&#8221; of &#8220;MySample&#8221; namespace. No need for getting view elements by id and for casting. I'm wondering why can't something like this be done for Android? </p>

<p>I obviously am not even pretending to know anything Android, so I am asking you the experts =)    <br />Is there any technical reason against it?</p>

<p>C# has a concept of partial classes (one class spanning multiple source files), so it's easy to just stick the generated code into its own file. Java's philosophy is different: why span multiple files? Just create multiple classes. Seems like it shouldn't be that difficult.</p>

<p>One could come up with an XML schema for specifying the name (like in XAML). XML allows decorating elements with multiple attributes, so it would work. Or, alternatively, the name specified in android:id could be used, but I think it needs to be unique for all IDs. Specifying a name per class could be more desirable.    <br />Please see a mockup file below: </p>

<script src="https://gist.github.com/itsff/6850663.js" type="text/javascript"></script>

<p>A custom pre-processor tool could be written that would parse the XML files and create a new class for each of them - say &#8220;LayoutXyzHelper&#8221;. These helpers would perform all the findViewById() during construction and expose all desired controls as member variables. A generated helper class for the XML layout above could look like this: </p>
<script src="https://gist.github.com/itsff/6850678.js" type="text/javascript"></script>

<p>The usage would be to construct the layout helper and save it as a &#8220;ui&#8221; member variable.</p>

<script src="https://gist.github.com/itsff/6850673.js" type="text/javascript"></script>

<p>Well, what do you think? Does this sound like a good open-source project idea? Or am I missing something obvious due to my lack of Android experience? Maybe this has already been done? <br />
Either case, please let me know.</p>