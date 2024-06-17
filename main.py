from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


def log_in(chrome_driver, usr, pw):
    chrome_driver.get("https://www.instagram.com")

    # Specify the timeout of the driver
    timeout = 5

    # Handle Alert - allow only neccessary cookies
    cookies = WebDriverWait(chrome_driver, timeout).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]'))).click()

    # Login to IG by identifying the necessary input fields
    # Specify username and password input field
    username = WebDriverWait(chrome_driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
    password = WebDriverWait(chrome_driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))

    # Make sure that the input fields are empty
    username.clear()
    password.clear()

    # Enter username and password
    username.send_keys(usr)
    password.send_keys(pw)
    time.sleep(5)

    # Click LogIn Button
    loginBtn = WebDriverWait(chrome_driver, timeout).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="loginForm"]/div/div[3]/button'))).click()
    time.sleep(5)

    # Return response - Login
    print("[Info] - Successful Login")

    # Handle Alert - not now (credentials)
    WebDriverWait(chrome_driver, 5)
    notNowCredentials = WebDriverWait(chrome_driver, timeout).until(EC.presence_of_element_located(
        (By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div'))).click()

    # Handle Alert - not now (notifications)
    WebDriverWait(chrome_driver, 5)
    notNowNotification = WebDriverWait(chrome_driver, timeout).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'))).click()

def read_profile(chrome_driver, profile_name):
    # Switch to profile
    chrome_driver.get('https://www.instagram.com/' + profile_name)
    time.sleep(5)

    # Identify User Information
    numberPosts_str = chrome_driver.find_element(
        by=By.XPATH, value="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span").text
    numberFollowers_str = chrome_driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span').text
    numberFollowing_str = chrome_driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span').text
    profile_header = chrome_driver.find_element(
        by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]').text

    # Remove commas and convert to integers
    numberPosts = float(numberPosts_str.replace(',', '.'))
    numberFollowers = float(numberFollowers_str.replace('Mio.', '').replace(',', '.'))
    numberFollowing = float(numberFollowing_str.replace(',', ''))

    # Create a dictionary with the user information
    user_info = {
        "Profile Name": profile_name,
        "Number of Posts (k)": numberPosts,
        "Number of Followers (Mio.)": numberFollowers,
        "Number of Following": numberFollowing,
        "Profile Header": profile_header,
    }

    # Convert the dictionary to a pandas DataFrame
    profile_info = pd.DataFrame([user_info])

    # Display the DataFrame
    return profile_info

def read_comments(chrome_driver, post_path, total_comments):
    # Switch to post
    chrome_driver.get('https://www.instagram.com/' + post_path)
    time.sleep(2)

    # Wait for the comments section to load
    comments_section = WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located(
        (By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div")))

    # Scroll through the comments until 1000 comments are collected
    comments = []

    numberScrolls = total_comments // 15
    countScroll = 0
    print("[Info] - Total Number of Scrolls: " + str(numberScrolls))

    for i in range(numberScrolls):
        # Idedntify the comment list dialog box
        dialog = WebDriverWait(chrome_driver, 10).until(lambda d: d.find_element(
            by=By.XPATH, value='/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]'))

        time.sleep(1)
        # Execute scroll
        chrome_driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].scrollHeight;',
            dialog)
        print("[Info] - Iteration of Scrolls: " + str(countScroll + 1) + "/" + str(numberScrolls))
        countScroll += 1

    for i in range(1, total_comments):
        try:

            check_gif = chrome_driver.find_element(by=By.XPATH,
                value="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[" + str(i)
                      + "]/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/span").text

            if check_gif == "You may need to allow third party cookies to view this GIF.":
                continue

            current_comment_author = chrome_driver.find_element(by=By.XPATH,
                value="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[" + str(i)
                      + "]/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/span[1]/span").text
            current_comment_content = chrome_driver.find_element(by=By.XPATH,
                value="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[" + str(i)
                      + "]/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/span").text
            comments.append({"Comment Author": current_comment_author, "Comment Content": current_comment_content})
        except:
                continue

    # Create a DataFrame from the collected comments
    comment_df = pd.DataFrame(comments)

    # Display the DataFrame
    return comment_df

def polarity_scores_predefined_model(comment_text, comment_author):
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    encoded_text = tokenizer(comment_text, return_tensors="pt")
    output = model(**encoded_text)
    sentiment_scores = output[0][0].detach().numpy()
    sentiment_scores = softmax(sentiment_scores)

    # Determine the maximum sentiment score and its corresponding category
    max_score_index = sentiment_scores.argmax()
    sentiment_categories = ["negative", "neutral", "positive"]
    sentiment_category = sentiment_categories[max_score_index]

    sentiment_comment_scores = {
        "Comment Author": comment_author,
        "roberta_neg": sentiment_scores[0],
        "roberta_neu": sentiment_scores[1],
        "roberta_pos": sentiment_scores[2],
        "sentiment": sentiment_category
    }

    return sentiment_comment_scores

def process_comments(comments_df):
    res_model = {}
    for i, row in comments_df.iterrows():
        comment_content = row["Comment Content"]
        comment_author = row["Comment Author"]
        res_model[i] = polarity_scores_predefined_model(comment_content, comment_author)

    sentiment_comment_score_model = pd.DataFrame(res_model).T

    return sentiment_comment_score_model

def combine_comment_sentiment(comments_df, sentiment_df):
    combined_comments_sentiment = comments_df.merge(sentiment_df, on="Comment Author")

    return combined_comments_sentiment

def create_combined_data(chrome_driver, post_path, table_name, number_of_comments):
    comments_df = read_comments(chrome_driver=chrome_driver, post_path=post_path, total_comments=number_of_comments)
    sentiment_df = process_comments(comments_df)
    combined_df = combine_comment_sentiment(comments_df, sentiment_df)
    combined_df = combined_df.drop_duplicates(subset=["Comment Author", "Comment Content"])
    store_df_into_db(combined_df, table_name)
    return combined_df

# Count sentiment categories for each dataframe
def count_sentiments(df):
    return df['sentiment'].value_counts()

def store_df_into_db(data_df, table_name):
    db_file = "data.db"

    # Create a database engine using SQLAlchemy
    engine = create_engine(f"sqlite:///{db_file}")

    # Save the data to the specified table in the database
    data_df.to_sql(table_name, engine, if_exists='replace', index=False)

def visualize_profiles(combined_data_df):
    combined_data_df = combined_data_df.iloc[:,:4]
    # Create a 1x3 grid of subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # 1 row, 3 columns
    color = ['red', 'yellow']
    #legend_labels = combined_data_df.iloc[:, 0].tolist()

    # Loop through the subplots
    for i, col in enumerate(combined_data_df.columns[1:]):
        ax = axes[i]
        combined_data_df.plot(x="Profile Name", y=col, kind="bar", ax=ax, color=color)
        ax.set_title(col)
        # Set the legend to an empty string to remove it
        ax.legend('')

    # Adjust layout and show the plots
    plt.tight_layout()
    plt.show()

def visualize_sentiment(combined_df_fcb_rbl, combined_df_fcb_svd, combined_df_bvb_fch, combined_df_bvb_new):
    # Create a colormap for the sentiments
    colors = {'neutral': 'blue', 'positive': 'green', 'negative': 'red'}
    default_color = 'gray'  # Default color for unknown sentiments
    # Count sentiments for individual dataframes
    sentiments_fcb_rbl = count_sentiments(combined_df_fcb_rbl)
    sentiments_fcb_svd = count_sentiments(combined_df_fcb_svd)
    sentiments_bvb_fch = count_sentiments(combined_df_bvb_fch)
    sentiments_bvb_new = count_sentiments(combined_df_bvb_new)

    # Create bar charts
    fig, axes = plt.subplots(2, 2, figsize=(15, 8))

    # Bar charts for individual dataframes
    sentiments_dataframes = [sentiments_fcb_rbl, sentiments_fcb_svd, sentiments_bvb_fch, sentiments_bvb_new]
    titles = ["FCB vs RBL", "FCB vs SVD", "BVB vs FCH", "BVB vs NEW"]

    for ax, sentiments, title in zip(axes.flat, sentiments_dataframes, titles):
        # Convert sentiment labels to lowercase before accessing colors and use a default color
        ax = sentiments.plot(kind='bar', ax=ax, color=[colors.get(s.lower(), default_color) for s in sentiments.index],
                             legend=False)
        ax.set_title(title)
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")

        # Annotate each bar with the count
        for p in ax.patches:
            ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center')

        # Add total number of sentiments as text next to the title
        total_sentiments = sentiments.sum()
        ax.set_title(f"{title}\nTotal Sentiments: {total_sentiments}")

    # Adjust layout and show the plots
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    user = "<yourUsername>"
    password = "<yourPassword>"
    profile_fcb = "fcbayern"
    profile_bvb = "bvb09"
    post_fcb_rbl = "p/Cv27PvZINwY/"
    post_fcb_svd = "p/Cy8odemolGY/"
    post_bvb_new = "p/Cy23k-fIEk6/"
    post_bvb_fch = "p/CwqbIwhIUtf/"

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    chrome_driver_path = Service("chromedriver.exe")
    myDriver = webdriver.Chrome(service=chrome_driver_path, options=options)

    log_in(chrome_driver=myDriver, usr=user, pw=password)

    # Profile Info - FCB
    fcb_info = read_profile(chrome_driver=myDriver, profile_name=profile_fcb)
    # Profile Info - BVB
    bvb_info = read_profile(chrome_driver=myDriver, profile_name=profile_bvb)
    # Combine profile info
    combined_profile_info = pd.concat([fcb_info, bvb_info])
    store_df_into_db(combined_profile_info, "Profile Info")

    pd.set_option('display.max_columns', None)
    # FCB vs RBL
    combined_fcb_rbl = create_combined_data(myDriver, post_fcb_rbl, "FCBvsRBL", 750)
    print("Combined Data for FCB vs RBL:")
    print(combined_fcb_rbl.shape)

    # FCB vs SVD
    combined_fcb_svd = create_combined_data(myDriver, post_fcb_svd, "FCBvsSVD", 750)
    print("Combined Data for FCB vs SVD:")
    print(combined_fcb_svd.shape)

    # BVB vs FCH
    combined_bvb_fch = create_combined_data(myDriver, post_bvb_fch, "BVBvsFCH", 750)
    print("Combined Data for BVB vs FCH:")
    print(combined_bvb_fch.shape)

    # BVB vs NEW
    combined_bvb_new = create_combined_data(myDriver, post_bvb_new, "BVBvsNEW", 750)
    print("Combined Data for BVB vs NEW:")
    print(combined_bvb_new.shape)

    myDriver.close()

    # Visualization
    visualize_profiles(combined_profile_info)
    visualize_sentiment(combined_fcb_rbl, combined_fcb_svd, combined_bvb_fch, combined_bvb_new)





