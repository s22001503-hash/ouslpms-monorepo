"""
📊 Query Local Classification History
======================================

This script queries the local SQLite database (job_queue.db) to view
print classification history stored by the agent.

Useful for:
- Offline access to print history
- Debugging classification results
- Analytics and reporting
- Audit trail when Firestore is unavailable

Usage:
    python scripts/query_local_history.py [options]
    
Options:
    --user USER_ID      Filter by specific user ID
    --date YYYY-MM-DD   Filter by specific date
    --limit N           Limit number of records (default: 50)
    --stats             Show daily statistics
    --export CSV_FILE   Export to CSV file
"""

import sys
import os
import sqlite3
import json
from pathlib import Path
from datetime import datetime
import argparse

# Database path
DB_PATH = r"C:\AI_Prints\job_queue.db"

def check_database():
    """Check if database exists and has data."""
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Database not found at {DB_PATH}")
        print("   The agent creates this database when it first runs.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if classification_history table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='classification_history'
        """)
        
        if not cursor.fetchone():
            print("❌ Error: classification_history table not found")
            print("   The agent needs to be restarted to create the new table.")
            conn.close()
            return False
        
        # Get record count
        cursor.execute("SELECT COUNT(*) FROM classification_history")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Database found: {DB_PATH}")
        print(f"📊 Total records: {count}")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def get_classification_history(user_id=None, date=None, limit=50):
    """Retrieve classification history from database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Access columns by name
        cursor = conn.cursor()
        
        query = """
            SELECT id, job_id, user_id, file_name, file_hash, file_size,
                   total_pages, classification, confidence, action, reason,
                   copies, timestamp, created_at
            FROM classification_history
            WHERE 1=1
        """
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if date:
            query += " AND DATE(timestamp) = ?"
            params.append(date)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
        
    except Exception as e:
        print(f"❌ Query error: {e}")
        return []

def get_daily_statistics(user_id=None, date=None):
    """Get daily statistics."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Total attempts
        query = "SELECT COUNT(*) FROM classification_history WHERE DATE(timestamp) = ?"
        params = [date]
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        cursor.execute(query, params)
        total = cursor.fetchone()[0]
        
        # By action
        query = """
            SELECT action, COUNT(*) as count
            FROM classification_history
            WHERE DATE(timestamp) = ?
        """
        params = [date]
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        query += " GROUP BY action"
        cursor.execute(query, params)
        by_action = {row[0]: row[1] for row in cursor.fetchall()}
        
        # By classification
        query = """
            SELECT classification, COUNT(*) as count
            FROM classification_history
            WHERE DATE(timestamp) = ?
        """
        params = [date]
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        query += " GROUP BY classification"
        cursor.execute(query, params)
        by_classification = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'date': date,
            'user_id': user_id or 'All users',
            'total_attempts': total,
            'allowed': by_action.get('allow', 0),
            'blocked': by_action.get('block', 0),
            'by_classification': by_classification
        }
        
    except Exception as e:
        print(f"❌ Statistics error: {e}")
        return {}

def export_to_csv(records, filename):
    """Export records to CSV file."""
    try:
        import csv
        
        if not records:
            print("⚠️ No records to export")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
        
        print(f"✅ Exported {len(records)} records to {filename}")
        
    except Exception as e:
        print(f"❌ Export error: {e}")

def display_records(records):
    """Display records in a formatted table."""
    if not records:
        print("📭 No records found")
        return
    
    print(f"\n{'='*120}")
    print(f"{'ID':<5} {'User':<8} {'File Name':<25} {'Classification':<15} {'Action':<8} {'Copies':<7} {'Timestamp':<20}")
    print(f"{'='*120}")
    
    for record in records:
        file_name = record['file_name'][:24] if len(record['file_name']) > 24 else record['file_name']
        timestamp = record['timestamp'][:19] if record['timestamp'] else 'N/A'
        
        # Color code actions
        action = record['action']
        if action == 'allow':
            action_display = f"✅ {action}"
        elif action == 'block':
            action_display = f"❌ {action}"
        else:
            action_display = f"⏳ {action}"
        
        print(f"{record['id']:<5} {record['user_id']:<8} {file_name:<25} {record['classification']:<15} {action_display:<8} {record['copies']:<7} {timestamp:<20}")
    
    print(f"{'='*120}\n")

def display_statistics(stats):
    """Display statistics in a formatted view."""
    if not stats:
        return
    
    print(f"\n📊 Daily Statistics")
    print(f"{'='*60}")
    print(f"Date: {stats['date']}")
    print(f"User: {stats['user_id']}")
    print(f"\nPrint Attempts:")
    print(f"  Total:   {stats['total_attempts']}")
    print(f"  ✅ Allowed: {stats['allowed']}")
    print(f"  ❌ Blocked: {stats['blocked']}")
    
    if stats['by_classification']:
        print(f"\nBy Classification:")
        for classification, count in stats['by_classification'].items():
            print(f"  {classification}: {count}")
    
    print(f"{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Query local classification history from agent database'
    )
    parser.add_argument('--user', help='Filter by user ID')
    parser.add_argument('--date', help='Filter by date (YYYY-MM-DD)')
    parser.add_argument('--limit', type=int, default=50, help='Limit number of records')
    parser.add_argument('--stats', action='store_true', help='Show daily statistics')
    parser.add_argument('--export', help='Export to CSV file')
    
    args = parser.parse_args()
    
    print("📊 Local Classification History Query Tool")
    print("=" * 60)
    
    # Check database
    if not check_database():
        sys.exit(1)
    
    print()
    
    # Show statistics if requested
    if args.stats:
        stats = get_daily_statistics(args.user, args.date)
        display_statistics(stats)
    
    # Query and display records
    records = get_classification_history(args.user, args.date, args.limit)
    
    if records:
        display_records(records)
        
        # Export if requested
        if args.export:
            export_to_csv(records, args.export)
    else:
        print("📭 No records found matching criteria")
    
    print(f"💡 Tips:")
    print(f"  • View user 99999's history: python {sys.argv[0]} --user 99999")
    print(f"  • View today's stats: python {sys.argv[0]} --stats")
    print(f"  • Export to CSV: python {sys.argv[0]} --export history.csv")

if __name__ == '__main__':
    main()
