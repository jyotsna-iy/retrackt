import streamlit as st
import requests
from deepface import DeepFace
import tempfile
import os
import sys

st.write("Python version:", sys.version)
st.set_page_config(page_title="Retrackt: Trace and Report Non Consensual Images on Reddit", layout="centered")

st.title("Find out if your photograph has been reposted on Reddit without your consent")

# 1. Instagram image URL
insta_url = st.text_input("Enter Instagram Image URL (direct .jpg/.png preferred):")

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_file.write(response.content)
            temp_file.close()
            return temp_file.name
    except:
        return None

def get_reddit_images():
    reddit_url = "https://www.reddit.com/r/BeautifulIndianWomen/search.json"
    headers = {'User-agent': 'face-matcher-bot'}
    params = {'q': '', 'restrict_sr': 1, 'limit': 15}
    response = requests.get(reddit_url, headers=headers, params=params)
    results = response.json()
    images = []

    for post in results['data']['children']:
        url = post['data'].get('url_overridden_by_dest') or post['data'].get('url')
        if url and url.endswith((".jpg", ".jpeg", ".png")):
            images.append({
                "title": post['data']['title'],
                "url": url,
                "permalink": f"https://reddit.com{post['data']['permalink']}"
            })
    return images

# Image Matching / Similarity 
if st.button("Find Matches") and (insta_url or uploaded_file):
    with st.spinner("Matching... this may take a few seconds"):

        # 1. Load input image
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

        reddit_posts = get_reddit_images()
        matched = []

        for post in reddit_posts:
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
            except Exception as e:
                continue

        if matched:
            st.success(f"Found {len(matched)} matches:")
            matched = sorted(matched, key=lambda x: x["distance"])
            for match in matched:
                st.markdown(f"**[{match['title']}]({match['reddit_url']})**")
                st.image(match["image_url"], width=300)
                st.markdown(f"**Distance**: `{match['distance']:.3f}`")
                st.markdown("---")
        else:
            st.warning("No matches found.")
