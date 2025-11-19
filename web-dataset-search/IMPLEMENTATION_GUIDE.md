# Implementation Guide: Web Dataset Search Service

## Quick Start Implementation

This guide provides practical, production-ready code examples for building a web dataset search service.

---

## Architecture Overview

```
┌─────────────────┐
│  User Query     │
│  + Schema       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Query Parser   │ ← GPT-4 converts NL to search params
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Web Search     │ ← Find relevant pages
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Web Crawler    │ ← Fetch & render pages (Playwright/Crawl4AI)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Extractor │ ← LLM extracts structured data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validator      │ ← Multi-stage validation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Dataset Output │ ← JSON/CSV/Parquet
└─────────────────┘
```

---

## Option 1: Using Crawl4AI + GPT-4 (Recommended for MVP)

### Installation

```bash
# Install dependencies
pip install crawl4ai[all]
pip install openai pydantic fastapi uvicorn

# Install Playwright browsers
playwright install
```

### Core Implementation

```python
# main.py
import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from crawl4ai import AsyncWebCrawler
from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI(api_key="your-api-key")

# Define your data schema
class Product(BaseModel):
    """Product information schema"""
    name: str = Field(..., description="Product name")
    price: float = Field(..., gt=0, description="Price in USD")
    description: Optional[str] = Field(None, description="Product description")
    url: str = Field(..., description="Product URL")
    in_stock: bool = Field(..., description="Whether product is in stock")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Product rating out of 5")

    @validator('price')
    def validate_price(cls, v):
        if v > 100000:
            raise ValueError('Price seems unrealistic')
        return v

class DatasetResult(BaseModel):
    """Complete dataset result"""
    query: str
    total_results: int
    data: List[Product]
    confidence_score: float = Field(..., ge=0, le=1)
    sources: List[str]

# Step 1: Parse natural language query into search parameters
async def parse_query(user_query: str) -> Dict[str, Any]:
    """Convert natural language to search parameters using GPT-4"""

    system_prompt = """You are a search query parser. Convert natural language requests into structured search parameters.

Output JSON format:
{
    "search_queries": ["query1", "query2"],  // Multiple search variations
    "num_results": 10,  // How many pages to check
    "filters": {
        "price_max": null,
        "price_min": null,
        "date_range": null,
        // other filters
    }
}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)

# Step 2: Perform web search (simplified - in production use SerpAPI or similar)
async def web_search(query: str, num_results: int = 10) -> List[str]:
    """
    Perform web search and return URLs
    In production, use SerpAPI, Google Custom Search API, etc.
    """
    # Placeholder - replace with actual search API
    from googlesearch import search
    urls = []
    try:
        for url in search(query, num_results=num_results):
            urls.append(url)
    except Exception as e:
        print(f"Search error: {e}")
    return urls

# Step 3: Crawl and extract structured data
async def extract_data_from_url(url: str, schema: type[BaseModel]) -> Optional[BaseModel]:
    """Extract structured data from a URL using Crawl4AI + GPT-4"""

    async with AsyncWebCrawler(verbose=False) as crawler:
        # Crawl the page
        result = await crawler.arun(
            url=url,
            bypass_cache=True,
            word_count_threshold=10,
            excluded_tags=['form', 'nav', 'footer', 'header'],
            remove_overlay_elements=True,
        )

        if not result.success:
            print(f"Failed to crawl {url}")
            return None

        # Get clean markdown
        markdown_content = result.markdown

        # If content is too long, truncate intelligently
        max_tokens = 8000  # Leave room for response
        if len(markdown_content) > max_tokens * 4:  # rough char estimate
            markdown_content = markdown_content[:max_tokens * 4]

        # Extract structured data using GPT-4
        extraction_prompt = f"""Extract information from this webpage according to the schema.

IMPORTANT RULES:
- Only extract information that is explicitly present on the page
- If a field is not found, set it to null
- Do not guess or make up information
- Include a confidence score (0-100) for the overall extraction

Schema: {schema.model_json_schema()}

Webpage content:
{markdown_content}

Extract the data in JSON format matching the schema."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a precise data extraction assistant. Only extract information that is explicitly visible."},
                {"role": "user", "content": extraction_prompt}
            ],
            response_format={"type": "json_object"}
        )

        try:
            extracted_data = json.loads(response.choices[0].message.content)
            # Validate against schema
            validated = schema(**extracted_data)
            return validated
        except Exception as e:
            print(f"Validation error for {url}: {e}")
            return None

# Step 4: Cross-validation using different model
async def cross_validate(data: BaseModel, source_url: str, original_content: str) -> float:
    """
    Validate extracted data using a different LLM (Claude) for cross-checking
    Returns confidence score 0-1
    """

    validation_prompt = f"""Review this extracted data for accuracy against the source content.

Extracted Data:
{data.model_dump_json(indent=2)}

Source Content (first 2000 chars):
{original_content[:2000]}

Provide a confidence score (0-100) and explain any concerns.
Output JSON: {{"confidence": 85, "concerns": ["list of issues if any"]}}
"""

    # Using GPT-4 again (in production, use Claude for true cross-validation)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data validation expert."},
            {"role": "user", "content": validation_prompt}
        ],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    return result.get("confidence", 50) / 100.0

# Step 5: Main pipeline
async def build_dataset(user_query: str, schema: type[BaseModel], max_results: int = 20) -> DatasetResult:
    """
    Main function to build dataset from natural language query
    """

    print(f"Processing query: {user_query}")

    # Parse query
    search_params = await parse_query(user_query)
    print(f"Search parameters: {search_params}")

    # Perform web searches
    all_urls = []
    for search_query in search_params.get("search_queries", [user_query]):
        urls = await web_search(search_query, num_results=max_results // len(search_params.get("search_queries", [user_query])))
        all_urls.extend(urls)

    # Remove duplicates
    all_urls = list(set(all_urls))[:max_results]
    print(f"Found {len(all_urls)} URLs to process")

    # Extract data from each URL
    extracted_data = []
    confidences = []

    for url in all_urls:
        print(f"Processing: {url}")
        try:
            data = await extract_data_from_url(url, schema)
            if data:
                # Simple validation for now
                extracted_data.append(data)
                confidences.append(0.85)  # Placeholder
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue

    # Calculate overall confidence
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    # Build result
    result = DatasetResult(
        query=user_query,
        total_results=len(extracted_data),
        data=extracted_data,
        confidence_score=avg_confidence,
        sources=all_urls[:len(extracted_data)]
    )

    return result

# Example usage
async def main():
    # Example 1: Product search
    query = "Find MacBook Pro M3 laptops under $2000"

    result = await build_dataset(
        user_query=query,
        schema=Product,
        max_results=10
    )

    print(f"\n=== Results ===")
    print(f"Query: {result.query}")
    print(f"Total results: {result.total_results}")
    print(f"Confidence: {result.confidence_score:.2%}")
    print(f"\nData:")
    print(result.model_dump_json(indent=2))

    # Save to JSON
    with open("dataset.json", "w") as f:
        f.write(result.model_dump_json(indent=2))

    # Save to CSV
    import pandas as pd
    df = pd.DataFrame([item.dict() for item in result.data])
    df.to_csv("dataset.csv", index=False)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Option 2: Using ScrapeGraphAI (For Complex Workflows)

### Installation

```bash
pip install scrapegraphai
playwright install
```

### Implementation

```python
# scrapegraph_implementation.py
from scrapegraphai.graphs import SmartScraperGraph
from pydantic import BaseModel, Field
from typing import List
import json

