"""
🗄️ SQLite REST API Server for Agent Local Database
====================================================

Exposes the agent's local classification history via HTTP REST API.

This allows admin dashboards and monitoring tools to remotely access
print classification data stored in the agent's SQLite database.

Features:
- Classification history queries (with pagination)
- Daily statistics per user
- Search functionality
- Summary analytics
- API key authentication
- CORS support for web dashboards

Usage:
    python sqlite_api_server.py

API Endpoints:
    GET  /                           - Health check
    GET  /api/classification-history - Get classification records
    GET  /api/daily-stats            - Get daily statistics
    GET  /api/search                 - Search history
    GET  /api/stats/summary          - Get overall statistics
    GET  /api/users                  - List unique users

Author: OUSL Print Management System
Date: October 29, 2025
"""

import os
import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# ==================== CONFIGURATION ====================

# Database path (same as agent)
QUEUE_DB = r"C:\AI_Prints\job_queue.db"

# API Key for authentication (change this in production!)
API_KEY = "ousl-sqlite-api-key-2025"  # Should be in environment variable in production

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== MODELS ====================

class ClassificationRecord(BaseModel):
    """Single classification record from database."""
    id: int
    job_id: Optional[str] = None
    user_id: Optional[str] = None
    file_name: Optional[str] = None
    file_hash: Optional[str] = None
    file_size: Optional[int] = None
    total_pages: Optional[int] = None
    classification: Optional[str] = None
    confidence: Optional[float] = None
    action: Optional[str] = None
    reason: Optional[str] = None
    copies: Optional[int] = None
    timestamp: Optional[str] = None
    created_at: Optional[str] = None
    synced_to_firestore: Optional[int] = None

class DailyStats(BaseModel):
    """Daily statistics for a user."""
    user_id: str
    date: str
    total_attempts: int
    allowed: int
    blocked: int
    by_classification: Dict[str, int]

class SummaryStats(BaseModel):
    """Overall database statistics."""
    total_records: int
    unique_users: int
    by_action: Dict[str, int]
    by_classification: Dict[str, int]

class HealthCheck(BaseModel):
    """API health check response."""
    service: str
    status: str
    database: str
    database_exists: bool
    total_records: int

class UserInfo(BaseModel):
    """User information from database."""
    user_id: str
    total_prints: int
    allowed: int
    blocked: int
    last_print: Optional[str]

# ==================== AUTHENTICATION ====================

async def verify_api_key(x_api_key: str = Header(..., description="API key for authentication")):
    """
    Verify API key from request header.
    
    Usage in request:
        curl -H "X-API-Key: your-api-key-here" http://localhost:8001/api/...
    """
    if x_api_key != API_KEY:
        logger.warning(f"Invalid API key attempt: {x_api_key[:10]}...")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key. Include valid X-API-Key header."
        )
    return x_api_key

# ==================== DATABASE HELPERS ====================

def check_database_exists() -> bool:
    """Check if database file exists."""
    return os.path.exists(QUEUE_DB)

