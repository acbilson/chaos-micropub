+++
aliases = ["/posts/angular-architecture/"]
category = "technology"
comments = true
date = "2021-06-01"
description = "In which Alex presents his latest Angular project."
tags = ["angular", "architecture", "diagrams", "database", "project"]
title = "Angular Architecture"
[featuredImage]
  alt = "green trellis over brick"
  large = "https://bn02pap001files.storage.live.com/y4mFm61UCAEIWdJfkMIUTk_iWpevDghkeZddHRo26K01zUgxA47gEgyeS8d_gqPhjjyQMRSwS4H9t_PbLMu6a2mhdOUXC9HRLryZBarw3mpPK1F4h7Qxo2rhh1Wtbsemj1VnF5mbytTDY0NZABbpTqCNFWBMDgg5BDwriqmcPHigqigAwu35cAybCMaa0WzMB8a?width=1024&height=768&cropmode=none"
  small = "https://bn02pap001files.storage.live.com/y4mFm61UCAEIWdJfkMIUTk_iWpevDghkeZddHRo26K01zUgxA47gEgyeS8d_gqPhjjyQMRSwS4H9t_PbLMu6a2mhdOUXC9HRLryZBarw3mpPK1F4h7Qxo2rhh1Wtbsemj1VnF5mbytTDY0NZABbpTqCNFWBMDgg5BDwriqmcPHigqigAwu35cAybCMaa0WzMB8a?width=256&height=192&cropmode=none"
+++
It's a strange and unfortunate pattern that my day-to-day work rarely makes it into my writing. This article rectifies that pattern by exploring a large project I recently completed.

One of my strengths is the design of systems and architecture. I don't claim to always make the best choice, but I am more likely than my peers to make a thoughtful, comprehensive review of our available designs, weigh the pros/cons, and diagram an architecture that makes the most business sense.

On my first project at $COMPANY, I was given the privilege to work with one of the firm's partners to build a new product offering for our customers. The product had been meticulously designed in a series of Excel sheets, but we needed to move the project to our website.

# Phase 1: Requirements

First, I put on my business analyst hat and developed the project requirements. I learned enough about the project domain to ask coherent questions about the user's process. I crafted a seven-page requirements document and estimated twenty-two-week delivery in a statement of work. I hosted a medium-sized prototype in AWS S3.

It was a solid beginning to the project, but I made some mistakes. I misread how much of the project's design and content were uncertain and pushed too often for answers in the first two months. I selected a waterfall project methodology because of the pressure for a concrete deadline when I should have advocated for Agile.

The project didn't stabilize enough to craft a suitable architecture until three months in.

# Phase 2: Architecture

The first architecture to gel was the database. I began the project with fake data to gain early UI feedback, but it was clear that this must be a data-driven design. With the expert advice of a resident DBA, we designed normalized table schemas that have required little modification. Here's a snapshot:

{{< image "/posts/data/angular_architecture/database_diagram.svg" "diagram" >}}

> shout-out to the awesome work done by the developers of [PlantUML](https://github.com/plantuml/plantuml), without whom I would not have software to build comprehensive and beautiful UML diagrams such as these!

Unlike the database, the Angular architecture underwent a significant re-write halfway through the project. The re-write was partially occasioned by changing requirements and partially by a series of conversations with senior developers. Especially as a new hire, it was crucial that I not only deliver business value but do so in a way that is comprehensible to my developer peers. I'm pleased by the result of our dialogue and the stability that's come from the re-write.

{{< image "/posts/data/angular_architecture/component_diagram.svg" "diagram" >}}

> This might come as a surprise, but I put these diagrams together before most of the code was implemented. These images aren't documentation for the sake of this post but artifacts that were crucial to my design process. Like the carpenter's adage to "measure twice, cut once," I find the effort spent diagramming an architecture saves days of individual development churn and focuses dialogue and questions in teams.

# Phase 3: Refinement

Even with mid-project changes, the original requirements were completed by the target deadline! As the UI matured and we received a little user feedback, however, it became clear that our customers would be better served by delaying the release until we refined the user experience.

This phase was when our team hit its stride. The looming deadline was replaced with a semi-Agile approach. Daily meetings and regular status emails reduced the stress on our communication and limited surprises. With a foundation to build upon, changing requirements no longer resulted in crash estimates for multi-week sub-projects but were usually implemented in less than two day's development time.

I'm proud of what I've achieved. Wanna see?

![summary-chart](/posts/data/angular_architecture/summary_chart.png)
![detail-table](/posts/data/angular_architecture/detail_table.png)
