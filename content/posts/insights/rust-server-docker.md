+++
aliases = ["/posts/rust-server-docker/"]
category = "technology"
comments = true
date = "2020-06-24"
description = "In which Alex shares his first foray using Rocket with Docker."
tags = ["rustlang", "docker"]
title = "Rocket Server in Docker"
[featuredImage]
  alt = "Photo by SpaceX on UnSplash"
  large = "https://images.unsplash.com/photo-1517976547714-720226b864c1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
  small = "https://images.unsplash.com/photo-1517976547714-720226b864c1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
+++
{{<photoref "SpaceX" "https://unsplash.com/@spacex" >}}

I began learning Rust in late 2019 because of it's popularity on StackOverflow. When I realized that the language exposed the internals of programming languages while being easier than my foray into Assembly, I was hooked.

I fell in love with Docker using my SPR Consulting Windows machine. I missed the simplicity of Linux and loved how I could destroy the entire environment when I finished working in my Docker container. To get this server going, it made perfect sense to use Docker to encapsulate all the dependencies.

If you've done any Rust development, however, you've noticed how the dependency process is painfully slow (Though it may be [overused dependencies](https://blog.kodewerx.org/2020/06/the-rust-compiler-isnt-slow-we-are.html)). I wanted to add all the dependencies for a basic server into my docker image so that I wouldn't need to wait for all of them to download every time I spun up a docker container. So I began to hack away.

The first step is to get a basic Dockerfile working. Since I'm building for a Debian box, I used the Buster distro:

{{< highlight dockerfile >}}
FROM rust:buster

RUN apt-get update && apt-get upgrade -y
RUN apt-get install vim git -y

ENTRYPOINT ["tail", "-f", "/dev/null"]
{{< / highlight >}}

For a new Dockerfile I always update the image and install my favorite text editor, Vim. I set the entrypoint to hang so I can jump into and out of the image to run commands.

I attempted to follow the steps without updating to the nightly Rust build in hopes the image was already configured this way out-of-the-box but alas, it was not to be. So I added the following to my Dockerfile to shift over to Rust nightly (thanks to [Rocket - Getting Started](https://rocket.rs/v0.4/guide/getting-started/)).

{{< highlight dockerfile >}}
RUN rustup default nightly
RUN rustup override set nightly
RUN rustup update && cargo update
{{< / highlight >}}

To my surprise, this fails! Turns out it requires a Cargo.toml manifest, even though I haven't created my project yet. So I generated a new project for a default setup.

{{< highlight dockerfile >}}
RUN cd /home && cargo new default_cargo --bin
{{< / highlight >}}

Another error?! Looks like Cargo wants to know the user, but Docker hasn't set the variable. It's the little things that can turn folks off to Docker, but I'm persistent. With a little searching I update the line to include the required variable:

{{< highlight dockerfile >}}
RUN cd /home && export USER=root && cargo new default_cargo --bin
{{< / highlight >}}

Now we're getting all the Rust nightly dependencies. That'll save us some time!

We can continue following the quick start by adding the Rocket dependency to our Cargo.toml manifest. I also needed to run `cargo build` so Cargo would install the dependencies, which meant updating `main.rs` to the getting started example. I just copy-pasted the example from my local drive to Docker:

{{< highlight dockerfile >}}
RUN echo "rocket = \"0.4.5\"" >> /home/default_cargo/Cargo.toml
COPY ./default.rs /home/default_cargo/src/main.rs
RUN cargo build
{{< / highlight >}}

Success! Now we have all the dependencies from Rust nightly **and** every dependency for the Rocket package. I spin up the docker container only to discover that Rocket defaults to run on localhost. If you've worked with Docker before, you know that you'll have problems escaping the container with localhost. One more update to change the running host to 0.0.0.0 (Rocket.toml example taken from [Rocket config](https://rocket.rs/v0.4/guide/configuration/)):

{{< highlight dockerfile >}}
COPY ./Rocket.toml /home/default_cargo/Rocket.toml
{{< / highlight >}}

Now it's all set. Build the image, which took five minutes on my laptop, then spin up the Docker image - don't forget to expose port 8000 - and viola, you have a default Rocket server at http://localhost:8000 on your local machine! Blazing fast too, since all the dependencies are already downloaded in your custom Docker image.

Here's the full Dockerfile:

{{< highlight dockerfile >}}
FROM rust:buster

RUN apt-get update && apt-get upgrade -y
RUN apt-get install vim git -y

# create a default cargo project to complete the setup
FROM rust:buster

RUN apt-get update && apt-get upgrade -y
RUN apt-get install vim git -y

# create a default cargo project to complete the setup
RUN cd /home && export USER=root && cargo new default_cargo --bin
WORKDIR /home/default_cargo

# configs for using rocket.rs
RUN rustup default nightly
RUN rustup override set nightly

# update rust packages
RUN rustup update && cargo update

# add rocket dependency
RUN echo "rocket = \"0.4.5\"" >> /home/default_cargo/Cargo.toml

# copy default Rocket server (replaces existing main.rs)
COPY ./default.rs /home/default_cargo/src/main.rs

# build the Rocket server dependencies
RUN cargo build

# copy Rocket default settings (req to set Docker-compliant host)
COPY ./Rocket.toml /home/default_cargo/Rocket.toml

ENTRYPOINT ["tail", "-f", "/dev/null"]
{{< / highlight >}}

Another afternoon well spent.