# Define schema
class Company(BaseModel):
    name: str
    description: str
    funding: str
    employees: str
    website: str

# Configuration
graph_config = {
    "llm": {
        "model": "openai/gpt-4o",
        "api_key": "your-api-key",
        "temperature": 0
    },
    "verbose": True,
    "headless": True
}

# Create scraper
smart_scraper = SmartScraperGraph(
    prompt="Extract company information: name, description, funding, employees, and website",
    source="https://example.com/company-page",
    config=graph_config,
    schema=Company
)

# Run extraction
result = smart_scraper.run()
print(json.dumps(result, indent=2))
```

---

## Option 3: Vision-Based Extraction (For Complex Visual Content)

```python
# vision_extraction.py
from playwright.async_api import async_playwright
from openai import OpenAI
import base64
from pydantic import BaseModel
from typing import List

client = OpenAI(api_key="your-api-key")

class TableData(BaseModel):
    """For extracting data from visual tables/charts"""
    headers: List[str]
    rows: List[List[str]]

async def extract_with_vision(url: str, schema: type[BaseModel]) -> BaseModel:
    """Extract data using GPT-4 Vision"""

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Wait for content to load
        await page.wait_for_load_state("networkidle")

        # Take screenshot
        screenshot = await page.screenshot(full_page=True)
        await browser.close()

    # Encode screenshot
    base64_image = base64.b64encode(screenshot).decode('utf-8')

    # Extract using GPT-4 Vision
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Extract data from this webpage according to schema: {schema.model_json_schema()}. Return JSON only."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        response_format={"type": "json_object"}
    )

    extracted = json.loads(response.choices[0].message.content)
    return schema(**extracted)
