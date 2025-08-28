import streamlit as st
import requests
from deepface import DeepFace
import tempfile
import os
import sys
import time
import praw


st.set_page_config(page_title="Retrackt: Trace and Report Non Consensual Images on Reddit", layout="centered")
st.write("Python version:", sys.version)
st.title("Find out if your photograph has been reposted on Reddit without your consent")

reddit = praw.Reddit(
    client_id="IJ9SJnf2Rlib8p6LnYnO8Q",          
    client_secret="5TFcCxmJSL4owpFtYmTaeDXL4GFwPw",   
    user_agent="RetracktScript by u/jeremiahdoe"  
)

insta_url = st.text_input("Enter Instagram Image URL (direct .jpg/.png preferred):")
insta_username = st.text_input("Enter your Instagram username:")
full_name = st.text_input("Enter your full name:")
uploaded_file = st.file_uploader("Or upload an image", type=["jpg", "jpeg", "png"])
subreddit = st.text_input("Enter subreddit name to scan:", "BeautifulIndianWomen")

def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_file.write(response.content)
            temp_file.close()
            return temp_file.name
    except:
        return None


def get_all_reddit_images(subreddit_name="BeautifulIndianWomen", limit=200):
    images = []

    try:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.new(limit=limit):
            if submission.url.lower().endswith((".jpg", ".jpeg", ".png")):
                images.append({
                    "title": submission.title,
                    "url": submission.url,
                    "permalink": f"https://reddit.com{submission.permalink}"
                })
    except Exception as e:
        st.error(f"Failed to fetch Reddit posts: {e}")
    
    return images


if st.button("Find Matches") and (insta_url or uploaded_file):
    with st.spinner("Matching... this may take a while"):

        # --- Get input image path ---
        if insta_url:
            insta_img_path = download_image(insta_url)
        elif uploaded_file:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(uploaded_file.read())
            temp_file.close()
            insta_img_path = temp_file.name
        else:
            st.error("No image provided")
            st.stop()


        reddit_posts = get_all_reddit_images(subreddit_name=subreddit)

        if not reddit_posts:
            st.warning("No image posts found in the subreddit.")
            st.stop()

        matched = []

        for idx, post in enumerate(reddit_posts):
            try:
                reddit_img_path = download_image(post["url"])
                if not reddit_img_path:
                    continue

                result = DeepFace.verify(insta_img_path, reddit_img_path, enforce_detection=False)

                if result['verified']:
                    matched.append({
                        "reddit_url": post["permalink"],
                        "image_url": post["url"],
                        "distance": result["distance"],
                        "title": post["title"]
                    })

                os.remove(reddit_img_path)

                if (idx + 1) % 50 == 0:
                    st.write(f"Processed {idx + 1} images...")

            except Exception as e:
                continue

        os.remove(insta_img_path)


        if matched:
            matched = sorted(matched, key=lambda x: x["distance"])[:3]
            st.success(f"Found top {len(matched)} matches:")

            for match in matched:
                st.markdown(f"**[{match['title']}]({match['reddit_url']})**")
                st.image(match["image_url"], width=300)
                st.markdown(f"**Similarity Distance**: `{match['distance']:.3f}`")
                st.markdown("---")
        else:
            st.warning("No matches found.")
