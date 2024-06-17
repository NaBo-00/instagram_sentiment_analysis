# Instagram Comments Scraper and Sentiment Analysis

## Disclaimer

| :warning: | Use at your own risk, the author of this project is not liable for your actions :exclamation: |
| --- | --- |
| :warning: | This project was made for research and educational purposes **ONLY**:exclamation: |
| :warning: | This project violates Instagrams's User Agreement, and because of this, Instagram may (and will) temporarily or permanently ban your account. We are not responsible for your account being banned:exclamation: |

## Description

This project provides a set of functions for scraping Instagram post's comments, processing them, and performing sentiment analysis using a pre-trained model. The results are stored in a database and visualized using matplotlib.

## Features

- **Log In to Instagram:** Automated login to Instagram using Selenium.
- **Profile Data Extraction:** Scrape profile data including the number of posts, followers, following, and profile header.
- **Comment Extraction:** Extract comments from specific Instagram posts.
- **Sentiment Analysis:** Perform sentiment analysis on extracted comments using a pre-trained RoBERTa model.
- **Data Storage:** Store the extracted and processed data into a SQLite database.
- **Data Visualization:** Visualize profile information and sentiment analysis results.

## Dependencies

The project requires the following Python libraries:

- selenium
- pandas
- transformers
- scipy
- sqlalchemy
- matplotlib

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/NaBo-00/instagram-sentiment
    ```

2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Download the ChromeDriver executable:** 
    - Make sure to match the version of your Chrome browser.
    - Place the `chromedriver.exe` in the project directory or specify its path in the script.

## Usage

### Running the Script

1. **Set your Instagram credentials and target profiles in the script:**
    ```python
    user = "<yourUsername>"
    password = "<yourPassword>"
    ```

2. **Specify the target profiles and posts:**
    ```python
    profile_fcb = "fcbayern"
    profile_bvb = "bvb09"
    post_fcb_rbl = "p/Cv27PvZINwY/"
    post_fcb_svd = "p/Cy8odemolGY/"
    post_bvb_new = "p/Cy23k-fIEk6/"
    post_bvb_fch = "p/CwqbIwhIUtf/"
    ```

3. **Run the script:**
    ```sh
    python main.py
    ```

### Functions

- **`log_in(chrome_driver, usr, pw)`**: Logs into Instagram.
- **`read_profile(chrome_driver, profile_name)`**: Reads the profile data of the specified user.
- **`read_comments(chrome_driver, post_path, total_comments)`**: Extracts comments from the specified post.
- **`polarity_scores_predefined_model(comment_text, comment_author)`**: Computes sentiment scores for a comment.
- **`process_comments(comments_df)`**: Processes a DataFrame of comments and computes sentiment scores.
- **`combine_comment_sentiment(comments_df, sentiment_df)`**: Combines comment and sentiment data.
- **`create_combined_data(chrome_driver, post_path, table_name, number_of_comments)`**: Extracts comments, processes sentiments, and stores them in a database.
- **`count_sentiments(df)`**: Counts sentiment categories in a DataFrame.
- **`store_df_into_db(data_df, table_name)`**: Stores a DataFrame into a SQLite database.
- **`visualize_profiles(combined_data_df)`**: Visualizes profile information.
- **`visualize_sentiment(combined_df_fcb_rbl, combined_df_fcb_svd, combined_df_bvb_fch, combined_df_bvb_new)`**: Visualizes sentiment analysis results.

## Database

The project uses SQLite to store the scraped and processed data. The database file is named `data.db` and is located in the project directory.

## Visualization

The project provides functions to visualize both the profile data and the sentiment analysis results. The visualizations are created using matplotlib and include bar charts for various metrics and sentiments.

## Example

An example script demonstrating the usage of the provided functions is included in the main script. It logs into Instagram, reads profile data, extracts comments, performs sentiment analysis, stores the data in a database, and visualizes the results.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Legal :warning:
This script is in no way affiliated with, authorized, maintained, sponsored or endorsed by Instagram or any of its affiliates or subsidiaries. Developed for research and educational purposes ONLY - Use at your own risk.

This project violates Instagram's Terms of Service (TOS), and because of this, Instagram may (and will) temporarily or permanently ban your account. I'm not responsible for your account being banned or any actions you perform.



---

Made by NaBo-00 | Copyright &copy; NaBo-00 | All Rights Reserved

<div><img alt="NaBo-00-logo.png" src="NaBo-00-logo.png" width="100" height="60" /></div>
