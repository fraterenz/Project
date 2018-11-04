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

# A list of internal milestones up until project milestone 2



**Clean the data, how?**
* Create a metric that defines the most relevant pages (article length, article logs, article referred links (clickstreams), ...), according to a certain date, looking at the page date of creation (e.g. World War II is a known conflict but is outdated so discarded).
* Create a list of less relevant pages (these will be the least discussed and least known pages nowadays).



# Questions for TAa


The dataset pages edit history expand to multiple terabytes of text because contains all pages with complete page edit history but we would like to have only the the number of times a page has been edited. Maybe it would be better to scrap the selected wikipedia pages “https://en.wikipedia.org/urlToPage**&action=history**”?
