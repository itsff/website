---
id: 24
title: First Windows Phone 7 App
date: 2010-11-11T21:14:00+00:00
author: filip
layout: post
guid: http://filipfracz.net.holly.arvixe.com/?p=24
permalink: /2010/11/first-windows-phone-7-app/
tumblr_filipfracz_permalink:
  - http://filipfracz.tumblr.com/post/63249703786/first-windows-phone-7-app
  - http://filipfracz.tumblr.com/post/63249703786/first-windows-phone-7-app
tumblr_filipfracz_id:
  - "63249703786"
  - "63249703786"
categories:
  - Programming
  - Uncategorized
tags:
  - MoCalc
  - wp7
---
As you undoubtedly heard from my posts on Twitter, I have published my very first Windows Phone 7 app. Yes, you guessed it right – it's a mortgage calculator called [Mo Calc](http://basically.me/Apps/MoCalc).

## Dev Experience

I wanted to see if Microsoft's promise of reusing [existing Silverlight code](http://page/MortgageCalculator.aspx "Mo Calc") on the phone was true. Indeed it was, but mainly for the business logic. The unique space constrains of a phone screen pretty much required a brand new UI. I was glad my old code followed the MVVM pattern – I was able to quickly use databinding and get the new UI of the ground.

I really enjoyed styling the interface in Blend. Microsoft did an awesome job on this front. Visual design makes writing apps much quicker, even quicker than on Android. You don't have to deploy to the device/emulator to see how your UI will look like.

The APIs feel fine as well – every .NET dev will be at home. That said, I must say I personally like the &#8220;intent&#8221; model of Android better that Silverlight's web-like &#8220;navigation&#8221; model. But that's just my personal opinion. I'm still giving WP7 dev experience very high marks.

<img style="border: 0px initial initial" src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-cool.gif" border="0" alt="Cool" />  <img style="border: 0px initial initial" src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-cool.gif" border="0" alt="Cool" /> <img style="border: 0px initial initial" src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-cool.gif" border="0" alt="Cool" />

Below are some [screenshots](http://www.flickr.com/photos/filipandtab/sets/72157625212299115/with/5156716185/ "Screenshots of Mo Calc on Flickr") from version 1.0.0.0 of Mo Calc.

<div>
  <a title="Home screen with multiple mortgages by itsFF, on Flickr" href="http://www.flickr.com/photos/filipandtab/5156716185/"><img src="http://farm5.static.flickr.com/4053/5156716185_de870e7d62_m.jpg" alt="Home screen with multiple mortgages" width="144" height="240" /></a> <a title="Screen for adding or editing mortgages. The estimated payment is auto-updated with each change. by itsFF, on Flickr" href="http://www.flickr.com/photos/filipandtab/5156716109/"><img src="http://farm2.static.flickr.com/1376/5156716109_e450356afa_m.jpg" alt="Screen for adding or editing mortgages. The estimated payment is auto-updated with each change." width="144" height="240" /></a> <a title="Mortgage comparison - graph showing monthly payments by itsFF, on Flickr" href="http://www.flickr.com/photos/filipandtab/5157325024/"><img src="http://farm5.static.flickr.com/4043/5157325024_75b4f10566_m.jpg" alt="Mortgage comparison - graph showing monthly payments" width="144" height="240" /></a>
</div>

<div>
</div>

<div>
</div>

## Marketplace Experience

Unlink Apple, Microsoft has published clear guidelines of what is allowed and what is not. It was nice to be able to read a document outlining all the things that are considered during the certification process. I chose to make my Mo Calc free and make money from ads. Microsoft allows 5 free app submissions.
Publishing Mo Calc through the website was very easy; a typical &#8220;wizard&#8221; experience. I was told the approval may take as long as five days, but my app got into the market just after 18 hours. Nice! 

<img src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-cool.gif" border="0" alt="Cool" />  <img style="border: 0px initial initial" src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-cool.gif" border="0" alt="Cool" /> <img style="border: 0px initial initial" src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-cool.gif" border="0" alt="Cool" />

## The Bad and Ugly

While the quick submission turnaround time was certainly impressive, Microsoft managed to frustrate the heck out of me.

Right after my app made it to the market, I received a confirmation email stating that my marketplace account had been cancelled. Wait, what?
You read it right. The money was refunded to me, and I can no longer log in. Why did this happen? Nobody knows.

I have been calling MS tech support every day since, but was told that it may take more than a week to get my account reinstated. Very, very frustrating!

Meanwhile, my app is available in the marketplace. I have since found a few bugs and issues (ex. the ads are not showing, so I am not making any money) that I would like to fix, but I cannot access my account. Thanks Microsoft. I just hope that no one gives my app negative feedback for the glitches.

I'm really hoping my account gets reinstated soon&#8230;

<img src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-surprised.gif" border="0" alt="Surprised" />  <img style="border: 0px initial initial" src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-yell.gif" border="0" alt="Yell" /> <img src="https://s3.amazonaws.com/basically_me_images/smileys/smiley-cry.gif" border="0" alt="Cry" />