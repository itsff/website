---
id: 21
title: 'Async Patterns with C# – Handling Requests'
date: 2010-07-12T09:23:00+00:00
author: filip
layout: post
guid: http://filipfracz.net.holly.arvixe.com/?p=21
permalink: /2010/07/async-patterns-with-c-handling-requests/
tumblr_filipfracz_permalink:
  - http://filipfracz.tumblr.com/post/63249704702/async-patterns-with-c-handling-requests
  - http://filipfracz.tumblr.com/post/63249704702/async-patterns-with-c-handling-requests
tumblr_filipfracz_id:
  - "63249704702"
  - "63249704702"
categories:
  - Programming
  - Uncategorized
tags:
  - async
  - C
  - csharp
  - pattern
  - programming
---
This is a continuation of my earlier blog post regarding asynchronous operations in .NET. We are now going to discuss the various ways of issuing and receiving results from asynchronous requests.

There are three main ways of issuing an asynchronous request and later receiving the result. They are described in the sections below.

## Callback methods

The pattern of specifying a callback method goes way, way back. And it is still being widely used today. The idea is simple:

  * Call a method that starts an asynchronous operation
      * Pass in a delegate to the function you want called when the operation completes
      * Optionally specify user data
  * The specified callback methods gets called asynchronously. The arguments passed to it usually contain:
      * The result of async operation
      * Error indication (Exception object or error code)
      * User data

Depending on the needs the callback method could be a simple delegate or an interface.

### Delegates

The approach of passing delegates is convenient, because one could easily take advantage of closures/lambdas. That way objects in scope become available to the “callback” method.

A main disadvantage would be that it is difficult to “cancel” the asynchronous operation. There also is no “identity” to the operation (unless we consider the pair `<delegate, user data>`).

Although there are no technical reasons, in practice only 1 delegate gets passed as a callback.

### Interfaces

When viewed simply as “collections of methods,” interfaces could be considered a special case of “callbacks” or, as Java folks like to call them, listeners. In Java it is convenient to pass interfaces to receive callbacks, because Java allows for creation of inline anonymous classes. This is unfortunately not the case for C#, which is why the “request object” is a more interesting pattern for the .NET crowd. More on that in the next section.

Since interfaces represent concrete objects, they do have identities. This could allow for “cancelling” async requests by passing the same observer instance that was used when making the request.

## Request objects

This is a very common pattern that most coders are familiar with. The premise is simple:

  * Create an object representing the asynchronous operation
  * Optionally set properties on the request object, for instance store some user data.
  * Hookup the event handler (or handlers).
  * Call a method starting the asynchronous action.
  * Receive the event with results. Extract the information from event arguments.

The main advantage of using the request object is that the object itself is responsible for emitting the events signaling the completion/failure of the async operation. In other words, the “sender” passed to the event handling function is the request. Users can store custom data with the request and easily get to it from the handler. This could be accomplished via composition (for example by having a Tag property), or by inheritance (by allowing the users to extend the request object).
Depending on the needs, the request object can have multiple events. For instance, one for signaling completion, and one errors.
The request object could also optionally provide a “Cancel” method that would stop the asynchronous action, or at least prevent the events from being fired.

Once can classify the request objects depending on how they are created, and who actually starts the asynchronous operation. Several main categories are briefly described below.

### Self-created, self-submitting

The user can create the request object by calling its constructor directly. The method starting the async action is off the request object itself.
This variation of the pattern is convenient as it could allow for extending the request object through inheritance.



### Factory-created, self-submitting

The user creates the request object by calling a factory method. Typically the factory is some kind of main “API” object that contains multiple operations. Once created, the request object is self-sufficient and can be “submitted” using its own method.
Since the request is constructed by a factory, it usually means that extending the request object is not allowed.



### Self-created, factory-submitted

The user is able to create the request object by calling its constructor. This could potentially allow for inheritance scenarios.
Asynchronous action is started by calling a method on another object, which usually ends up being the main “API” object.



## Hybrid – BeginInvoke/EndInvoke

The pattern of BeginInvoke/EndInvoke that is build into the .NET framework can be seen as a hybrid of callback method and request object. The usage is a follows:

  * Call a “BeginInvoke” method to start an async operation
      * The method accepts a callback delegate and user data.
      * The return of the method is an IAsyncResult instance that the caller needs to hold on to
  * IAsyncResult could be used to wait until async operation completes and to cancel it.
  * When the callback function gets called
      * Call “EndInvoke” and pass it the IAsyncResult instance acquired from the “BeginInvoke”
      * The “EndResult” will return the “outcome” of the async operation.