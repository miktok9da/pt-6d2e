"""
Generate 600 Portuguese topics about ancient women's history.
"""

import os
import requests
from urllib.parse import quote
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv()

def generate_french_topics_batch(batch_num, count=100):
    """Generate a batch of Portuguese topics."""
    
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        print(f"[batch {batch_num}] Error: POLLINATIONS_API_KEY not found in .env")
        return []
    
    # Simpler system prompt
    system = (
        "You are a historian specialized in ancient women's history. "
        f"Create {count} unique topics in Portuguese about women in ancient civilizations. "
        "Each topic should be 5-10 words, interesting and educational. "
        "Cover: laws, customs, famous women, professions, religion, culture, art. "
        "Output ONLY the topics, one per line, no numbers or bullets."
    )
    
    prompt = f"Generate {count} unique Portuguese topics about women in ancient civilizations"
    
    headers = {"Authorization": f"Bearer {api_key}"}
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
    
    print(f"[batch {batch_num}] Generating {count} Portuguese topics...")
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        
        # Parse topics from chat completions response
        content = r.json()['choices'][0]['message']['content'].strip()
        
        # Parse topics
        topics = []
        for line in content.split('\n'):
            cleaned = line.strip()
            # Remove common prefixes
            for prefix in ['- ', '* ', '• ', '→ ', '> ']:
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix):]
            # Remove numbering
            import re
            cleaned = re.sub(r'^\d+[\.\:\)\-]\s*', '', cleaned)
            
            if cleaned and len(cleaned) > 5:
                topics.append(cleaned)
        
        print(f"[batch {batch_num}] Generated {len(topics)} topics")
        return topics[:count]
    
    except Exception as e:
        print(f"[batch {batch_num}] Error: {e}")
        return []

def main():
    """Generate 600 Portuguese topics in batches."""
    
    all_topics = []
    batches = 6  # 6 batches of 100 = 600 topics
    
    for i in range(batches):
        topics = generate_french_topics_batch(i+1, 100)
        all_topics.extend(topics)
        
        print(f"[progress] Total topics so far: {len(all_topics)}")
        
        # Wait between batches to avoid rate limits
        if i < batches - 1:
            print("[progress] Waiting 5 seconds before next batch...")
            time.sleep(5)
    
    # Write to file
    topics_file = Path('topics.txt')
    with open(topics_file, 'w', encoding='utf-8') as f:
        for topic in all_topics:
            f.write(f"{topic}\n")
    
    print(f"\n[done] Generated {len(all_topics)} Portuguese topics!")
    print(f"[done] Saved to {topics_file}")

if __name__ == '__main__':
    main()
