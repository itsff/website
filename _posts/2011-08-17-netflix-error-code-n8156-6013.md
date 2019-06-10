---
id: 33
title: Netflix Error Code N8156-6013
date: 2011-08-17T10:38:00+00:00
author: filip
layout: post
guid: http://filipfracz.net.holly.arvixe.com/?p=33
permalink: /2011/08/netflix-error-code-n8156-6013/
tumblr_filipfracz_permalink:
  - http://filipfracz.tumblr.com/post/63249701128/netflix-error-code-n8156-6013
  - http://filipfracz.tumblr.com/post/63249701128/netflix-error-code-n8156-6013
tumblr_filipfracz_id:
  - "63249701128"
  - "63249701128"
categories:
  - Uncategorized
tags:
  - Error
  - Netflix
  - silverlight
---
My wife came across this mysterious &#8220;Netflix Error Code N8156-6013&#8221; today and let me tell you – she was not happy. Netflix player keep complaining about DRM and date (which was correct). It took me a good 20 minutes to find a solution. Credit goes to Chad ([read his post here](http://the-chronicon.blogspot.com/2011/02/netflix-vs-silverlight-4-he-said-she.html "Netflix Error Code N8156-6013")). I'm reposting to give the solution more exposure.

<div>
  <blockquote>
    <p>
      The fix after much research is to delete a Playready config file<span class="Apple-converted-space"> </span><strong><em>mspr.hds</em></strong><span class="Apple-converted-space"> </span>(leftover from the Silverlight 3 version) and allow the Netflix player to re-create the file using Silverlight 4.<br />The file to delete or rename (probably safer; in case something goes wrong just rename it back correctly)<strong></p>

      <p>
        On Windows XP:</strong><br />C:Documents and SettingsAll UsersApplication DataMicrosoftPlayReadymspr.hds<em><br />or</em><br />C:ProgramDataMicrosoftPlayReadymspr.hds<strong></p>

        <p>
          On Windows 7:</strong><br />C:UsersAll UsersApplication DataMicrosoftPlayReadymspr.hds<em><br />or</em><br />C:ProgramDataMicrosoftPlayReady (Thanks Jarin)<strong></p>

          <p>
            On MAC:</strong><br />HD > Library > Application Support > Microsoft > PlayReady > mspr.hds
          </p>

          <p>
            Don't forget to restart your browsers!
          </p></blockquote> </div>

          <div>
            Hopefully this post will save you time. Once again, <a title="Netflix Error Code N8156-6013" href="http://the-chronicon.blogspot.com/2011/02/netflix-vs-silverlight-4-he-said-she.html">credit goes to Chad</a>.
          </div>