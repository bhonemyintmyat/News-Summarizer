from fpdf import FPDF  
from datetime import date

# 1. We create some mock news data just like your scraper would output
mock_news_data = [
    [
        "Global Markets Rally on Tech Earnings", 
        "• Technology stocks surged 4 in early trading today.\n• Investors reacted positively to better-than-expected quarterly reports.\n• Analysts predict sustained growth through the end of the fiscal year."
    ],
    [
        "Local Team Wins Championship After 10-Year Drought", 
        "• The city's football club secured a 2-1 victory in the final seconds of the match.\n• Over 50,000 fans gathered in the downtown plaza to celebrate the historic win.\n• A victory parade is scheduled for this coming Friday afternoon."
    ],
    [
        "New Solar Technology Promises 50% Higher Efficiency", 
        "• Researchers unveiled a newly designed solar panel utilizing rare-earth composites.\n• The prototype demonstrates a 50% increase in energy conversion rates compared to standard panels.\n• Commercial production is expected to begin by 2028."
    ]
]

def create_example_pdf(news_data, filename="example_news.pdf"):
    # Initialize the PDF
    pdf = FPDF(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Add a Document Header
    pdf.set_font("Helvetica", style="B", size=24)
    pdf.set_text_color(0, 51, 102) # Deep blue
    pdf.cell(w=0, h=12, text="🌍 Daily News Digest", ln=1, align="L")
    
    # Add a Date Subheader
    pdf.set_font("Helvetica", style="I", size=10)
    pdf.set_text_color(128, 128, 128) # Gray
    pdf.cell(w=0, h=6, text=f"Generated on {date.today()}", ln=1, align="L")
    pdf.ln(5)
    
    # Draw a horizontal dividing line
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Loop through the data and print to PDF
    for index, (headline, summary) in enumerate(news_data, 1):
        
        # Clean up strings for standard PDF fonts
        headline = headline.encode('latin-1', 'replace').decode('latin-1')
        summary = summary.encode('latin-1', 'replace').decode('latin-1')
        
        # Print Headline
        pdf.set_font("Helvetica", style="B", size=14)
        pdf.set_text_color(51, 51, 51)
        pdf.multi_cell(w=0, h=7, text=f"{index}. {headline}")
        pdf.ln(2)
        
        # Print Summary Body
        pdf.set_font("Helvetica", style="", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(w=0, h=6, text=summary)
        
        # Divider Space
        pdf.ln(8)
        
    # Save the document
    pdf.output(filename)
    print(f"✅ Success! Open {filename} to see the result.")

# 2. Run the function using our mock data
create_example_pdf(mock_news_data)