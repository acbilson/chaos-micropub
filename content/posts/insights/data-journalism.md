+++
aliases = ["/posts/data-journalism/"]
category = "technology"
comments = true
date = "2020-11-05"
description = "In which Alex combines two amazing discoveries in data journalism"
tags = ["journalism","visualization","datasette"]
title = "Visualizing COVID Deaths"
toc = true
[featuredImage]
  alt   = "Photo by Mayron on Unsplash"
  large = "https://images.unsplash.com/photo-1544813545-4827b64fcacb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
  small = "https://images.unsplash.com/photo-1544813545-4827b64fcacb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
+++
{{< raw >}}
<style>

img.tall-chart {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}

</style>
{{< / raw >}}

{{<photoref "Mayron Oliviera" "https://unsplash.com/@m4yron" >}}
Did you know that [datasette](https://github.com/simonw/datasette) is a mature tool to display and inspect sqlite databases via your browser?

And did you know that [Open Data Inception](https://opendatainception.io/) collects **thousands** of data sets published across the globe?

Let's see what we can do with this information. We're going to use datasette, [Vega](https://vega.github.io/vega/), and a subset of open source data published by the Cook County Medical Examiner [COVID-19 Related Deaths](https://datacatalog.cookcountyil.gov/Public-Safety/Medical-Examiner-Case-Archive-COVID-19-Related-Dea/3trz-enys) to grasp how COVID-19 has affected Cook County, Illinois.

## First Thoughts

I chose to visualize COVID because I sometimes forget people are dying, but there are dozens of other interesting projects just waiting for us to discover. Here's a paper published by the City of Evanston to inspire you and I - [2020 Adopted Budget](https://data.cityofevanston.org/stories/s/tu52-urjb).

Before we begin, it's worth noting that the tool Cook County uses to house this data, [Socrata](https://dev.socrata.com/), (by [Tyler Technology](https://www.tylertech.com/Platform-Technologies.html)), has its own visualization technology. If you don't want to get technical, you can do your own data examination in Socrata [right here](https://datacatalog.cookcountyil.gov/d/3trz-enys/visualization).

## Data Setup

I've never had an easier setup than datasette. There's not even steps per-se; just look at this shell script. All you'll need is a version of Python 3 to use it.

{{< highlight sh >}}
#!/bin/sh

# create virtual environment
python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install requirements
pip3 install datasette
pip3 install socrata2sql

# install datasette plugins
datasette install datasette-vega

# deactivate virtual environment
deactivate
{{< / highlight >}}

## Data Acquisition

Remember that I mentioned the data is hosted by Socrata? Well, Socrata hosts a Web API! But you don't need to read their API documentation; thanks to Andrew Chavez' work we can use his [socrata2sql](https://github.com/DallasMorningNews/socrata2sql) tool. Here's the entire command to get our data set (don't forget to activate your virtual environment first).

{{< highlight sh >}}
socrata2sql insert datacatalog.cookcountyil.gov 3trz-enys
{{< / highlight >}}

This will generate a sqlite table with the name of the data source. We just gave socrata2sql the host and the dataset id and it handles the rest.

## Data Visualization

Last step (already? I know!), let's host the datasette website. Again, it's a one-liner (and you still need your virtual environment activated):

{{< highlight sh >}}
datasette serve medical_examiner_case_archive__covid19_related_deaths.sqlite
{{< / highlight >}}

Now let's do some analysis.

## Deaths by Age

First, I wanted to know the age span of COVID-related deaths. I filtered out ages with fewer than 25 deaths to remove data outliers, but it's worth noting that deaths span from age 12-108 (and one infant).

![deaths-by-age](/posts/data/covid/cook_covid_deaths_by_age.svg)

Cook county fits international COVID death patterns in that the majority of deaths are among those older than 50.

Here's the SQL query:

{{< highlight sql >}}
select
  age,
  COUNT(*) as 'count'
from
  medical_examiner_case_archive__covid19_related_deaths
group by
  age
having
  COUNT(*) >= 25
{{< / highlight >}}

## Deaths by Month and Age

Let's get a little more sophisticated. What if we bucketed all COVID-related deaths by age, then filled the buckets by month? I've removed the young and old outliers to fit the graph and flipped it over for better display on phones.

{{< image "/posts/data/covid/cook_covid_deaths_group_age_month_all.svg" "tall-chart" >}}

The first and second months of the pandemic saw the highest number of deaths among those over 50, but their numbers taperred off by June, which corresponds to the beginning of lockdown procedures. Deaths in the months after June appear to have leveled off.

Let's drill down a little further by removing early months from the results.

{{< image "/posts/data/covid/cook_covid_deaths_group_age_month_since_july.svg" "tall-chart" >}}

Sure enough, the past three months have leveled off. More concerning, however, is that the current rise in COVID cases may also indicate a rise in deaths among those over 50. There are a few ages which already have five or more deaths in November, but this data only has the first four days in November. It's not a good sign that some ages have as many reported deaths in the first four days of November as the entire month of October.

And the SQL query:

{{< highlight sql >}}
select
  age,
  COUNT(*) as 'count',
  strftime('%m-%Y', death_date) as 'month'
from
  medical_examiner_case_archive__covid19_related_deaths
group by
  month,
  age
having
  COUNT(*) >= 5
  and month >= '07-2020'
  and age between 50 and 100
{{< / highlight >}}

## Deaths by City and Month

One more. What if we reviewed all the towns in Cook county, bucketed by month?

If you ran that query yourself, you'd notice that Chicago dwarfs all the others. So I removed Chicago and ended up with:

![death-group-city](/posts/data/covid/cook_covid_deaths_group_city_month.svg)

Two insights stand out.

First, Cicero, Niles, and Wheeling have significantly higher deaths than other towns (besides Chicago). Do they have a higher elderly population? Go pull census information and send me your analysis.

Second, Cicero has a concerning rise in deaths. While most cities have reduced deaths over time, October was the worst month for Cicero. Why is that?

I did observe that many towns have no data after June. It's likely these towns are reporting their numbers independent of the Cook County medical examiner's office, and not that there have been zero deaths.

And the SQL query:

{{< highlight sql >}}
select
  COUNT(*) as 'count',
  strftime('%m-%Y', death_date) as 'month',
  residence_city
from
  medical_examiner_case_archive__covid19_related_deaths
where
  residence_city not in ('Chicago', 'CHICAGO', '')
group by
  residence_city,
  month
having
  COUNT(*) >= 5
  and month >= '06-2020'
{{< / highlight >}}

## Acknowledgements

Thanks to [Tom MacWright](https://macwright.com/2020/10/01/recently.html) for the datasette reference, to the datasette creator, [Simon Willison](https://simonwillison.net/), for using the Open Data Inception Project in your [datasette demonstration](https://www.youtube.com/watch?v=pTr1uLQTJNE), and to [Andrew Chavez](https://achavez.io/) for the socrata2sql tool!

## Caveats

I've copied these notices from the COVID-19 source data. In case you don't follow the links, I want to be sure these are visible.

{{< raw >}}
<blockquote>
This filtered view contains information about COVID-19 related deaths that occurred in Cook County that were under the Medical Examiner’s jurisdiction.This view was created by looking for "covid" in any of these fields: Primary Cause, Primary Cause Line A, Primary Cause Line B, Primary Cause Line C, or Secondary Cause.<br /> <br /> Not all deaths that occur in Cook County are reported to the Medical Examiner or fall under the jurisdiction of the Medical Examiner. The Medical Examiner’s Office determines cause and manner of death for those cases that fall under its jurisdiction. Cause of death describes the reason the person died. This dataset includes information from deaths starting in August 2014 to the present, with information updated daily.</blockquote>
{{< / raw >}}
