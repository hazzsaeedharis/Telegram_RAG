import click
from document_loader import load_document_from_url
from chunker import chunk_text
from embedder import embed_texts, embed_text
from vector_store import store_embeddings, query_top_k, clear_all_chunks
from llm_client import ask_llm

@click.group()
def cli():
    """LangChain Redis Q&A CLI"""
    pass

@cli.command()
@click.argument("url")
def index(url):
    """Load a document from URL, chunk, embed, and store in Redis."""
    click.echo(f"Loading document from: {url}")
    text = load_document_from_url(url)
    click.echo(f"Document loaded ({len(text)} chars). Chunking...")
    chunks = chunk_text(text)
    click.echo(f"Chunked into {len(chunks)} pieces. Embedding...")
    embeddings = embed_texts(chunks)
    click.echo("Storing embeddings in Redis...")
    store_embeddings(chunks, embeddings)
    click.echo("Indexing complete.")

@cli.command()
@click.argument("question")
def ask(question):
    """Ask a question. Retrieves top 3 relevant chunks and queries the LLM."""
    click.echo("Embedding question...")
    q_emb = embed_text(question)
    click.echo("Querying Redis for top 3 relevant chunks...")
    top_chunks = query_top_k(q_emb, k=3)
    if not top_chunks:
        click.echo("No indexed data found. Please run 'index' first.")
        return
    context = "\n\n".join([f"Chunk {i+1}:\n{chunk}" for i, (chunk, _) in enumerate(top_chunks)])
    prompt = (
        f"Given the following document excerpts:\n\n{context}\n\n"
        f"Answer the following question as accurately as possible:\n{question}"
    )
    click.echo("Sending prompt to LLM...")
    answer = ask_llm(prompt)
    click.echo("\n--- LLM Response ---\n")
    click.echo(answer)

@cli.command()
def clear():
    """Clear all indexed chunks from Redis."""
    clear_all_chunks()
    click.echo("All indexed chunks cleared from Redis.")

if __name__ == "__main__":
    cli()
