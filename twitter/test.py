import requests

blob_url = "blob:https://twitter.com/3c8d3da8-7699-4f39-a373-5d3fb4a0b888"

output_file = 'downloaded_video.mp4'

try:
    # Send a GET request to the blob URL
    response = requests.get(blob_url, stream=True)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a new file and write the content of the blob to it
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Video downloaded successfully to '{output_file}'")
    else:
        print("Failed to download video")
except Exception as e:
    print(f"Error downloading video: {e}")