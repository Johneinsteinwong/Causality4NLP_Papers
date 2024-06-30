import re
import requests
import os

# Define the path to the README.md file
file_path = 'README.md'

# Read the contents of the README.md file
with open(file_path, 'r') as file:
    readme_contents = file.read()

# Regular expression to find titles and their corresponding PDF links
pattern = re.compile(r'\*\*(.*?)\*\*.*?\[pdf\]\((http[s]?://[^\)]+\.pdf)\)')
matches = pattern.findall(readme_contents)

# Directory to save the downloaded PDFs
download_dir = 'data/'
os.makedirs(download_dir, exist_ok=True)

# Function to sanitize filenames
def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '(', ')')).rstrip()

# Function to download a PDF file
def download_pdf(url, filename, download_dir):
    local_filename = os.path.join(download_dir, filename)
    headers = {'Accept': 'application/pdf'}
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# Download all PDF files with sanitized filenames
for title, link in matches:
    sanitized_title = sanitize_filename(title) + '.pdf'
    print(f'Downloading {link} as {sanitized_title}...')
    try:
        download_pdf(link, sanitized_title, download_dir)
    except Exception as e:
        print(e)


print('All PDFs have been downloaded.')