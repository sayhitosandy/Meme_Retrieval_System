## Efficient Meme Retrieval System
A weighted model that retrieves a set of memes from database based on user query.

#### Problem Statement
A meme is an image, gif or video (usually funny) which has some text content on it.

**Basic problem:** When the user enters a search query, a set of memes is retrieved from a database, where each element of the database comprises of an image and some text.

#### Dataset & Collection
* We scraped more than `14,000` posts from `3` popular public Instagram meme profiles using an open source software, `instaloader`.
* Each post crawled resulted in a `jpg` and a corresponding `json` containing caption, hashtags, and other metadata of the post.
* To capture a vast diversity of memes, all content posted on the page since inception has been scraped.

#### Gold Standard Dataset
* Made a set of `10` queries on the `9gag` website and picked `10` relevant results for each query.
* Created `csv` file with columns: Query, Captions
* Use this as Gold Standard to calculate Precision, Recall, F1, MAP score.

#### Challenges
* Absence of perfect correlation between caption and user query.
* Information contained in the meme image element itself is hard to retrieve.

#### OCR in Weighted Model
* To improve the results, we used `Pytesseract` to read the text from the meme images. 
* We created one `json` for each image file containing this text, and then calculated `tf-idf` scores. 
* We created a combined weighted model for the `tf-idf` scores of the actual text-based and the image-extracted text, by taking a `weighted average` of the tf-idf scores.

#### Results and Conclusion
Our improved model performed significantly better in terms of recall and marginally better in terms of Precision than the model without using OCR. Hence, we can conclude that combining image-based features with the text-based features had an appreciable improvement on our IR system.

