"""
Convert a Jekyll blog post (markdown) to an MP3 audio file and upload to HuggingFace.
Adapted from research/improving_catllm_classification/convert_results_to_audio.py
"""

import re
import asyncio
import os
import edge_tts
from pydub import AudioSegment
from huggingface_hub import HfApi


def clean_blog_text(text):
    # Strip YAML front matter (--- ... ---)
    text = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)

    # Remove HTML comments <!-- ... -->
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # Remove HTML tags <...>
    text = re.sub(r'<[^>]+>', '', text)

    # Remove image references  ![...](...)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

    # Remove code blocks (``` ... ```) — not readable aloud
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # Remove inline code backticks but keep the text
    text = re.sub(r'`([^`]+)`', r'\1', text)

    # Remove markdown tables (lines starting with |)
    text = re.sub(r'(\|[^\n]+\|\n?)+', '', text)

    # Convert headers: strip # markers but keep the heading text as a sentence
    text = re.sub(r'^#{1,4}\s+(.+)$', r'\1.', text, flags=re.MULTILINE)

    # Convert links [text](url) → just text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Remove horizontal rules
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)

    # Remove bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)

    # Remove blockquote markers
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)

    # Translate symbols that TTS reads awkwardly
    text = text.replace('–', ' to ')
    text = text.replace('—', ', ')
    text = text.replace('×10⁻⁶', 'times ten to the negative six')
    text = text.replace('²', ' squared')
    text = text.replace('R²', 'R squared')
    text = text.replace('%', ' percent')
    text = text.replace('~', 'approximately ')
    text = text.replace('≥', ' or more')
    text = text.replace('≤', ' or fewer')

    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    return text.strip()


async def generate_audio(text, output_file, voice="en-US-BrianNeural", chunk_size=5000):
    if len(text) <= chunk_size:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    else:
        chunks = []
        current_chunk = ""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        if current_chunk:
            chunks.append(current_chunk.strip())

        print(f"  Splitting into {len(chunks)} chunks...")
        temp_files = []
        for i, chunk in enumerate(chunks):
            temp_file = f"temp_chunk_{i}.mp3"
            temp_files.append(temp_file)
            print(f"  Chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
            communicate = edge_tts.Communicate(chunk, voice)
            await communicate.save(temp_file)

        combined = AudioSegment.empty()
        for temp_file in temp_files:
            combined += AudioSegment.from_mp3(temp_file)
            os.remove(temp_file)

        combined.export(output_file, format="mp3")


def upload_to_huggingface(mp3_path, repo_id, filename):
    api = HfApi()
    # Create the dataset repo if it doesn't exist
    try:
        api.create_repo(repo_id=repo_id, repo_type="dataset", exist_ok=True)
        print(f"Repo {repo_id} ready.")
    except Exception as e:
        print(f"Repo creation note: {e}")

    api.upload_file(
        path_or_fileobj=mp3_path,
        path_in_repo=filename,
        repo_id=repo_id,
        repo_type="dataset",
    )
    url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{filename}"
    print(f"Uploaded: {url}")
    return url


def main():
    blog_path = "_posts/2026-03-02-catvader-threads-analysis.md"
    mp3_file = "catvader-threads-analysis.mp3"
    hf_repo = "chrissoria/blog-audio"

    with open(blog_path, "r", encoding="utf-8") as f:
        raw = f.read()

    cleaned = clean_blog_text(raw)
    print(f"Cleaned text: {len(cleaned)} characters.")
    print("\n--- Preview (first 500 chars) ---")
    print(cleaned[:500])
    print("---\n")

    print("Generating audio (en-US-BrianNeural)...")
    asyncio.run(generate_audio(cleaned, mp3_file))
    print(f"Saved: {mp3_file}")

    size_mb = os.path.getsize(mp3_file) / (1024 * 1024)
    print(f"File size: {size_mb:.1f} MB")

    print("Uploading to HuggingFace...")
    url = upload_to_huggingface(mp3_file, hf_repo, mp3_file)

    print(f"\nEmbed in Jekyll with:\n")
    print(f'<audio controls style="width:100%">')
    print(f'  <source src="{url}" type="audio/mpeg">')
    print(f'</audio>')


if __name__ == "__main__":
    main()
