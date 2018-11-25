# Biaspedia: Media-driven data

# Abstract


The information covered by the media is often related to an underlying **economical factor**. Let's consider conflicts: the more the money is invested on actions related to them, the more media will inform people. We think that Wikipedia indirectly correlates with this *information bias* since people creating wiki pages may write about such subjects according to the media trend. What if Wikipedia were imbalanced in its coverage of knowledge? What if Wikipedia showcased an unbalanced representation of the world presented by the media? Since Wikipedia aims to capture data driven by non-profit seeking people, we could provide an unbiased source information (data not yet fully covered by the media). Our goal is to provide an *unbiased* source of information by creating a new way to inform people based on Wikipedia, as it represents non-profit method to collect the information. 


# Research questions

* Does current knowledge or media coverage correlate with the most popular Wikipedia pages, reflecting the economical bias? 
* How to define a metric of popularity within different article pages?
* How to provide an unbiased source of information? Would the extrapolation and the presentation of less known wikipedia articles provide an unbiased source of information?
* What are the respective contributions to such popular pages from parts of the world? 


# Dataset

* **Wikipedia pages content**: data size and format: 64.2 G in one single .xml file
* **Wikipedia pages edit history**: pages-meta-history xml files 
* **Wikipedia clickstreams**: https://dumps.wikimedia.org/other/clickstream/readme.html
* **Wikipedia mediacounts**: https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Mediacounts

# Pipeline 

* **filter pages per category** [CLUSTER]
    * civilian attack
    * civil conflict
    * military conflict

* **outlier removal and disambiguations removal** 
    * use keywords (**"war, riot, conflict, protest, revolt, operation, attack, annexation, genocide, insurgency, crisis, confrontation, clash"**) on the article titles to extract from our chosen categories (`civilian attack`, `civil conflict`, `military conflict`)

* **quantify popularity of each page in each category using 4 metrics** 
    * article length
    * number of references and important medias
    * numero of views from API 
    * number of external links [CLUSTER]

* **quantify importance of each page in each category**
We want to see how *important* each page is in each category. As we are solely focusing on *'war'*-related subjects in this pilot phase, we define *page importance* by the number of deaths. Data is obtained either using the page's wikidata is the data exists or acquired through infobox parsing. Relevant information is chosen based on the fields found on [List of infoboxes and fields](https://en.wikipedia.org/wiki/Wikipedia:List_of_infoboxes#Event) 

    * **Infobox important fields to extract**
        * `civilian attack`
            * fatalities
            * location
            * date
        * `civil conflict`
            * place
            * date
            * casualties1
        * `military conflict`
            * place
            * date
            * casualties1 

    * **Extract info for each category in Wikidata**:
        * `civilian attack`
            * location
            * date 
            * fatalities
        * `military conflict`
            * 'number of deaths (P1120)']['amount']
            * 'end time (P582)'
            * 'location (P276)'
        * `civil conflict`
            * 'number of deaths (P1120)']['amount']
            * 'end time (P582)'
            * 'location (P276)'


* **Join tables on the page id or page title**
    * Get table where 1 row = 1 page
        * *1 page contains*
           * id
           * title
           * ref count 
           * references
           * views or numero di visite da API
           * number of external links
           * related info box stuff/wikidata (location, date, deaths)

# A list of internal milestones up until project milestone 3

* Clean the data, how?
* Create a metric that defines the most relevant pages (article length, article logs, article referred links (clickstreams), ...), according to a certain date, looking at the page date of creation (e.g. World War II is a known conflict but is outdated so discarded).

# For milestone 3
* Infer a list of less relevant pages (these will be the least discussed and least known pages nowadays), and 
contrast with "Popular" articles.



# Questions for TAs

* Number of views of a page: 
    * We are not sure if we should take into account the “relevance” of the article by normalizing the views of a page. For instance, if there is a civil conflict in Paris, where 2 civilians are found dead. The page would be more visualized than for instance a page talking about an attack in Stockholm, as the Parisian population is twice the size of Stockholm population. Should we normalize by the population size of the country in conflict? 
    * Another hypothesis could be that the views are not from unique people, meaning that a person can visit multiple times a given page, so the statistics could be a bit biased, no? Maybe by normalizing we can minimize the bias?