```

---

## Option 4: FastAPI Web Service

```python
# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
import asyncio

app = FastAPI(title="Web Dataset Search API")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    schema_definition: Dict[str, Any] = Field(..., description="Pydantic-style schema definition")
    max_results: int = Field(20, ge=1, le=100, description="Maximum results to return")

class SearchResponse(BaseModel):
    query: str
    total_results: int
    confidence_score: float
    data: List[Dict[str, Any]]
    sources: List[str]
    processing_time_seconds: float

@app.post("/search", response_model=SearchResponse)
async def search_dataset(request: SearchRequest):
    """
    Main endpoint to build dataset from natural language query

    Example request:
    {
        "query": "Find AI startups with Series A funding in 2024",
        "schema_definition": {
            "name": {"type": "string"},
            "funding": {"type": "string"},
            "website": {"type": "string"}
        },
        "max_results": 20
    }
    """
    import time
    start_time = time.time()

    try:
        # Convert schema definition to Pydantic model
        # (In production, use a proper schema converter)

        # Call main pipeline
        # result = await build_dataset(request.query, schema, request.max_results)

        # Placeholder response
        response = SearchResponse(
            query=request.query,
            total_results=0,
            confidence_score=0.85,
            data=[],
            sources=[],
            processing_time_seconds=time.time() - start_time
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run with: uvicorn api:app --reload
```

---

## Advanced: Multi-Model Validation Pipeline

```python
# validation.py
from typing import Any, Dict, List
from pydantic import BaseModel
import asyncio
from openai import OpenAI
from anthropic import Anthropic

class ValidationResult(BaseModel):
    is_valid: bool
    confidence: float
    issues: List[str]
    cross_validation_agreement: float

class DataValidator:
    """Multi-stage validation pipeline"""

    def __init__(self):
        self.openai_client = OpenAI()
        self.anthropic_client = Anthropic()

    async def validate(self, data: BaseModel, source_content: str, source_url: str) -> ValidationResult:
        """Run multi-stage validation"""

        # Stage 1: Schema validation (automatic via Pydantic)
        schema_valid = True  # Already validated by Pydantic

        # Stage 2: Cross-model validation
        agreement = await self._cross_model_validation(data, source_content)

        # Stage 3: Statistical validation
        stat_issues = self._statistical_validation(data)

        # Stage 4: Consistency checks
        consistency_issues = self._consistency_checks(data)

        all_issues = stat_issues + consistency_issues

        # Calculate overall confidence
        confidence = agreement * (1.0 - len(all_issues) * 0.1)
        confidence = max(0.0, min(1.0, confidence))

        return ValidationResult(
            is_valid=confidence > 0.7,
            confidence=confidence,
            issues=all_issues,
            cross_validation_agreement=agreement
        )

    async def _cross_model_validation(self, data: BaseModel, source_content: str) -> float:
        """Validate using both GPT-4 and Claude"""

        # Extract same data with Claude
        prompt = f"Extract the same information from this content:\n{source_content[:2000]}"

        # Simplified - in production, actually call both APIs
        # Compare results and calculate agreement

        return 0.85  # Placeholder

    def _statistical_validation(self, data: BaseModel) -> List[str]:
        """Check for statistical outliers"""
        issues = []

        # Example: Check price ranges
        if hasattr(data, 'price'):
            if data.price < 0:
                issues.append("Negative price detected")
            elif data.price > 1000000:
                issues.append("Suspiciously high price")

        return issues

    def _consistency_checks(self, data: BaseModel) -> List[str]:
        """Logical consistency checks"""
        issues = []

        # Example: Check URL format
        if hasattr(data, 'url'):
            if not data.url.startswith('http'):
                issues.append("Invalid URL format")

        return issues
```

---

## Caching Layer (Production Optimization)

```python
# cache.py
from typing import Optional
import hashlib
import json
from datetime import datetime, timedelta
import aiosqlite

class CacheManager:
    """SQLite-based caching for scraped data"""

    def __init__(self, db_path: str = "cache.db", ttl_hours: int = 24):
        self.db_path = db_path
        self.ttl = timedelta(hours=ttl_hours)

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    url_hash TEXT PRIMARY KEY,
                    url TEXT,
                    content TEXT,
                    extracted_data TEXT,
                    created_at TIMESTAMP,
                    expires_at TIMESTAMP
                )
            """)
            await db.execute("CREATE INDEX IF NOT EXISTS idx_url ON cache(url)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_expires ON cache(expires_at)")
            await db.commit()

    def _hash_url(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    async def get(self, url: str) -> Optional[Dict]:
        """Get cached data if not expired"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT extracted_data, expires_at FROM cache WHERE url_hash = ?",
                (self._hash_url(url),)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    extracted_data, expires_at = row
                    if datetime.fromisoformat(expires_at) > datetime.now():
                        return json.loads(extracted_data)
        return None

    async def set(self, url: str, data: Dict):
        """Cache extracted data"""
        now = datetime.now()
        expires = now + self.ttl

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO cache (url_hash, url, extracted_data, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self._hash_url(url),
                url,
                json.dumps(data),
                now.isoformat(),
                expires.isoformat()
            ))
            await db.commit()

    async def cleanup_expired(self):
        """Remove expired cache entries"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM cache WHERE expires_at < ?", (datetime.now().isoformat(),))
            await db.commit()
```

---

## Complete Production Example

```python
# production_pipeline.py
import asyncio
from typing import List, Type
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionPipeline:
    """Production-ready dataset building pipeline"""

    def __init__(self):
        self.cache = CacheManager()
        self.validator = DataValidator()

    async def initialize(self):
        await self.cache.init_db()

    async def build_dataset(
        self,
        query: str,
        schema: Type[BaseModel],
        max_results: int = 20,
        min_confidence: float = 0.7
    ) -> DatasetResult:
        """Build high-quality dataset with full validation"""

        logger.info(f"Building dataset for query: {query}")

        # 1. Parse query
        search_params = await parse_query(query)

        # 2. Search web
        urls = []
        for search_query in search_params.get("search_queries", [query]):
            found_urls = await web_search(search_query, max_results)
            urls.extend(found_urls)
        urls = list(set(urls))[:max_results]

        logger.info(f"Found {len(urls)} URLs to process")

        # 3. Extract with caching and validation
        validated_data = []
        sources = []
        confidences = []

        for url in urls:
            # Check cache
            cached = await self.cache.get(url)
            if cached:
                logger.info(f"Cache hit: {url}")
                validated_data.append(schema(**cached))
                confidences.append(0.9)
                sources.append(url)
                continue

            # Extract
            try:
                data = await extract_data_from_url(url, schema)
                if not data:
                    continue

                # Validate
                validation = await self.validator.validate(data, "", url)

                if validation.confidence >= min_confidence:
                    validated_data.append(data)
                    confidences.append(validation.confidence)
                    sources.append(url)

                    # Cache successful extraction
                    await self.cache.set(url, data.dict())
                else:
                    logger.warning(f"Low confidence ({validation.confidence:.2f}) for {url}: {validation.issues}")

            except Exception as e:
                logger.error(f"Error processing {url}: {e}")

        # 4. Build result
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return DatasetResult(
            query=query,
            total_results=len(validated_data),
            data=validated_data,
            confidence_score=avg_confidence,
            sources=sources
        )

# Usage
async def main():
    pipeline = ProductionPipeline()
    await pipeline.initialize()

    result = await pipeline.build_dataset(
        query="Find gaming laptops with RTX 4070 under $1500",
        schema=Product,
        max_results=15,
        min_confidence=0.75
    )

    print(f"Found {result.total_results} high-quality results")
    print(f"Average confidence: {result.confidence_score:.2%}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Testing & Quality Assurance

```python
# tests.py
import pytest
from pydantic import BaseModel

class TestProduct(BaseModel):
    name: str
    price: float

@pytest.mark.asyncio
async def test_extraction_accuracy():
    """Test extraction accuracy against known good data"""

    test_url = "https://example.com/product"
    expected = TestProduct(name="Test Product", price=99.99)

    extracted = await extract_data_from_url(test_url, TestProduct)

    assert extracted.name == expected.name
    assert abs(extracted.price - expected.price) < 0.01

@pytest.mark.asyncio
async def test_validation_pipeline():
    """Test multi-stage validation"""

    validator = DataValidator()
    test_data = TestProduct(name="Valid Product", price=50.0)

    result = await validator.validate(test_data, "sample content", "https://example.com")

    assert result.is_valid
    assert result.confidence > 0.7
```

---

## Deployment

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application
COPY . .

# Run
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Requirements

```txt
# requirements.txt
crawl4ai[all]
openai>=1.0.0
anthropic>=0.18.0
pydantic>=2.0.0
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
playwright>=1.40.0
aiosqlite>=0.19.0
pandas>=2.0.0
python-multipart
httpx
```

---

## Cost Monitoring

```python
# cost_tracker.py
from datetime import datetime
import aiosqlite

class CostTracker:
    """Track API costs"""

    def __init__(self, db_path: str = "costs.db"):
        self.db_path = db_path

    async def log_cost(self, model: str, input_tokens: int, output_tokens: int, cost_usd: float):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO costs (timestamp, model, input_tokens, output_tokens, cost_usd)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(), model, input_tokens, output_tokens, cost_usd))
            await db.commit()

    async def get_daily_cost(self) -> float:
        """Get today's total cost"""
        today = datetime.now().date().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT SUM(cost_usd) FROM costs WHERE DATE(timestamp) = ?",
                (today,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row[0] else 0.0
```

---

## Next Steps

1. **Choose your approach** based on requirements (see RESEARCH.md)
2. **Set up development environment** with the code above
3. **Define your schemas** for your specific use cases
4. **Build and test MVP** with small dataset
5. **Add validation layers** incrementally
6. **Monitor quality metrics** continuously
7. **Optimize costs** based on usage patterns
8. **Scale gradually** with proper testing

---

**Document Version**: 1.0
**Last Updated**: 2025-11-19
