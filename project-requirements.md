**Question: Mini Instagram Django REST Server**
Create just the backend REST server for a mini instagram app, where users create albums, add pics to it, tag their albums with topics, & discover other users with similar tastes.

An album is a collection of pictures that users post. On top of each picture, the user can write a caption, change the font color of the caption and position the caption anywhere on top of the image. While rendering on the UI, the caption should be able to be rendered exactly on the saved position and in the saved color by the user.

As a user I want to be able to do the following things -
1) Create as many albums as I want, save it to my outbox, but not publish it yet. Other users can only see albums that I actually published
2) Add as many pics to any of my unpublished albums. For each pic I can add
a caption on top of the pic and position it anywhere on the pic and select
a specific font color
3) Publish albums from my "drafts"
4) Add hashtags to my albums before I publish
5) Discover users similar to my tastes & follow them

Create the django db side, python code with proper entry REST API endpoints for the that the client can call.

For #5, user discovery, assume you are given a db table, where each row contains a user id, similar user's id & similarity score.