"""
Text Chunking Utility for Long Documents
=========================================

Handles intelligent chunking of long documents while maintaining context.
Supports both fixed-size and semantic (section-based) chunking.

Author: OUSL Print Management System
Date: November 1, 2025
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Chunk:
    """Represents a document chunk with metadata"""
    text: str
    chunk_id: int
    total_chunks: int
    page_range: Tuple[int, int]
    word_count: int
    char_count: int
    section_title: str = None
    
class TextChunker:
    """
    Smart text chunking with multiple strategies
    """
    
    def __init__(
        self,
        chunk_size: int = 1500,  # words per chunk
        chunk_overlap: int = 200,  # words overlap between chunks
        min_chunk_size: int = 100  # minimum words in a chunk
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def should_chunk(self, text: str, threshold_words: int = 3000) -> bool:
        """
        Determine if document needs chunking
        
        Args:
            text: Full document text
            threshold_words: Minimum words to trigger chunking
        
        Returns:
            True if chunking needed, False otherwise
        """
        word_count = len(text.split())
        return word_count > threshold_words
    
    def chunk_text(
        self,
        text: str,
        strategy: str = "auto"
    ) -> List[Chunk]:
        """
        Chunk text using specified strategy
        
        Args:
            text: Full document text
            strategy: "auto", "fixed", or "semantic"
        
        Returns:
            List of Chunk objects
        """
        # Check if chunking is needed
        if not self.should_chunk(text):
            return [Chunk(
                text=text,
                chunk_id=0,
                total_chunks=1,
                page_range=(1, self._estimate_pages(text)),
                word_count=len(text.split()),
                char_count=len(text),
                section_title="Full Document"
            )]
        
        # Choose strategy
        if strategy == "auto":
            # Try semantic first, fallback to fixed
            if self._has_sections(text):
                strategy = "semantic"
            else:
                strategy = "fixed"
        
        # Apply strategy
        if strategy == "semantic":
            return self._semantic_chunking(text)
        else:
            return self._fixed_size_chunking(text)
    
    def _fixed_size_chunking(self, text: str) -> List[Chunk]:
        """
        Split text into fixed-size chunks with overlap
        """
        words = text.split()
        total_words = len(words)
        chunks = []
        
        start_idx = 0
        chunk_id = 0
        
        while start_idx < total_words:
            # Calculate end index
            end_idx = min(start_idx + self.chunk_size, total_words)
            
            # Extract chunk words
            chunk_words = words[start_idx:end_idx]
            chunk_text = " ".join(chunk_words)
            
            # Estimate page range
            start_page = self._estimate_page_number(start_idx, total_words, text)
            end_page = self._estimate_page_number(end_idx, total_words, text)
            
            # Create chunk
            chunks.append(Chunk(
                text=chunk_text,
                chunk_id=chunk_id,
                total_chunks=0,  # Will update after
                page_range=(start_page, end_page),
                word_count=len(chunk_words),
                char_count=len(chunk_text),
                section_title=f"Section {chunk_id + 1}"
            ))
            
            # Move to next chunk with overlap
            start_idx = end_idx - self.chunk_overlap
            
            # Prevent infinite loop if chunk too small
            if end_idx >= total_words:
                break
            
            chunk_id += 1
        
        # Update total_chunks for all chunks
        total_chunks = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total_chunks
        
        return chunks
    
    def _semantic_chunking(self, text: str) -> List[Chunk]:
        """
        Split text by sections/chapters while respecting size limits
        """
        # Detect section headers
        sections = self._detect_sections(text)
        
        if not sections:
            # Fallback to fixed chunking if no sections found
            return self._fixed_size_chunking(text)
        
        chunks = []
        chunk_id = 0
        
        for section_title, section_text in sections:
            section_words = len(section_text.split())
            
            # If section is small enough, keep as one chunk
            if section_words <= self.chunk_size * 1.5:
                chunks.append(Chunk(
                    text=section_text,
                    chunk_id=chunk_id,
                    total_chunks=0,
                    page_range=(1, self._estimate_pages(section_text)),
                    word_count=section_words,
                    char_count=len(section_text),
                    section_title=section_title
                ))
                chunk_id += 1
            else:
                # Section too large, split further
                sub_chunks = self._fixed_size_chunking(section_text)
                for i, sub_chunk in enumerate(sub_chunks):
                    sub_chunk.chunk_id = chunk_id
                    sub_chunk.section_title = f"{section_title} (Part {i+1})"
                    chunks.append(sub_chunk)
                    chunk_id += 1
        
        # Update total_chunks
        total_chunks = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total_chunks
        
        return chunks
    
    def _has_sections(self, text: str) -> bool:
        """Check if text has clear section markers"""
        # Common section patterns
        patterns = [
            r'^#{1,6}\s+.+$',  # Markdown headers
            r'^[A-Z][^.!?]*:',  # "Chapter 1:", "Section A:"
            r'^\d+\.\s+[A-Z]',  # "1. Introduction"
            r'^(Chapter|Section|Part)\s+\d+',  # "Chapter 1", "Section 2"
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.MULTILINE):
                return True
        
        return False
    
    def _detect_sections(self, text: str) -> List[Tuple[str, str]]:
        """
        Detect and extract sections from text
        
        Returns:
            List of (section_title, section_text) tuples
        """
        sections = []
        
        # Try different header patterns
        patterns = [
            (r'^(#{1,6})\s+(.+)$', re.MULTILINE),  # Markdown
            (r'^([A-Z][^.!?\n]{0,100}):[ \n]', re.MULTILINE),  # "Title:"
            (r'^((?:Chapter|Section|Part)\s+\d+[:\s]+[^\n]+)', re.MULTILINE),
        ]
        
        for pattern, flags in patterns:
            matches = list(re.finditer(pattern, text, flags))
            if len(matches) >= 2:  # Need at least 2 sections
                for i, match in enumerate(matches):
                    title = match.group(1).strip()
                    start = match.end()
                    end = matches[i + 1].start() if i < len(matches) - 1 else len(text)
                    section_text = text[start:end].strip()
                    
                    if section_text:  # Only add non-empty sections
                        sections.append((title, section_text))
                
                if sections:
                    return sections
        
        return []
    
    def _estimate_pages(self, text: str) -> int:
        """Estimate number of pages (250 words per page)"""
        words = len(text.split())
        return max(1, words // 250)
    
    def _estimate_page_number(
        self,
        word_index: int,
        total_words: int,
        full_text: str
    ) -> int:
        """Estimate page number for a word index"""
        total_pages = self._estimate_pages(full_text)
        page = max(1, int((word_index / total_words) * total_pages))
        return page


# Example usage and testing
if __name__ == "__main__":
    chunker = TextChunker(chunk_size=1500, chunk_overlap=200)
    
    # Test with short text
    short_text = "This is a short document with only 10 words total."
    print("Short document test:")
    print(f"Should chunk: {chunker.should_chunk(short_text)}\n")
    
    # Test with long text
    long_text = " ".join(["word"] * 5000)  # 5000 words
    print("Long document test:")
    print(f"Should chunk: {chunker.should_chunk(long_text)}")
    chunks = chunker.chunk_text(long_text, strategy="fixed")
    print(f"Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):  # Show first 3
        print(f"\nChunk {i}:")
        print(f"  Words: {chunk.word_count}")
        print(f"  Page range: {chunk.page_range}")
        print(f"  Section: {chunk.section_title}")
    
    # Test with sectioned text
    sectioned_text = """
    Chapter 1: Introduction
    This is the introduction with many words about the topic.
    """ + " ".join(["word"] * 2000) + """
    
    Chapter 2: Methodology
    This chapter describes the methodology used.
    """ + " ".join(["word"] * 2000) + """
    
    Chapter 3: Results
    Here are the results of the study.
    """ + " ".join(["word"] * 2000)
    
    print("\n\nSectioned document test:")
    chunks = chunker.chunk_text(sectioned_text, strategy="semantic")
    print(f"Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i}:")
        print(f"  Section: {chunk.section_title}")
        print(f"  Words: {chunk.word_count}")
        print(f"  Page range: {chunk.page_range}")
