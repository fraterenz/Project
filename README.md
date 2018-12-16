# Biaspedia: Media-driven data

# Notebook
Select notebook **pipeline.ipynb** to view our pipeline and analysis.

# Abstract

**How do we beat top-ranking Wikipedia content?**

We suppose that Wikipedia is facing the common problem as pages in Google. Highly popular articles are popular also because they have a lot of backlinks or pages that are redirected to them. Imagine you're a journalist or a active blogger writing about an article on Afghanistan news. You google and enter the `Afghanistan` article on Wikipedia to get the resources quickly. Entering wikipedia articles through search engines such as Google can be tricky because even if it yields decent amount of content, you will never find an unpopular Wikipedia page. Once you find enough content on Wikipedia, you'll return to your adored search engine. So, why would you keep searching for that unpopular `inexistent` page? 

As a pilot-phase, we focus solely on articles that all have as common subject: `civilian attack`, `civil conflict`, `military conflict`. In other words, we look at such subject-related articles and quantify their popularity and importance using a score with different **metrics** detailed below. 

Our goal is to showcase articles which may be less popular so that you can be informed by facts and topics you may search or need using English Wikipedia. This can help promote less visible articles so that they can be improved, edited, viewed and thus contribute to our knowledge of the on-going events!

Also, for a journalist, it may really be helpful because instead of covering incredibly adverstised topics, they may get the opportunity to be the first to right their own story about an uncovered subject. Their research can improve the article visibility and give more importance to a hidden world. 

We hypothesize that unkown articles are not necessarily unimportant! 

In order to estimate the popularity of the wikipedia articles, we came up with some metrics, stemming from intuition and some good references ([1](https://en.wikipedia.org/wiki/Help:Drawing_attention_to_new_pages#How_do_I_get_others_to_notice_the_page_I_just_created?)) and ([2](https://en.wikipedia.org/wiki/Wikipedia:Pageview_statistics#What_factors_can_increase_a_page's_viewing?)) became good indicators to select our candidates. 

4 characteristics of an article could be used to identify the popularity of an article:
* [x] page references
* [x] page views
* [x] external links
* [x] article length


# Research questions

* How can we develop a metric of popularity to rank Wikipedia pages?
* Does current knowledge or media coverage correlate with the most popular Wikipedia pages? 
* Are popular articles always important? 


# Dataset

* **Wikipedia pages content**: data size and format: 64.2 G in one single .xml file
* **pageview API** to get views

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

         SCORE =  views +  links +  references +  length 
        
        all the features are standardized using [MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler). To be able to measure the influence of each component, they need to be comparable and thus on the same range to compute the popularity score. For this reason, we transform the features by scaling each feature to a range between 0 and 1. We used this standardization approach instead of normalization to maintain the structure of the data, i.e. to preserve the distribution of the features.

# Data distribution
* **Distribution of articles for each keyword**: {war riot conflict protest revolt operation attack annexation genocide insurgency crisis confrontation clash}
* **Distribution of number of references**: follows a power law. The distribution has a heavy-tailed distribution
    * Histogram
    * Log-log plot
    * Boxplot with and without outliers
* **Percentage of references for domains**: 
    * top 3 references are : {books.google.com, www.nytimes.com, www.theguardian.com}
    * top 3 references after analyzing articles (describing conflicts after 1995): {www.reuters.com, www.almasdarnews.com, www.nytimes.com}. Interestingly, the media has changed as the conflicts are more oriented towards the Middle East.

* **Distribution of number of views**: follows a power law. The distribution has a heavy-tailed distribution
    * Histogram
    * Log-log plot
    * Boxplot with and without outliers
* **Distribution of article lengths** : follows a power law. The distribution has a heavy-tailed distribution.
    * Histogram
    * Log-log plot

# End of milestone 3
* [x] Infer a list of less relevant pages (these will be the least discussed and least known pages nowadays), and 
contrast with "Popular" articles.

* [x] Compute popularity metric **external links**

* [x] Contrast references between *popular* and *nonpopular* articles in ongoing events 

* [x] Evaluate metric of popularity through a survey 

# Results of the survey 

<div class="alert alert-block alert-warning">
<font color='#B8860B'>
<b>Note</b>
</font>
<font color='black'>
We want to double check that our score is correlated with what people think. We wrote a survey in order to verify that our metric is accurate. We collected 2088 answers from more than 20 people. The user choices between left, right or 'Skip' in order to indicate the most popular conflict between the 2 proposed conflicts, i.e. it is a binary survey. 

The coverage of the survey is not incredible (12%) because we have more than 17 000 articles that can be used to write the survey, and some are really really unknown. Therefore, we randomly selected only articles that correspond to the middle to the top part of our popularity ranking.

We counted the number of correct answer for each popularity duel and we found out that 94 % of the answers to the questionaire match our popularity score, not bad! 

The metric thus seems to capture the popularity of the article. In this 6% of error, most of the errors seem to come more often from a missclick or a confusion rather than an error in our metric. For instance, two users thought that World War I is less popular than 2009 Jaipur fire or Battle of Adwa, which seems a bit unrealistic. Another group of errors arise from 2 unknown conflicts, like 2008 Bin Salman mosque bombing vs the Battle of Marawi. 
Having established that the metric seems realistic, we continue our investigation by looking at the findings our metric will give: spot important unpopular conflicts!
</font>
</div>


We want to double check that our score is correlated with what people think. We wrote a survey in order to verify that our metric is accurate. We collected 2088 answers from more than 20 people. The user choices between left, right or 'Skip' in order to indicate the most popular conflict between the 2 proposed conflicts, i.e. it is a binary survey. 

The coverage of the survey is not incredible (12%) because we have more than 17 000 articles that can be used to write the survey, and some are really really unknown. Therefore, we randomly selected only articles that correspond to the middle to the top part of our popularity ranking.

We counted the number of correct answer for each popularity duel and we found out that 94 % of the answers to the questionaire match our popularity score, not bad! 

The metric thus seems to capture the popularity of the article. In this 6% of error, most of the errors seem to come more often from a missclick or a confusion rather than an error in our metric. For instance, two users thought that World War I is less popular than 2009 Jaipur fire or Battle of Adwa, which seems a bit unrealistic. Another group of errors arise from 2 unknown conflicts, like 2008 Bin Salman mosque bombing vs the Battle of Marawi. 
Having established that the metric seems realistic, we continue our investigation by looking at the findings our metric will give: spot important unpopular conflicts!


# Questions for TAs

* Number of views of a page: 
    * We are not sure if we should take into account the “relevance” of the article by normalizing the views of a page. For instance, if there is a civil conflict in Paris, where 2 civilians are found dead. The page would be more visualized than for instance a page talking about an attack in Stockholm, as the Parisian population is twice the size of Stockholm population. Should we normalize by the population size of the country in conflict? 
    * Another hypothesis could be that the views are not from unique people, meaning that a person can visit multiple times a given page, so the statistics could be a bit biased, no? Maybe by normalizing we can minimize the bias?


# External libraries
* [wptools wiki](https://github.com/siznax/wptools/wiki) to help us parse the data
* [mwviews](https://github.com/mediawiki-utilities/python-mwviews)
* [WikipediaCitationUsage](https://github.com/epfl-dlab/WikipediaCitationUsage/blob/master/MetaPageQueries.ipynb) to parse references

# Contributions
