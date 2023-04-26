# Deployment

There are two parts to deployment: the front-end (client) and the back-end (server).

## Client

Deployment of the client is very simple: simply serve the appropriate files
(`index.html`, `main.js`, `style.css`, `favicon.ico`, `bg.jpg`)
on your HTTP (web) server of choice. You can simply serve the entire project
directory if you choose. Make sure to change the WebSockets
location to wherever you have your server set up (see below). In short, you can
do this with a single command:
```
sed -i -e 's,ws://localhost:8001/,wss://example.com/ws/,' main.js
```

Note however the `wss://` in the replacement link. It is assumed you have SSL
set up on your server site; if not, simply replace with `ws://` instead. Also,
note the endpoint that the server can be reached at (here it's `/ws/`).

## Server

Deployment of the server is a bit trickier. Take note of the port that `app.py`
is working on (default 8001). Create an endpoint (such as `/ws/`) where
`app.py` is accessible. I am proxying the request using NGINX; here is my
configuration:
```
location /ws/ {
    proxy_pass http://localhost:8001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

Note that if you have the client and server in a separate directory or are
serving them with different servers/services, `app.py` requires `GamePB.py`,
`draw.py`, and the `assets/` folder to function.

## Licensing of this file (`INSTALL.md`)

Copyright 2023 Rodrigo Becerril Ferreyra

Copying and distribution of this file, with or without modification, are permitted in any medium without royalty, provided the copyright notice and this notice are preserved. This file is offered as-is, without any warranty.
