# Snippets (server)

Snippets is my take on a "light bookmarking" app in the spirit of Pocket or Google Keep. I found that neither of those apps worked exactly the way I wanted them, so I decided to just build my own as a way to learn VueJS. It focuses less on note-taking and image-snipping and more on just being a temporary bookmarking solution--ideal for keeping a link you want to come back to but don't want to commit to with a permanent bookmark in your browser (e.g. a video you're in the middle of watching or a Reddit thread you want to come back to later).

The server code is built with Django + Django Rest Framework, and is deployed on Heroku with a PostgreSQL DB.

You can view the repo for the client-side code [here](https://github.com/gargrave/snippets-client).

# Demo

You can see a dev/demo version [here](https://gargrave-snippets-dev.netlify.com). You can sign up for a new account, and everything should be working (there is no "forgot password" functionality, though, so remember your password). Bear in mind that the server is running a free Heroku instance, so don't be frightened if there are performance issues.
