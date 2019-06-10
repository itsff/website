---
id: 8
title: Windows Forms on Japanese XP
date: 2009-04-01T11:23:00+00:00
author: filip
layout: post
guid: http://filipfracz.net.holly.arvixe.com/?p=8
permalink: /2009/04/windows-forms-on-japanese-xp/
tumblr_filipfracz_permalink:
  - http://filipfracz.tumblr.com/post/63249708431/windows-forms-on-japanese-xp
  - http://filipfracz.tumblr.com/post/63249708431/windows-forms-on-japanese-xp
tumblr_filipfracz_id:
  - "63249708431"
  - "63249708431"
categories:
  - Programming
  - Uncategorized
tags:
  - internationalization
  - winforms
  - work
---
Today at work we ran into an interesting issue. Our Windows Forms-based application worked perfectly on the English Windows XP, but it looked weired on the Japanese version. It was quite noticable – size of some UI controls differed by about 2 pixels and the entire layout was out of wack (of course we probably should have been using some sort of layout manager, but that's a different story).

After spending hours debugging this thing we came to realize it was a font problem. WinForms uses Microsoft Sans Serif by default, and its size can be a bit larger on east-Asian systems (I imaginge it's hard to read the pictograms when the font size is small). The solution was simple – all we had to do was to change the font to &#8220;MS Shell Dlg&#8221; which is an alias to a default system font. That fixed all our sizing issues. Important thing to mention is also that we had to type the font name manually in the resource file; for some reason the designer would not let us select the virtual font.

Let's hope that when we switch to WPF all such issues will be taken care of by the layout managers.

**EDIT:** We were actually able to go back to not specifying the font (using the default) and just applied the DPI AutoSizeMode property to the form.