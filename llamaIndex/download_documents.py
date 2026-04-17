"""
LlamaIndex Documentation Crawler using Crawl4AI

This script crawls the LlamaIndex documentation site and saves each page
as a clean markdown file, optimized for RAG/LLM ingestion.

Why Crawl4AI instead of BeautifulSoup?
1. LlamaIndex docs is a JavaScript SPA (Astro/Starlight) - BS4 can't render JS
2. The site uses clean URLs (/python/framework/) not .html files
3. Crawl4AI provides built-in markdown generation for LLM workflows
4. Deep crawling handles the 400+ page navigation tree automatically

Usage:
    uv run python download_docs.py
"""

import asyncio
from pathlib import Path
from urllib.parse import urlparse

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    BFSDeepCrawlStrategy,
    DefaultMarkdownGenerator,
    FilterChain,
    URLPatternFilter,
    PruningContentFilter,
)

#configuration
BASE_URL="https://developers.llamaindex.ai/python/framework/"
OUTPUT_DIR=Path("./llamaindex-docs")
MAX_DEPTH=5

async def crawl_llamaindex_docs():
    """Crawl LLamaIndex documentation and save as markdown files"""
    OUTPUT_DIR.mkdir(exist_ok=True)

    #Browser Configuration
    browser_config=BrowserConfig(
        headless=True,
        verbose=True
    )
    #filtering the urls
    url_filter=FilterChain(filters=[
        URLPatternFilter(
            patterns=["*developers.llamaindex.ai/python/*"],
            use_glob=True,
            reverse=False
        )
    ])
    #DeepCrawl Strategy- BFS(to get all pages)

    deep_crawl=BFSDeepCrawlStrategy(
        max_depth=MAX_DEPTH,
        filter_chain=url_filter,
        include_external=False #Stay within the domain
    )

    #Content filtering 
    content_filter=PruningContentFilter(
        threshold=0.48,
        threshold_type="fixed"
    )
    #Crwaler configuration- markdown generation and content filter
    crawl_config=CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=content_filter
        ),
        deep_crawl_strategy=deep_crawl,
        verbose=True
    )
    print("="*60)
    print("LlamaIndex Documentation Crawler")
    print("="*60)
    print(f"Target: {BASE_URL}")
    print(f"Output:{OUTPUT_DIR.absolute()}")
    print(f"Strategy:BFS Deep Crawl(max_depth={MAX_DEPTH})")
    print("-"*60)
    print("Starting crawl... This will take 5-10 minutes\n")

    ##instantiating a webcrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        results=await crawler.arun(
            BASE_URL,
            config=crawl_config
        )
        # Convert a single output to list
        if not isinstance(results,list):
            results=[results]

        saved_count=0
        failed_count=0

        for i,result in enumerate(results):
            if result.success and result.markdown:
                # Use fit_markdown for RAg-optimized source
                md_result=result.markdown
                content=md_result.fit_markdown if md_result.fit_markdown else md_result.raw_markdown

                if content:
                    #create file names corresponding to URLs
                    parsed=urlparse(result.url)
                    path_parts=[p for p in parsed.path.strip("/").split("/") if p]
                    filename="_".join(path_parts) if path_parts else "index"
                    filename=f"{filename}.md"

                    #save the file
                    filepath=OUTPUT_DIR / filename
                    filepath.write_text(content,encoding="uft-8")
                    print(f"[{i+1:3d}] Saved: {filename} ({len(content):,} chars)")
                    saved_count+=1
                else:
                    print(f"[{i+1:3d}] Empty: {result.url}")
                    failed_count+=1
            else:
                error_msg=getattr(result,'error_message','Unknwon error')
                print(f"[{i+1:3d}] Failed: {result.url} - {error_msg}")
                failed_count+=1
    #Summary
    print("\n"+ "="*60)
    print("Crawl Complete")
    print("="*60)
    print(f"Pages saved:{saved_count}")
    print(f"Pages failed:{failed_count}")
    print(f"Output Directory:{OUTPUT_DIR.absolute()}")
    print(f"Total Files: {len(list(OUTPUT_DIR.glob('*.md')))}")


if __name__ == "__main__":
    asyncio.run(crawl_llamaindex_docs())
        