def get_db_connection():
    """Get SQLite database connection."""
    if not check_database_exists():
        raise HTTPException(
            status_code=503,
            detail=f"Database not found at {QUEUE_DB}. Agent may not be running."
        )
    
    try:
        conn = sqlite3.connect(QUEUE_DB)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_record_count() -> int:
    """Get total number of records in database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM classification_history')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

# ==================== FASTAPI APP ====================

app = FastAPI(
    title="Agent SQLite API",
    description="REST API for accessing agent's local classification history",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for admin dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ENDPOINTS ====================

@app.get("/", response_model=HealthCheck)
async def root():
    """
    API health check endpoint.
    
    Returns service status and database information.
    No authentication required.
    """
    db_exists = check_database_exists()
    total_records = get_record_count() if db_exists else 0
    
    return HealthCheck(
        service="Agent SQLite API",
        status="running",
        database=QUEUE_DB,
        database_exists=db_exists,
        total_records=total_records
    )

@app.get("/api/classification-history", response_model=List[ClassificationRecord])
async def get_classification_history(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    classification: Optional[str] = Query(None, description="Filter by classification type"),
    action: Optional[str] = Query(None, description="Filter by action (allow/block)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Skip N records (for pagination)"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get classification history from local SQLite database.
    
    **Authentication:** Requires X-API-Key header
    
    **Examples:**
    - All records: `GET /api/classification-history`
    - User specific: `GET /api/classification-history?user_id=99999`
    - Paginated: `GET /api/classification-history?limit=50&offset=100`
    - Filtered: `GET /api/classification-history?classification=office&action=allow`
    
    **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build query dynamically based on filters
        query = '''
            SELECT id, job_id, user_id, file_name, file_hash, file_size,
                   total_pages, classification, confidence, action, reason, 
                   copies, timestamp, created_at, synced_to_firestore
            FROM classification_history
            WHERE 1=1
        '''
        params = []
        
        if user_id:
            query += ' AND user_id = ?'
            params.append(user_id)
        
        if classification:
            query += ' AND classification = ?'
            params.append(classification)
        
        if action:
            query += ' AND action = ?'
            params.append(action)
        
        query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts
        records = [dict(row) for row in rows]
        
        logger.info(f"Retrieved {len(records)} records (filters: user_id={user_id}, classification={classification}, action={action})")
        
        return records
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching classification history: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/daily-stats", response_model=DailyStats)
async def get_daily_stats(
    user_id: str = Query(..., description="User ID"),
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get daily statistics for a specific user.
    
    **Authentication:** Requires X-API-Key header
    
    **Example:**
    ```
    GET /api/daily-stats?user_id=99999&date=2025-10-29
    ```
    
    **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get counts by action
        cursor.execute('''
            SELECT action, COUNT(*) as count
            FROM classification_history
            WHERE user_id = ?
            AND DATE(timestamp) = ?
            GROUP BY action
        ''', (user_id, date))
        
        action_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Get counts by classification
        cursor.execute('''
            SELECT classification, COUNT(*) as count
            FROM classification_history
            WHERE user_id = ?
            AND DATE(timestamp) = ?
            GROUP BY classification
        ''', (user_id, date))
        
        classification_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        stats = DailyStats(
            user_id=user_id,
            date=date,
            total_attempts=sum(action_counts.values()),
            allowed=action_counts.get('allow', 0),
            blocked=action_counts.get('block', 0),
            by_classification=classification_counts
        )
        
        logger.info(f"Retrieved daily stats for user {user_id} on {date}")
        
        return stats
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching daily stats: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/search")
async def search_history(
    query: str = Query(..., min_length=2, description="Search term (min 2 characters)"),
    field: str = Query("file_name", description="Field to search (file_name, classification, user_id, action)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum results"),
    api_key: str = Depends(verify_api_key)
):
    """
    Search classification history by keyword.
    
    **Authentication:** Requires X-API-Key header
    
    **Example:**
    ```
    GET /api/search?query=report&field=file_name
    ```
    
    **Searchable Fields:**
    - `file_name` - Search by filename
    - `classification` - Search by classification type
    - `user_id` - Search by user ID
    - `action` - Search by action (allow/block)
    
    **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
    """
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Validate field
        allowed_fields = ['file_name', 'classification', 'user_id', 'action', 'reason']
        if field not in allowed_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid field. Allowed: {', '.join(allowed_fields)}"
            )
        
        # Search with LIKE (case-insensitive)
        cursor.execute(f'''
            SELECT id, job_id, user_id, file_name, file_hash,
                   classification, confidence, action, reason, 
                   copies, timestamp, created_at
            FROM classification_history
            WHERE {field} LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        records = [dict(row) for row in rows]
        
        logger.info(f"Search query '{query}' in field '{field}' returned {len(records)} results")
        
        return {
            'query': query,
            'field': field,
            'count': len(records),
            'results': records
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching history: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/stats/summary", response_model=SummaryStats)
async def get_summary_stats(api_key: str = Depends(verify_api_key)):
    """
    Get overall database statistics.
    
    **Authentication:** Requires X-API-Key header
    
    **Example:**
    ```
    GET /api/stats/summary
    ```
    
    Returns total records, unique users, and breakdowns by action/classification.
    
    **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total records
        cursor.execute('SELECT COUNT(*) FROM classification_history')
        total_records = cursor.fetchone()[0]
        
        # By action
        cursor.execute('''
            SELECT action, COUNT(*) as count
            FROM classification_history
            GROUP BY action
        ''')
        by_action = {row[0]: row[1] for row in cursor.fetchall()}
        
        # By classification
        cursor.execute('''
            SELECT classification, COUNT(*) as count
            FROM classification_history
            GROUP BY classification
        ''')
        by_classification = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Unique users
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM classification_history')
        unique_users = cursor.fetchone()[0]
        
        conn.close()
        
        stats = SummaryStats(
            total_records=total_records,
            unique_users=unique_users,
            by_action=by_action,
            by_classification=by_classification
        )
        
        logger.info("Retrieved summary statistics")
        
        return stats
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching summary stats: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/users", response_model=List[UserInfo])
async def get_users(
    limit: int = Query(100, ge=1, le=1000, description="Maximum users to return"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get list of unique users with their statistics.
    
    **Authentication:** Requires X-API-Key header
    
    **Example:**
    ```
    GET /api/users?limit=50
    ```
    
    **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                user_id,
                COUNT(*) as total_prints,
                SUM(CASE WHEN action = 'allow' THEN 1 ELSE 0 END) as allowed,
                SUM(CASE WHEN action = 'block' THEN 1 ELSE 0 END) as blocked,
                MAX(timestamp) as last_print
            FROM classification_history
            WHERE user_id IS NOT NULL
            GROUP BY user_id
            ORDER BY total_prints DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        users = [
            UserInfo(
                user_id=row[0],
                total_prints=row[1],
                allowed=row[2],
                blocked=row[3],
                last_print=row[4]
            )
            for row in rows
        ]
        
        logger.info(f"Retrieved {len(users)} users")
        
        return users
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ==================== MAIN ====================

def main():
    """Run the SQLite API server."""
    print("=" * 70)
    print("🗄️  Agent SQLite REST API Server")
    print("=" * 70)
    print(f"Database: {QUEUE_DB}")
    print(f"Database exists: {check_database_exists()}")
    print(f"Server: http://localhost:8001")
    print(f"API Docs: http://localhost:8001/docs")
    print(f"API Key: {API_KEY}")
    print("=" * 70)
    print("\n📝 Available Endpoints:")
    print("  GET  /                           - Health check (no auth)")
    print("  GET  /api/classification-history - Get classification records")
    print("  GET  /api/daily-stats            - Get daily statistics")
    print("  GET  /api/search                 - Search history")
    print("  GET  /api/stats/summary          - Get overall statistics")
    print("  GET  /api/users                  - List unique users")
    print("\n🔑 Authentication:")
    print("  Include header: X-API-Key: " + API_KEY)
    print("\n💡 Example:")
    print(f'  curl -H "X-API-Key: {API_KEY}" http://localhost:8001/api/stats/summary')
    print("=" * 70)
    print()
    
    # Check database before starting
    if not check_database_exists():
        logger.warning(f"⚠️  Database not found at {QUEUE_DB}")
        logger.warning("   The agent will create it when it runs.")
        logger.warning("   API will return 503 errors until database exists.")
        print()
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces
        port=8001,
        log_level="info"
    )

if __name__ == "__main__":
    main()
