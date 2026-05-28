import requests
from fpdf import FPDF, XPos, YPos
from tabulate import tabulate
from bs4 import BeautifulSoup
from datetime import date
import sys
from google import genai
import time
client = genai.Client(api_key="your_api_key_here")
AGENT = {"User-Agent": "your_user_agent"}

def main():
    headers = ["No", "Categories"]
    main_cat = []
    table_data = start(main_cat)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    clean_url = (user(table_data))
    update = (get_news(clean_url))
    content = get_content(update)
    ai_sum = (gemini(content))
    pdf = create_pdf(ai_sum)

def start(main_cat):
    url = "https://www.aljazeera.com/"
    response = requests.get(url, headers = AGENT)
    soup = BeautifulSoup(response.text, "html.parser")
    menu_items = soup.find_all("li", class_="menu__item--aje")

    for item in menu_items:
        # Go one layer deeper to find the actual link tag
        link_tag = item.find("a")
        # Always check if the tag exists to prevent errors!
        if link_tag:
            url = link_tag.get('href')
            name = link_tag.get_text(strip=True)
            if f"{name}: aljazeera.com{url}" not in main_cat and name != "Video":
                main_cat.append(f"{name}: https://aljazeera.com{url}")
            else:
                continue
    new_cat = list(dict.fromkeys(main_cat))
    table_data = [[i, h] for i, h in enumerate((new_cat)[1:19], 1)]
    return table_data

    
def user(table_data):
    max_attempts = 3
    while max_attempts > 0:
        try:
            user_input = int(input("Enter the number you want to see: "))
            if 1 <= user_input <= len(table_data):
                raw_string = str(table_data[user_input - 1])
                pieces = raw_string.split(": ") 
                clean_url = pieces[1].strip(" ]'")
                return clean_url
            else:
                raise ValueError()
        except ValueError:
            max_attempts -= 1
            if max_attempts > 0:
                continue
            else:
                sys.exit("Bye 👋😊")
        
    
def get_news(clean_url):
    news_list = []
    d = date.today()
    res = f"/{d.year}/{d.month}/{d.day}/"
    update = requests.get(clean_url, headers = AGENT)
    bsoj = BeautifulSoup(update.text, "html.parser")
    headline_cards = bsoj.find_all("h2", class_="article-card__title")
    for card in headline_cards:
        link_tag = card.find("a")
        if not link_tag:
            link_tag=card.find_parent("a")
        if link_tag:
            article_url = link_tag.get("href")
            
            # check if today's date string is in the URL
            if article_url and res in article_url:
                title = card.get_text(strip=True)
                news_list.append(f"https://www.aljazeera.com{article_url}\n")
            else:
                # It's an older story, skip it
                continue
    if len(news_list) >= 1:
        return news_list
    else:
        sys.exit("❌ No news for Today! Try other categories 🙏")

def get_content(update):
    single_paragraph = []
    for link in update:
        content_link = requests.get(link.strip(), headers = AGENT)
        content = BeautifulSoup(content_link.text, "html.parser")
        body_container = content.find("div", class_="wysiwyg wysiwyg--all-content")
        title_tag = content.find("h1")
        if body_container and title_tag:
    
    #Search for all <p> tags ONLY inside that specific container
            paragraphs = body_container.find_all("p")
            text_list = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            single_article = " ".join(text_list)
            single_paragraph.append(single_article)
    return(single_paragraph)

def gemini(content):
    summary = []
    
    for index, article_text in enumerate(content, 1):
        print(f"📰 Processing Article {index}...")
        
        # 1. The Refined Prompt (Adding Title and Strict Output Formatting)
        my_prompt = f"""You are a highly efficient news editor. 
                Please read the following article text and provide:
                1. A concise, engaging title for the news.
                2. Exactly 3 concise bullet points focusing strictly on the factual who, what, when, and where.

                Format your response exactly like this:
                TITLE: [Your Title Here]
                * [Point 1]
                * [Point 2]
                * [Point 3]

                CRITICAL RULES:
                - Do not include any introductory or concluding phrases.
                - Do not use curly or smart quotes (‘ ’ “ ”). Use only standard straight quotes (' ").

                ARTICLE TEXT:
                {article_text}
                """
        
        # 2. The API Call
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash', 
                contents=my_prompt
            )
            
            # 3. The Question Mark Fix (The programmatic cleanup)
            clean_text = response.text
            clean_text = clean_text.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
            
            summary.append(clean_text)
            
        except Exception as e:
            print(f"[Error generating summary for article {index}: {e}]")
            # Append a formatted error placeholder so the PDF layout doesn't break
            summary.append("TITLE: ⚠️ Error\n* Could not generate summary for this article.")
        
        # 4. Rate Limit Pause
        time.sleep(4) 
        
    return summary

def create_pdf(ai_sum):
    # Initialize the PDF
    pdf = FPDF(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Add a Document Header
    pdf.set_font("Helvetica", style="B", size=24)
    pdf.set_text_color(214, 157, 16) # Deep blue
    pdf.cell(w=0, h=12, text="Daily News Digest", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.ln(2)
    
    # Add a Date Subheader
    pdf.set_font("Helvetica", "", size=12)
    pdf.set_text_color(128, 128, 128) # Gray
    pdf.cell(w=0, h=6, text=f"Generated on {date.today()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.ln(5)
    
    # Draw a horizontal dividing line
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Loop through the data and print to PDF
    for index, ai_text in enumerate(ai_sum, 1):
        lines = ai_text.split("\n")
        raw_headline = lines[0].replace("TITLE: ", "").strip()
        raw_summary = "\n".join(lines[1:]).strip()
        
        # Clean up strings for standard PDF fonts
        headline = raw_headline.encode('latin-1', 'replace').decode('latin-1')
        summary = raw_summary.encode('latin-1', 'replace').decode('latin-1')

        #print headline
        pdf.set_font("Helvetica", style="B", size = 14)
        pdf.set_text_color(0, 0, 139) # Dark BLue
        pdf.multi_cell(w=0, h=7, text=f"{index}. {headline}")
        pdf.ln(2)           

        # Print Summary Body
        pdf.set_font("Helvetica", style="", size=11)
        pdf.set_text_color(0, 0, 0) #pure black
        pdf.multi_cell(w=0, h=6, text=summary)
        # Divider Space
        pdf.ln(10)
    # Save the document
    pdf.output("Your Daily News.pdf")
    print(f"✅ Success! Open {"Your Daily News.pdf"} to see the result.")
    
if __name__ == "__main__":
    main()

