"""
Generate new topics using AI when topics.txt runs low.

This script:
1. Checks if topics.txt has enough topics (< 50 remaining)
2. Generates 100 new unique topics using Pollinations AI
3. Appends them to topics.txt
"""

import requests
from urllib.parse import quote
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_new_topics(count=100):
    """Generate new Portuguese topics about ancient women using paid Pollinations API."""
    
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        raise ValueError("POLLINATIONS_API_KEY environment variable is required for paid API")
    
    system = (
        "Você é um historiador especializado na história das mulheres nas civilizações antigas. "
        f"Crie uma lista de {count} tópicos únicos em português. "
        "Cada tópico deve ser curto (5-10 palavras), interessante e educativo. "
        "Os tópicos devem cobrir: as leis, os costumes, as mulheres famosas, as profissões, a religião, a cultura, a arte. "
        "Produza APENAS os tópicos, um por linha, sem números ou marcadores."
    )
    
    prompt = f"Crie {count} tópicos únicos sobre mulheres nas civilizações antigas"
    
    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "jsonMode": False
    }
    
    url = "https://gen.pollinations.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    print(f"[topics] Generating {count} new Portuguese topics...")
    for _attempt in range(3):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=180)
            break
        except Exception as e:
            print(f"[topics] Attempt failed: {e}")
            if _attempt < 2:
                import time; time.sleep((_attempt+1)*10)
            else:
                raise
    r.raise_for_status()
    
    # Parse topics from chat completions response
    content = r.json()['choices'][0]['message']['content'].strip()
    
    # Parse topics
    topics = []
    for line in content.split('\n'):
        # Remove numbering and clean
        cleaned = line.strip()
        # Remove common prefixes
        for prefix in ['- ', '* ', '• ']:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
        # Remove numbering like "1. " or "1) "
        import re
        cleaned = re.sub(r'^\d+[\.\:\)]\s*', '', cleaned)
        
        if cleaned and len(cleaned) > 5:
            topics.append(cleaned)
    
    return topics[:count]

def check_and_update_topics():
    """Check topics.txt and add more if needed."""
    
    topics_file = Path('topics.txt')
    
    # Read existing topics
    if topics_file.exists():
        with open(topics_file, 'r', encoding='utf-8') as f:
            existing_topics = [line.strip() for line in f if line.strip()]
    else:
        existing_topics = []
    
    print(f"[topics] Current topics: {len(existing_topics)}")
    
    # Check if we need more topics (trigger at 500 instead of 50)
    if len(existing_topics) < 500:
        print(f"[topics] Low on topics! Generating 100 more...")
        
        new_topics = generate_new_topics(100)
        
        # Append to file
        with open(topics_file, 'a', encoding='utf-8') as f:
            for topic in new_topics:
                f.write(f"{topic}\n")
        
        print(f"[topics] Added {len(new_topics)} new Portuguese topics!")
        print(f"[topics] Total topics now: {len(existing_topics) + len(new_topics)}")
    else:
        print(f"[topics] Enough topics available ({len(existing_topics)})")

if __name__ == '__main__':
    check_and_update_topics()
