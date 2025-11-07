import logging
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (required for STDIO servers)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Initialize FastMCP server
mcp = FastMCP("charlie")

# Constants
DOC_FILE = Path(__file__).parent / "doc.md"

def read_doc_file() -> str:
    """Read the documentation file."""
    try:
        if DOC_FILE.exists():
            return DOC_FILE.read_text(encoding='utf-8')
        else:
            return "Documentation file (doc.md) not found."
    except Exception as e:
        logging.error(f"Error reading doc file: {e}")
        return f"Error reading documentation: {str(e)}"

def search_doc_content(content: str, query: str) -> str:
    """Search for relevant content in the documentation based on a query."""
    if not query:
        return content
    
    query_lower = query.lower()
    lines = content.split('\n')
    relevant_lines = []
    
    # Find lines that contain the query
    for i, line in enumerate(lines):
        if query_lower in line.lower():
            # Include some context (previous and next lines)
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            context = '\n'.join(lines[start:end])
            if context not in relevant_lines:
                relevant_lines.append(context)
    
    if relevant_lines:
        return "\n\n---\n\n".join(relevant_lines)
    else:
        # If no exact match, return the full content
        return content

@mcp.tool()
async def get_charlie_info(query: str = "") -> str:
    """Get information from Charlie's documentation.
    
    This tool retrieves relevant information from the doc.md file.
    When you see "charlie" mentioned or need documentation information,
    use this tool to get the relevant details.
    
    Args:
        query: Optional search query to find specific information in the documentation.
               If empty, returns the full documentation.
    """
    logging.info(f"Getting Charlie info for query: {query}")
    
    doc_content = read_doc_file()
    
    if query:
        result = search_doc_content(doc_content, query)
    else:
        result = doc_content
    
    return result

def main():
    # Initialize and run the server
    logging.info("Starting MCP Charlie documentation server...")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()

