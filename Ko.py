import requests
import pdfkit

# Set the base URL for the webpage
base_url = "https://novelfull.com/my-abilities-come-with-special-effects/chapter-"

# Set the start and end chapter numbers
start_chapter = 29
end_chapter = 100

# Set the output PDF filename
output_filename = "chapter_pages.pdf"

# Send HTTP requests to each chapter and save the HTML content
chapter_content = []
for chapter in range(start_chapter, end_chapter + 1):
    url = base_url + str(chapter) + ".html"
    response = requests.get(url)
    chapter_content.append(response.text)

# Convert the HTML content to a single PDF
pdfkit.from_string("\n".join(chapter_content), output_filename)