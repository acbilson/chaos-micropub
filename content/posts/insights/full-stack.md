+++
category = "technology"
comments = true
date = "2020-10-28"
description = "In which Alex describes his process for full stack development."
draft = true
tags = ["full-stack"]
title = "Full Stack Development"
[featuredImage]
  large = ""
  small = ""
  alt   = ""
+++
I've always been a full-stack developer. My mind works in systems rather than languages, so I've never been compelled to master a single technology slice. Instead, I inhabit the interfaces between technology slices: between the file system and the API server, between the API server and the web frontend services, and between the web frontend services and the web component UI.

My first stack was a PHP backend with vanilla HTML/CSS and a little bit of JavaScript. That was back in my early twenties when Tommy, Matthew and I launched our first business. Since then I've been adding tech to the stack so I have more options to plug into my mental models.

One of my favorite stacks is (insert pic here) a SQL Server 2017 backend with a C# 4.5.2 Framework WebAPI service and a React frontend. I'm well versed in development SQL and can confidently retrieve optimized data for my services. I enjoy wiring my custom SQL to objects in the service so I rarely use an ORM to manage that interface. I get great pleasure transforming the SQL data into a clean JSON API that's ready for my frontend to consume. I retrieve the data from my service via custom JavaScript services and fit the data into organized web components for a pluggable, reactive web experience. Truthfully, this is one of my favorite stacks because it's one I've used the most often, writing several apps with most of these components for Relativity.

In my own time I prefer to pick up tech stacks that a small business might use. Most startups aren't interested in enterprise-level SQL Servers or foundational Microsoft technologies. It's getting the project going with the least overhead that's critical. One of my favorite quick stacks is a SQLLite backend, a Python Flask web service (with werkzeug templates I don't even need a frontend framework at first), maybe use SQLAlchemy to wire these two if I'm in a hurry, then a VueJS frontend.

Levels:

Web Layer
  HTML/CSS/JavaScript / VueJS / ReactJS / AngularJS

Service Layer
Flask / .NET Core WebAPI / Rocket (rustlang)

Persistence Layer
SQLite / MS SQL Server / MySQL (MariaDb)
