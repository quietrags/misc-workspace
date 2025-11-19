"""
Simple Example: Web Dataset Search with Natural Language

This example shows how to build a dataset from web searches using natural language queries.

Requirements:
    pip install openai pydantic

Environment:
    export OPENAI_API_KEY="your-api-key"
"""

import os
import json
from typing import Optional
from pydantic import BaseModel, Field, validator
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define your data schema
class Product(BaseModel):
    """Schema for product information"""
    name: str = Field(..., description="Product name")
    price: float = Field(..., gt=0, description="Price in USD")
    description: Optional[str] = Field(None, description="Product description")
    url: str = Field(..., description="Product URL")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Rating out of 5")

    @validator('price')
    def validate_price(cls, v):
        if v > 1000000:
            raise ValueError('Price seems unrealistic')
        return round(v, 2)


def parse_query_to_search(user_query: str) -> str:
    """
    Convert natural language query to search terms

    Example:
        "Find MacBook Pro laptops under $2000" → "MacBook Pro price buy"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using mini for cost efficiency
        messages=[
            {
                "role": "system",
                "content": "Convert the user's request into effective web search keywords. Return only the search query, nothing else."
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return response.choices[0].message.content.strip()


def extract_from_text(text_content: str, schema_description: str) -> dict:
    """
    Extract structured data from text using GPT-4 with schema

    This is a simplified version - in production you'd:
    1. Actually scrape the web pages
    2. Use Playwright for JavaScript rendering
    3. Add multi-stage validation
    """

    extraction_prompt = f"""Extract product information from this text.

Schema: {schema_description}

IMPORTANT RULES:
- Only extract information that is explicitly present
- If a field is not found, set it to null
- Do not guess or make up information
- Be precise with numbers

Text:
{text_content[:4000]}  # Limit context

Return valid JSON matching the schema."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a precise data extraction assistant."
            },
            {
                "role": "user",
                "content": extraction_prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


def simple_demo():
    """
    Simplified demonstration of the concept

    In production, you would:
    1. Actually perform web searches (using SerpAPI, Google Custom Search, etc.)
    2. Crawl the pages (using Playwright, Crawl4AI, etc.)
    3. Extract with validation
    4. Cross-validate with multiple models
    """

    print("=" * 60)
    print("Web Dataset Search - Simple Demo")
    print("=" * 60)

    # Example query
    user_query = "Find MacBook Pro M3 laptops with prices"
    print(f"\nUser Query: {user_query}")

    # Step 1: Convert to search terms
    search_query = parse_query_to_search(user_query)
    print(f"Search Query: {search_query}")

    # Step 2: Simulate scraped content (in production, you'd actually scrape)
    simulated_content = """
    MacBook Pro 14-inch with M3 chip

    Price: $1,599.00

    The new MacBook Pro 14-inch features the powerful M3 chip,
    delivering exceptional performance for professionals.

    Specifications:
    - M3 chip with 8-core CPU
    - 14-inch Liquid Retina XDR display
    - 8GB unified memory
    - 512GB SSD storage

    Rating: 4.8 out of 5 stars

    Buy now: https://www.apple.com/shop/buy-mac/macbook-pro/14-inch-m3
    """

    print("\n" + "-" * 60)
    print("Simulated Content Preview:")
    print(simulated_content[:200] + "...")
    print("-" * 60)

    # Step 3: Extract structured data
    print("\nExtracting structured data...")
    schema_description = Product.model_json_schema()

    try:
        extracted_data = extract_from_text(simulated_content, json.dumps(schema_description))

        # Validate with Pydantic
        product = Product(**extracted_data)

        print("\n✅ Extraction successful!")
        print("\nExtracted Product Data:")
        print(json.dumps(product.model_dump(), indent=2))

        # Save to file
        with open("extracted_product.json", "w") as f:
            f.write(product.model_dump_json(indent=2))
        print("\n💾 Saved to: extracted_product.json")

    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        return

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)

    print("\n📚 Next steps:")
    print("1. See RESEARCH.md for complete approach details")
    print("2. See IMPLEMENTATION_GUIDE.md for production code")
    print("3. Try advanced_validation.py for multi-stage validation")
    print("\n⚠️  Note: This is a simplified demo using simulated content.")
    print("For real web scraping, use Crawl4AI or Playwright.")


def custom_query_demo():
    """
    Interactive demo where you can try your own query
    """
    print("\n" + "=" * 60)
    print("Custom Query Demo")
    print("=" * 60)

    # Define a flexible schema
    class GenericItem(BaseModel):
        title: str
        description: Optional[str]
        price: Optional[float]
        url: Optional[str]
        additional_info: Optional[dict]

    # Get user input
    print("\nEnter your search query (or press Enter for default):")
    query = input("> ").strip()

    if not query:
        query = "Find wireless headphones with noise cancellation"
        print(f"Using default: {query}")

    # Simulate finding content
    print("\n[Simulating web search and extraction...]")
    print("(In production, this would actually search and scrape the web)")

    # This is where you'd integrate actual web scraping
    print(f"\nSearch query: {parse_query_to_search(query)}")
    print("\n✅ In a real implementation, this would:")
    print("   1. Search Google/Bing for relevant pages")
    print("   2. Crawl top N results with Playwright/Crawl4AI")
    print("   3. Extract structured data with GPT-4")
    print("   4. Validate with multi-stage pipeline")
    print("   5. Return high-quality dataset")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("\nSet it with:")
        print('  export OPENAI_API_KEY="your-api-key"')
        exit(1)

    # Run simple demo
    simple_demo()

    # Optionally run custom query demo
    print("\n" + "=" * 60)
    response = input("\nWould you like to try a custom query? (y/n): ").strip().lower()
    if response == 'y':
        custom_query_demo()
