# Biaspedia: Media-driven data

# Abstract


To investigate our hypothesis, we contrast **popular** articles vs **non-popular** articles on Wikipedia. As a pilot-phase, we focus solely on articles that all have as common subject: `civilian attack`, `civil conflict`, `military conflict`. In other words, we look at such subject-related articles and quantify their popularity and importance using a score with different **metrics** detailed below. Our objective is to showcase articles which are well known *(‘Syria war, ...’)* in comparison to articles which are less heard-of, less *popular* so that journalists,  aspiring writers or people can be informed by other facts. It can also help a journalist if he is having a writer’s block or has run out of stories to write about. To determine the *popularity* of an article, we define a metric of popularity based on 4 metrics: 

* page views
* page references
* article length
* external links

Also, it should be noted that certain conflicts *(Rohingya, ...)*  which were unknown a couple of years ago, have become of increasing interest. Future steps include: 
* finding a way to show this increasing in interest over the years if possible
* Highlight media included in the references of popular vs unpopular articles: *Which top domains are mentioned?  What kind of media are present?*



# Research questions

* Does current knowledge or media coverage correlate with the most popular Wikipedia pages? 
* How to provide an unbiased source of information? Would the extrapolation and the presentation of less known wikipedia articles provide an unbiased source of information?
* What are the respective contributions to such popular pages from parts of the world? (to be discussed)


# Dataset

* **Wikipedia pages content**: data size and format: 64.2 G in one single .xml file
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

* **attribute a score to each page based on the popularity metrics**

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


* **Join popularity metric tables on the page id**
    * Get table where 1 row = 1 page
        * *1 page contains*
           * id
           * title
           * ref count 
           * views
           * number of external links
* **Join final popularity metric table with each category table on the page id**
    * Get `military conflict` table where 1 row = 1 page
        * *1 page contains*
            * id
            * title
            * ref count 
            * views
            * number of external links
            * related info box stuff/wikidata (location, date, deaths)
     * Get `civil conflict` table where 1 row = 1 page
        * *1 page contains*
            * id
            * title
            * ref count 
            * views
            * number of external links
            * related info box stuff/wikidata (location, date, deaths)
            
     * Get `civilian attack` table where 1 row = 1 page
         * *1 page contains*
            * id
            * title
            * ref count 
            * views
            * number of external links
            * related info box stuff/wikidata (location, date, deaths)

* **Define a popularity score for each page**
    We use 4 features to define the popularity score of a page.

    We define the popularity score of an article as:

         SCORE = w1 * views + w2 * links + w3 * references + w4 * length 
        
        w1, w2, w3 and w4 are arbitrary weigths that normalize the features.

    We have noticed that the features references,length and views seem to follow a power law. Therefore, we use the median to construct the weights associated to them.

# Data distribution
* **Distribution of articles for each keyword**: {war riot conflict protest revolt operation attack annexation genocide insurgency crisis confrontation clash}
* **Distribution of number of references**: follows a power law. The distribution has a heavy-tailed distribution
    * Histogram
    * Log-log plot
    * Boxplot with and without outliers
* **Percentage of references for domains**: top 3 references are : {books.google.com, www.nytimes.com, www.theguardian.com}
* **Distribution of number of views**: follows a power law. The distribution has a heavy-tailed distribution
    * Histogram
    * Log-log plot
    * Boxplot with and without outliers
* **Distribution of article lengths** : follows a power law. The distribution has a heavy-tailed distribution.
    * Histogram
    * Log-log plot

# For milestone 3
* Infer a list of less relevant pages (these will be the least discussed and least known pages nowadays), and 
contrast with "Popular" articles.



# Questions for TAs

* Number of views of a page: 
    * We are not sure if we should take into account the “relevance” of the article by normalizing the views of a page. For instance, if there is a civil conflict in Paris, where 2 civilians are found dead. The page would be more visualized than for instance a page talking about an attack in Stockholm, as the Parisian population is twice the size of Stockholm population. Should we normalize by the population size of the country in conflict? 
    * Another hypothesis could be that the views are not from unique people, meaning that a person can visit multiple times a given page, so the statistics could be a bit biased, no? Maybe by normalizing we can minimize the bias?

# External libraries
* [wptools wiki](https://github.com/siznax/wptools/wiki) to help us parse the data
* [mwviews](https://github.com/mediawiki-utilities/python-mwviews)

