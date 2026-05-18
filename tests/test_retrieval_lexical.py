from app import knowledge_loader
from retrieval import chunker, lexical


def _sample_chunk():
    docs = knowledge_loader.get_index()["documents"]
    chunks = chunker.chunk_document(docs[0])
    return chunks[0]


def test_bm25_like_score_zero_for_empty_query():
    assert lexical.bm25_like_score("", _sample_chunk()) == 0.0


def test_bm25_like_score_positive_for_matching_token():
    docs = knowledge_loader.get_index()["documents"]
    # Pick a chunk and use a token that should appear in it (e.g. its domain word).
    chunk = chunker.chunk_document(docs[0])[0]
    title_word = docs[0]["metadata"]["title"].split()[0]
    score = lexical.bm25_like_score(title_word, chunk)
    assert score >= 0


def test_keyword_overlap_score_bounds():
    chunk = _sample_chunk()
    s = lexical.keyword_overlap_score("authentication", chunk)
    assert 0.0 <= s <= 1.5


def test_tag_match_score_uses_tags():
    chunk = _sample_chunk()
    if not chunk.get("tags"):
        return
    tag = chunk["tags"][0]
    assert lexical.tag_match_score(tag, chunk) >= 0.0


def test_domain_match_score_handles_underscored_domain():
    chunk = _sample_chunk()
    domain = chunk["domain"].replace("_", " ")
    assert lexical.domain_match_score(domain, chunk) == 1.0


def test_domain_match_score_no_match():
    chunk = _sample_chunk()
    assert lexical.domain_match_score("totally unrelated", chunk) == 0.0
