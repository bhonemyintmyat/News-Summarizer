My final project for CS50P is a Command-Line Interface (CLI) application whose purpose is to scrape the update news from Al Jazeera website, uses Google's Gemini AI to summarize the news articles into ‌a short, straightforward and concise bullet points, and generates a cleanly formatted, downloadable PDF file. 
I built this tool to solve the problem of information overload. Many people neither have time nor have interest to scroll throught the newsfeed and they are more interested in news that are straightforward and clear. In this project, a user can simply run the project, choose a category, and get a highly readable, downloadable PDF. You can use the CLI to input the number for the category you want to explore for three times at maximum. Only integer numbers are accepted. 

## Features

* **Live Web Scraping:** Makes use of libraries like `requests` and `BeautifulSoup4` to scrape the most recent article categories and links directly from the live web by traversing through the HTML DOM tree.
* **AI Summarization:** Leverages the `google-genai` SDK to analyze and summarize the complete article text. In particular, the AI is instructed to strip all biases and generate the most important, unbiased bullet points.
* **PDF Output:** Dynamically generates a PDF using `fpdf2`. Automatically creates a professional-looking document with bolded headings, properly formatted bullet points, and a professional font.
* **Friendly Command Line Interface:** Uses a command line interface (CLI) to allow you to get your news simply by inputting the corresponding integer number. Uses the `tabulate` library to display the scraped data elegantly in a tabulated form.
* **Graceful Error Handling:** Implements exponential backoff and retries API server overload errors (503 error codes). Prevents a crash of the entire code during execution when such an error occurs.
* **No news for Today!:** In case there is no news available for a certain category on a certain day, then the program will output an informative message saying "❌ No news for Today! Try other categories 🙏".

## Project Structure

To help navigate this repository, here is a brief overview of the core files included in this project:

* `project.py`: This is the main engine of the application. It contains the CLI loop, the `BeautifulSoup` scraping logic, the Gemini AI API integration, and the PDF generation code.
* `test_project.py`: This file contains a comprehensive suite of automated tests. It utilizes the `pytest` framework alongside the `monkeypatch` fixture to safely test the program's logic without sending unnecessary requests to live servers.
* `requirements.txt`: A simple text file detailing the exact third-party Python libraries (and their dependencies) required to run this code successfully.
* `README.md`: The detailed documentation file you are currently reading.

## Installation

To run this project on your local machine, you will need Python installed. 

1. Clone this repository to your local machine.
2. Install the required third-party libraries using pip:
```bash
   pip install -r requirements.txt
```
3. Set up your Google Gemini API Key as an environment variable:
```
    export GEMINI_API_KEY="your_api_key_here"
```

## How To Use It

1. Run project.py in the terminal
2. The table built by tabulate function will appear as below

```
    +------+-------------------------------------------------------------------------+
    |   No | Categories                                                              |
    +======+=========================================================================+
    |    1 | Africa: https://aljazeera.com/africa/                                   |
    +------+-------------------------------------------------------------------------+
    |    2 | Asia: https://aljazeera.com/asia/                                       |
    +------+-------------------------------------------------------------------------+
    |    3 | US & Canada: https://aljazeera.com/us-canada/                           |
    +------+-------------------------------------------------------------------------+
    |    4 | Latin America: https://aljazeera.com/latin-america/                     |
    +------+-------------------------------------------------------------------------+
    |    5 | Europe: https://aljazeera.com/europe/                                   |
    +------+-------------------------------------------------------------------------+
    |    6 | Asia Pacific: https://aljazeera.com/asia-pacific/                       |
    +------+-------------------------------------------------------------------------+
    |    7 | Middle East: https://aljazeera.com/middle-east/                         |
    +------+-------------------------------------------------------------------------+
    |    8 | Explained: https://aljazeera.com/tag/explainer/                         |
    +------+-------------------------------------------------------------------------+
    |    9 | Opinion: https://aljazeera.com/opinion/                                 |
    +------+-------------------------------------------------------------------------+
    |   10 | Sport: https://aljazeera.com/sports/                                    |
    +------+-------------------------------------------------------------------------+
    |   11 | Features: https://aljazeera.com/features/                               |
    +------+-------------------------------------------------------------------------+
    |   12 | Economy: https://aljazeera.com/economy/                                 |
    +------+-------------------------------------------------------------------------+
    |   13 | Human Rights: https://aljazeera.com/tag/human-rights/                   |
    +------+-------------------------------------------------------------------------+
    |   14 | Climate Crisis: https://aljazeera.com/climate-crisis                    |
    +------+-------------------------------------------------------------------------+
    |   15 | Investigations: https://aljazeera.com/investigations/                   |
    +------+-------------------------------------------------------------------------+
    |   16 | Interactives: https://aljazeera.com/interactives/                       |
    +------+-------------------------------------------------------------------------+
    |   17 | In Pictures: https://aljazeera.com/gallery/                             |
    +------+-------------------------------------------------------------------------+
    |   18 | Science & Technology: https://aljazeera.com/tag/science-and-technology/ |
    +------+-------------------------------------------------------------------------+
    Enter the number you want to see: 
```
3. If 18 for Science & Technology is inputted, the terminal will show the processing status and finished status.
    📰 Processing Article 1...
    📰 Processing Article 2...
    📰 Processing Article 3...
    ✅ Success! Open Your Daily News.pdf to see the result.
4. Finally, open the newly generated PDF file in your local directory and enjoy reading your concise news digest!

## Constraints

1. **Strict Valid Input**: Only accept positive integers between 1 and 18 are accepted. Other data types (strings, floats) or out-of-bounds numbers will be rejected.
2. **Attempts**: You have 3 attempts to try and if you still don't input correctly, you will get a "Bye" and the system will exit.
3. **API Dependency**: The Gemini AI results and API limits may vary based on Google's server load and your available API tokens.
4. **Internet Requirement**: Internet connection must be stable to scrape live data from website and connect it to Gemini AI.

# Design Choices

Some decisions had to be made in designing this application that would enable its stability, efficiency, and proper formatting. Some of the difficulties encountered during coding include:

**The "Smart Quotes" PDF Crash**: In the case of standard PDF fonts (Latin-1 encoding by default in fpdf2), the curly "smart quotes" produced by some AI-powered writing assistants cannot be processed directly by the PDF. When trying to create the PDF for the first time, this issue resulted in a failure in the compiling phase of the process. To tackle this problem, I have created a data sanitizer that uses the replace("‘", "'") function.
**No news for Today**: It may very well be that there’s not any news to download yet for a specific topic. Downloading an empty list and passing it on to the Gemini AI would therefore mean wasting both API requests and time of the user who’s waiting for something. I dealt with this scenario by first verifying whether the scraped list actually holds some news in it.
**Testing User Input**: To properly and ethically test my functions using pytest, I had to utilize the monkeypatch fixture which allowed me to simulate a user typing on the keyboard for the CLI inputs, and it let me create fake HTML response objects to test the network calls. By mocking the network, I ensured my test suite could run instantly and repeatedly without actually hitting live servers, preventing IP bans and guaranteeing tests would pass even without Wi-Fi.

# Future Updates

In the future, I plan to expand this project by adding multiple news sources beyond Al Jazeera, allowing users to compare headlines across different platforms. I also aim to implement an automated email feature so the generated PDF digest can be sent directly to a user's inbox whenvever he needed, fully automating the daily news gathering process. 