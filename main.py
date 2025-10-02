import sys
from summariser import summarize_text, summarize_url

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <text_or_url>")
    else:
        input_data = sys.argv[1]
        print("\n🔄 Summarizing...\n")
        
        if input_data.startswith("http"):
            summary = summarize_url(input_data)
        else:
            summary = summarize_text(input_data)
        
        print("📰 3-Line Summary:")
        print(summary)
