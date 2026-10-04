---
title: "SSH ForwardAgent Gotchas"
slug: ssh-forwardagent-gotchas
subtitle: ""
date: 2019-02-05T20:07:00+00:00
draft: false
tags: ["ssh"]
---

So, you’re trying to create an SSH Tunnel to your remote machine to make some gitlab/github clones.

That’s all fine and well until you don’t want to post your password on to the terminal.

First, look at you `~/.ssh/config` file and add the **“ForwardAgent yes”** to that machines ip.

{{< highlight bash >}}
Host 35.241.133.24
  IdentityFile ~/.ssh/id_rsa
  ForwardAgent yes
{{< /highlight >}}

That says to use your local private key as identification when accessing gitlab on your remote’s machine.
Then, just try to check your GitHub/Gitlab connectivity, but first, don’t forget to add you private key to your ssh-agent:

{{< highlight bash >}}
$ ssh-add -K
Identity added: /Users/me/.ssh/id_rsa (/Users/me/.ssh/id_rsa)
$ ssh-add -l
2048 SHA256:vt6nnixlJpupm8H5+cAuIcxy46LAYdYhfo+WL0E /Users/me/.ssh/id_rsa (RSA)
{{< /highlight >}}

Now, inside your machine try to check if you can authenticate on Gitlab/Github

{{< highlight bash >}}
$ ssh -v ubuntu@35.242.133.24
ubuntu@instance-1:~$ ssh-add -l
2048 SHA256:vt6nnixlJpupm8H5+cAuIcxy46LAYdYhfo+WL0E /Users/me/.ssh/id_rsa (RSA)

ubuntu@instance-1:~/load-test$ ssh -T git@github.com
Hi andreffs18! You've successfully authenticated, but GitHub does not provide shell access.
ubuntu@instance-1:~/load-test$ ssh -T git@gitlab.com
Welcome to GitLab, @andreffs18!
{{< /highlight >}}

Now, let’s try to clone our project

{{< highlight bash >}}
ubuntu@instance-1:~/load-test$ git pull origin master
Username for 'https://gitlab.com': ^C
{{< /highlight >}}

What?! I don’t want to put my credentials! Isn’t the **ForwardAgent** for this?

Okay, let’s look at our remotes:

{{< highlight bash >}}
ubuntu@instance-1:~/load-test$ git remote -v
origin    https://gitlab.com/andreffs18/load-test.git (fetch)
origin    https://gitlab.com/andreffs18/load-test.git (push)
{{< /highlight >}}

⚠️  If you work with HTTPs urls, it will always ask for your username/password!

If you're correctly using SSH when cloning / setting remotes.
Then make sure you have a ssh-agent to remember your password.
That way, you'll only enter your passphrase once by terminal session.

If it is still too annoying, then simply set a ssh-key without passphrase.

Just change it:

{{< highlight bash >}}
$ git remote set-url origin git@gitlab.com:andreffs18/load-test.git
{{< /highlight>}}


And now, on your remote machine you should be able to pull everything from your repo:
{{< highlight bash >}}
ubuntu@instance-1:~/load-test$ git pull origin master
debug1: client_input_channel_open: ctype auth-agent@openssh.com rchan 2 win 65536 max 16384
debug1: channel 1: new [authentication agent connection]
debug1: confirm auth-agent@openssh.com
From gitlab.com:andreffs18/load-test
 * branch            master     -> FETCH_HEAD
debug1: channel 1: FORCE input drain
Updating 16f56eb..f661b58
Fast-forward
 jmeter/test.jmx                        | 344 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 python/__init__.py                     |   2 +-
 python/uwsgi.ini                       |   7 ++
 elixir/config/config.exs               |   1 +
 elixir/config/dev.exs                  |   3 +-
 go/cmd/main.go                         |   2 +-
 6 files changed, 355 insertions(+), 4 deletions(-)
 create mode 100644 jmeter/test.jmx
 create mode 100644 go/cmd/main.go

{{< /highlight>}}

That’s it 👋.
