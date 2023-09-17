# Article_Classification_Task

A news article scraping and classifying project written on Python

The news source is chosen as https://lurer.com

The scraper.py program uses BeautifulSoup library for pulling data out of HTML files.
First, using CSS tags it scraps the links of different news category pages.
Then iterates through each category page and scraps the links to all the articles. Then with a delay of 2 second for each category, it scraps articles storing its text. Finally it converts the obtained text into a .csv file ( <article_text, category> ).

The article_classifier.py imports the .csv file, does some preprocessing (lowering, stopword remowal, those are let down in the currennt version of the code).
Replaces missing elements with empty strings.
Then divides the data into training, validating, and testing parts (using the sklearn ibrary). Next it vectorizes the data with TF-IDF vectorizer.
Initializes the hyperparameters and defines the classifier.

Here the SGDClassifier is used. 
Then we perform a grid search for the best hyperparameter and train the classifier on it.

And at last, we calculate the accuracy of the classifier with the precision/recall/f1-scores

Some of the best scores that I recieved:

![image_2023-09-17_204037528](https://github.com/AlexOrdukhanyan/Article_Classification_Task/assets/114373618/ed3a4f72-7897-4084-a86c-360ce9678141)

![Screenshot 2023-09-17 194051](https://github.com/AlexOrdukhanyan/Article_Classification_Task/assets/114373618/9d9f8573-759d-411c-9373-0352b73e71b9)


Useful Materials And Sources:

https://towardsdatascience.com/scraping-1000s-of-news-articles-using-10-simple-steps-d57636a49755

https://realpython.com/beautiful-soup-web-scraper-python/

https://towardsdatascience.com/multi-class-text-classification-model-comparison-and-selection-5eb066197568

https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f

