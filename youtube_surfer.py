import webbrowser
import urllib.parse

def search_youtube(query):
    # Encode the query to be URL-friendly
    query_string = urllib.parse.urlencode({"search_query": query})
    
    # Construct the YouTube search URL
    url = "https://www.youtube.com/results?" + query_string
    
    # Open the URL in the default web browser
    webbrowser.open(url)

# # Example usage:
# if __name__ == "__main__":
#     search_term = input("Enter the search term: ")
#     search_youtube(search_term)
