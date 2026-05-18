from app import knowledge_loader
from retrieval import chunker


def test_chunk_document_returns_chunks():
    docs = knowledge_loader.get_index()["documents"]
    chunks = chunker.chunk_document(docs[0])
    assert len(chunks) >= 1


def test_build_chunk_id_format():
    assert chunker.build_chunk_id("doc-1", 0) == "doc-1#chunk-000"


def test_chunk_all_documents_returns_chunks():
    docs = knowledge_loader.get_index()["documents"]
    chunks = chunker.chunk_all_documents(docs)
    assert len(chunks) >= len(docs)


def test_chunks_keep_doc_id_and_domain():
    docs = knowledge_loader.get_index()["documents"]
    chunks = chunker.chunk_document(docs[0])
    for c in chunks:
        assert c["doc_id"] == docs[0]["metadata"]["id"]
        assert c["domain"] == docs[0]["metadata"]["domain"]


def test_summarize_chunks_keys():
    docs = knowledge_loader.get_index()["documents"]
    chunks = chunker.chunk_all_documents(docs)
    summary = chunker.summarize_chunks(chunks)
    assert set(summary.keys()) >= {"total_chunks", "documents_chunked", "by_domain"}


def test_empty_body_yields_no_chunks():
    chunks = chunker.chunk_document({"metadata": {"id": "x"}, "body": ""})
    assert chunks == []
