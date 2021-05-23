---
title: "Postgres Is Now Running"
slug: postgres-is-now-running
subtitle: ""
date: 2017-09-20T10:53:00+00:00
draft: false
tags: ["postgres"]
toc: false
plotly: false
---

My Macbook has OSX Mavericks installed and sometimes it crashes for no reason, breaking my local postgres server.
After restarting and running again ```"$ brew services postgres"```, Postgres becomes _yellow_ and I end up spending sometime looking confused and frustrated.

Looking at the logs you can get a sense of whats happening:

{{< highlight bash>}}
$ tail -f /usr/local/var/postgres/server.log
FATAL:  lock file "postmaster.pid" already exists
{{< /highlight>}}

Simply removing the lock file that Postgres generates solves this issue:

{{< highlight bash>}}
$ rm -f /usr/local/var/postgres/postmaster.pid
{{< /highlight>}}


> If you can't find your `postmaster.pid`, just run the following snippet on your terminal:
>
> ```$ find ~ -name postmaster.pid\* ```


Now a simple restart puts the server back online!

{{< highlight bash>}}
$ brew services start postgresql
{{< /highlight >}}


### Why do we need to do this?

If your computer crashes and Postgres it's abruptly stopped, its cleanup procedures don't run so the `postmaster.pid` file is kept intact on your local hard drive.

Also, whenever we start postgres (`pg_ctl start`) the program checks if there is an already running server by looking for an existing `postmaster.pid`.

You can read more about this issue on [Postgres mailing list](https://www.postgresql.org/message-id/5039AF7B.2090607%40hogranch.com)
