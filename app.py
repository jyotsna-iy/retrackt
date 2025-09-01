import time
start_time = time.time()
print(f"[DEBUG] Starting app load at {time.strftime('%H:%M:%S')}")

import streamlit as st
print(f"[DEBUG] Streamlit imported in {time.time() - start_time:.2f}s")

import requests
print(f"[DEBUG] Requests imported in {time.time() - start_time:.2f}s")

# DeepFace will be imported lazily when needed
print(f"[DEBUG] Skipping DeepFace import (will load when needed)")

import tempfile
import os
import sys
from dotenv import load_dotenv
print(f"[DEBUG] Standard libraries imported in {time.time() - start_time:.2f}s")

# Load environment variables
load_dotenv()
print(f"[DEBUG] Environment variables loaded")

praw_start = time.time()
import praw
print(f"[DEBUG] PRAW imported in {time.time() - praw_start:.2f}s (total: {time.time() - start_time:.2f}s)")


print(f"[DEBUG] Setting up Streamlit UI...")
ui_start = time.time()
st.set_page_config(page_title="Retrackt: Trace and Report Non Consensual Images on Reddit", layout="centered")
st.write("Python version:", sys.version)
st.title("Find out if your photograph has been reposted on Reddit without your consent")
print(f"[DEBUG] Streamlit UI setup in {time.time() - ui_start:.2f}s (total: {time.time() - start_time:.2f}s)")

# Reddit connection will be initialized when needed
print(f"[DEBUG] Skipping Reddit connection (will connect when needed)")

print(f"[DEBUG] App fully loaded in {time.time() - start_time:.2f}s")
print("=" * 50)

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


def get_all_reddit_images(subreddit_name="BeautifulIndianWomen2", limit=1000):
    images = []

    try:
        # Initialize Reddit connection lazily
        reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET") 
        reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "Retrackt by u/jeremiahdoe")
        
        if not reddit_client_id or not reddit_client_secret:
            st.error("Reddit API credentials not found. Please check your .env file.")
            return []
            
        reddit = praw.Reddit(
            client_id=reddit_client_id,          
            client_secret=reddit_client_secret,   
            user_agent=reddit_user_agent  
        )
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
    # Create containers for dynamic updates
    status_container = st.container()
    progress_container = st.container()
    
    with status_container:
        status_text = st.empty()
        progress_bar = st.empty()
        details_text = st.empty()
        cancel_button = st.empty()
        
    # Track processing state
    start_time = time.time()
    
    try:
        # Import DeepFace lazily when actually needed
        status_text.info("🔄 Loading face recognition model (this may take a moment on first run)...")
        try:
            from deepface import DeepFace
            status_text.success("✅ Face recognition model loaded successfully!")
            time.sleep(1)  # Brief pause to show success message
        except Exception as e:
            status_text.error(f"❌ Failed to load face recognition model: {e}")
            st.stop()

        # Prepare the reference image
        status_text.info("📸 Preparing your reference image...")
        if insta_url:
            insta_img_path = download_image(insta_url)
            if not insta_img_path:
                status_text.error("❌ Failed to download image from Instagram URL")
                st.stop()
        elif uploaded_file:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(uploaded_file.read())
            temp_file.close()
            insta_img_path = temp_file.name
        else:
            status_text.error("❌ No image provided")
            st.stop()

        # Fetch Reddit posts
        status_text.info(f"🔍 Fetching image posts from r/{subreddit}...")
        reddit_posts = get_all_reddit_images(subreddit_name=subreddit)

        if not reddit_posts:
            status_text.warning("⚠️ No image posts found in the subreddit.")
            st.stop()

        total_posts = len(reddit_posts)
        status_text.success(f"✅ Found {total_posts} image posts to analyze")
        
        # Initialize progress tracking
        matched = []
        processed = 0
        failed_downloads = 0
        
        # Show initial progress bar
        progress_bar.progress(0)
        details_text.text(f"Starting analysis of {total_posts} images...")

        # Process each Reddit post
        for idx, post in enumerate(reddit_posts):
            try:
                # Update progress
                progress = (idx + 1) / total_posts
                progress_bar.progress(progress)
                
                # Calculate speed and ETA
                elapsed_time = time.time() - start_time
                if idx > 0:
                    avg_time_per_image = elapsed_time / idx
                    remaining_images = total_posts - idx
                    eta_seconds = avg_time_per_image * remaining_images
                    eta_text = f"ETA: {int(eta_seconds//60)}m {int(eta_seconds%60)}s"
                    speed_text = f"Speed: {60/avg_time_per_image:.1f} images/min"
                else:
                    eta_text = "Calculating ETA..."
                    speed_text = "Calculating speed..."
                
                # Update status
                status_text.info(f"🔄 Analyzing image {idx + 1}/{total_posts} | {len(matched)} matches found")
                details_text.text(f"📊 {speed_text} | {eta_text} | ❌ {failed_downloads} failed downloads")
                
                # Download Reddit image
                reddit_img_path = download_image(post["url"])
                if not reddit_img_path:
                    failed_downloads += 1
                    continue

                # Perform face verification
                result = DeepFace.verify(insta_img_path, reddit_img_path, enforce_detection=False)

                if result['verified']:
                    matched.append({
                        "reddit_url": post["permalink"],
                        "image_url": post["url"],
                        "distance": result["distance"],
                        "title": post["title"]
                    })
                    # Brief celebration for new match
                    status_text.success(f"🎯 MATCH FOUND! ({len(matched)} total) | Processing {idx + 1}/{total_posts}")

                # Clean up downloaded image
                os.remove(reddit_img_path)
                processed += 1

            except Exception as e:
                continue

        # Final progress update
        progress_bar.progress(1.0)
        total_time = time.time() - start_time
        status_text.success(f"✅ Analysis complete! Processed {processed}/{total_posts} images in {int(total_time//60)}m {int(total_time%60)}s")
        details_text.text(f"📊 Final stats: {len(matched)} matches found | {failed_downloads} failed downloads")

        # Clean up reference image
        os.remove(insta_img_path)
        
        # Display results
        if matched:
            matched = sorted(matched, key=lambda x: x["distance"])[:3]
            st.success(f"🎯 Found top {len(matched)} matches:")

            for match in matched:
                st.markdown(f"**[{match['title']}]({match['reddit_url']})**")
                st.image(match["image_url"], width=300)
                st.markdown(f"**Similarity Distance**: `{match['distance']:.3f}`")
                st.markdown("---")
        else:
            st.info("No matches found. Your image appears to be unique on this subreddit! 🎉")
        
    except Exception as e:
        status_text.error(f"❌ An error occurred: {e}")
        if 'insta_img_path' in locals():
            try:
                os.remove(insta_img_path)
            except:
                pass
