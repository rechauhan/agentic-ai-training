# Lab 6: Persistent Storage - Long-Term Memory

## 🎯 Learning Objectives

By the end of this lab, you will:
- Understand different storage backends for agent state
- Learn how to use databases for persistent storage
- Implement cloud storage solutions
- Build scalable state management systems
- Handle data migration and versioning

## 📖 Core Concepts

### What is Persistent Storage?

**Analogy**: Think of persistent storage like a **hotel's customer database**:

- **In-Memory State** (Lab 5): Notepad that gets thrown away when shift ends
- **File Storage**: Filing cabinet in the office
- **Database Storage**: Central computer system accessible by all staff
- **Cloud Storage**: Corporate database accessible from any hotel location

### Storage Options Comparison

| Storage Type | Speed | Scalability | Durability | Cost |
|--------------|-------|-------------|------------|------|
| In-Memory | ⚡⚡⚡ | ❌ | ❌ | Free |
| File System | ⚡⚡ | ⚠️ | ✅ | Free |
| SQLite | ⚡⚡ | ⚠️ | ✅ | Free |
| PostgreSQL | ⚡ | ✅ | ✅✅ | $ |
| Redis | ⚡⚡⚡ | ✅ | ✅ | $$ |
| Cloud (S3/GCS) | ⚡ | ✅✅ | ✅✅✅ | $ |


### Storage Architecture

```mermaid
graph TB
    A[Agent] --> B{Storage Layer}
    B --> C[SQLite]
    B --> D[PostgreSQL]
    B --> E[Redis]
    B --> F[Cloud Storage]
    
    C --> G[Local File]
    D --> H[Database Server]
    E --> I[In-Memory Cache]
    F --> J[S3/GCS/Azure]
    
    style B fill:#4285f4,color:#fff
    style C fill:#90EE90
    style D fill:#87CEEB
    style E fill:#FFB6C1
    style F fill:#DDA0DD
```

## 🏨 Travel Agent Use Case: TravelMate Persistent

We're building **TravelMate Persistent** with enterprise-grade storage:

1. **User Profiles**: Stored in PostgreSQL for querying
2. **Session Cache**: Redis for fast access
3. **Search History**: Time-series database
4. **Documents**: Cloud storage (S3) for receipts, itineraries
5. **Analytics**: Data warehouse for insights

### Real-World Scenario

```
User Sarah logs in from phone:
- Profile loaded from PostgreSQL
- Recent searches from Redis cache
- Past bookings from S3

User Sarah switches to laptop:
- Same profile, same data
- Seamless experience across devices

Admin runs analytics:
- Query all users' travel patterns
- Generate insights from aggregated data
- No impact on user experience
```

## 💻 Code Walkthrough

### Step 1: SQLite Storage (Simple Start)

```python
import sqlite3
import json
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SQLiteStorage:
    """Simple SQLite storage for agent state."""
    
    def __init__(self, db_path: str = "travel_agent.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                home_city TEXT,
                created_at TIMESTAMP,
                last_active TIMESTAMP
            )
        """)
        
        # Preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                user_id TEXT PRIMARY KEY,
                budget_level TEXT,
                travel_style TEXT,
                dietary_restrictions TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Search history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                search_type TEXT,
                origin TEXT,
                destination TEXT,
                search_date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        conn.commit()
        conn.close()

    
    def save_user(self, user_id: str, name: str = None, email: str = None, 
                  home_city: str = None):
        """Save or update user profile."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (user_id, name, email, home_city, created_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name = COALESCE(?, name),
                email = COALESCE(?, email),
                home_city = COALESCE(?, home_city),
                last_active = ?
        """, (user_id, name, email, home_city, datetime.now(), datetime.now(),
              name, email, home_city, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user profile."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, name, email, home_city, created_at, last_active
            FROM users WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "home_city": row[3],
                "created_at": row[4],
                "last_active": row[5]
            }
        return None
    
    def add_search(self, user_id: str, search_type: str, 
                   origin: str = None, destination: str = None):
        """Add search to history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO search_history (user_id, search_type, origin, destination, search_date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, search_type, origin, destination, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_search_history(self, user_id: str, limit: int = 10) -> list:
        """Get user's search history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT search_type, origin, destination, search_date
            FROM search_history
            WHERE user_id = ?
            ORDER BY search_date DESC
            LIMIT ?
        """, (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "search_type": row[0],
                "origin": row[1],
                "destination": row[2],
                "search_date": row[3]
            }
            for row in rows
        ]


# Usage
storage = SQLiteStorage()

# Save user
storage.save_user("user_123", name="Sarah", home_city="Boston")

# Get user
user = storage.get_user("user_123")
print(f"User: {user}")

# Add search
storage.add_search("user_123", "flight", "Boston", "Paris")

# Get history
history = storage.get_search_history("user_123")
print(f"History: {history}")
```

### Step 2: PostgreSQL Storage (Production Scale)

```python
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

class PostgreSQLStorage:
    """PostgreSQL storage for production use."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = psycopg2.connect(self.connection_string)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table with JSONB for flexible data
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(255) PRIMARY KEY,
                    profile JSONB NOT NULL,
                    preferences JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Search history with indexing
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) REFERENCES users(user_id),
                    search_data JSONB NOT NULL,
                    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_id 
                ON search_history(user_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_search_date 
                ON search_history(search_date DESC)
            """)
    
    def save_user(self, user_id: str, profile: dict, preferences: dict = None):
        """Save user with JSONB data."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (user_id, profile, preferences, updated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id) DO UPDATE SET
                    profile = EXCLUDED.profile,
                    preferences = EXCLUDED.preferences,
                    updated_at = CURRENT_TIMESTAMP
            """, (user_id, json.dumps(profile), json.dumps(preferences)))
    
    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user with all data."""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT user_id, profile, preferences, created_at, updated_at
                FROM users WHERE user_id = %s
            """, (user_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def add_search(self, user_id: str, search_data: dict):
        """Add search with full data as JSONB."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO search_history (user_id, search_data)
                VALUES (%s, %s)
            """, (user_id, json.dumps(search_data)))
    
    def get_popular_destinations(self, limit: int = 10) -> list:
        """Get most popular destinations across all users."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    search_data->>'destination' as destination,
                    COUNT(*) as search_count
                FROM search_history
                WHERE search_data->>'destination' IS NOT NULL
                GROUP BY search_data->>'destination'
                ORDER BY search_count DESC
                LIMIT %s
            """, (limit,))
            
            return [{"destination": row[0], "count": row[1]} 
                    for row in cursor.fetchall()]


# Usage
storage = PostgreSQLStorage(
    "postgresql://user:password@localhost:5432/travel_agent"
)

# Save user with complex data
storage.save_user(
    "user_123",
    profile={"name": "Sarah", "email": "sarah@example.com"},
    preferences={"budget": "medium", "dietary": ["vegetarian"]}
)

# Analytics query
popular = storage.get_popular_destinations()
print(f"Popular destinations: {popular}")
```

### Step 3: Redis Cache Layer

```python
import redis
import json
from typing import Optional

class RedisCache:
    """Redis cache for fast access to frequently used data."""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    
    def cache_user_session(self, user_id: str, session_data: dict, ttl: int = 3600):
        """Cache user session data (expires after ttl seconds)."""
        key = f"session:{user_id}"
        self.redis.setex(key, ttl, json.dumps(session_data))
    
    def get_user_session(self, user_id: str) -> Optional[dict]:
        """Get cached session data."""
        key = f"session:{user_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def cache_search_results(self, search_key: str, results: list, ttl: int = 300):
        """Cache search results (5 minutes)."""
        key = f"search:{search_key}"
        self.redis.setex(key, ttl, json.dumps(results))
    
    def get_cached_search(self, search_key: str) -> Optional[list]:
        """Get cached search results."""
        key = f"search:{search_key}"
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def increment_search_counter(self, destination: str):
        """Increment search counter for analytics."""
        key = f"counter:destination:{destination}"
        self.redis.incr(key)
    
    def get_trending_destinations(self, limit: int = 10) -> list:
        """Get trending destinations from counters."""
        keys = self.redis.keys("counter:destination:*")
        destinations = []
        
        for key in keys:
            destination = key.split(":")[-1]
            count = int(self.redis.get(key))
            destinations.append({"destination": destination, "count": count})
        
        return sorted(destinations, key=lambda x: x["count"], reverse=True)[:limit]


# Usage
cache = RedisCache()

# Cache session
cache.cache_user_session("user_123", {
    "name": "Sarah",
    "preferences": {"budget": "medium"}
})

# Get from cache (fast!)
session = cache.get_user_session("user_123")

# Cache search results
cache.cache_search_results("NYC-Paris-2024-03-15", [
    {"airline": "Air France", "price": 650},
    {"airline": "Delta", "price": 720}
])

# Track trending
cache.increment_search_counter("Paris")
cache.increment_search_counter("Tokyo")
trending = cache.get_trending_destinations()
```

### Step 4: Hybrid Storage Strategy

```python
class HybridStorageAgent:
    """Agent with hybrid storage strategy."""
    
    def __init__(self, db_storage, cache):
        self.db = db_storage  # PostgreSQL or SQLite
        self.cache = cache    # Redis
    
    def get_user_profile(self, user_id: str) -> dict:
        """Get user profile with cache-aside pattern."""
        # Try cache first
        cached = self.cache.get_user_session(user_id)
        if cached:
            print("[Cache hit]")
            return cached
        
        # Cache miss - get from database
        print("[Cache miss - loading from DB]")
        user = self.db.get_user(user_id)
        
        if user:
            # Store in cache for next time
            self.cache.cache_user_session(user_id, user)
        
        return user
    
    def search_flights(self, origin: str, destination: str, date: str) -> list:
        """Search with result caching."""
        search_key = f"{origin}-{destination}-{date}"
        
        # Check cache
        cached_results = self.cache.get_cached_search(search_key)
        if cached_results:
            print("[Using cached results]")
            return cached_results
        
        # Perform actual search (expensive operation)
        print("[Performing new search]")
        results = self._perform_flight_search(origin, destination, date)
        
        # Cache results
        self.cache.cache_search_results(search_key, results)
        
        # Track analytics
        self.cache.increment_search_counter(destination)
        
        return results
    
    def _perform_flight_search(self, origin: str, destination: str, date: str) -> list:
        """Actual flight search (mock)."""
        return [
            {"airline": "Airline A", "price": 650},
            {"airline": "Airline B", "price": 720}
        ]


# Usage
db = PostgreSQLStorage("postgresql://...")
cache = RedisCache()
agent = HybridStorageAgent(db, cache)

# First call - cache miss
profile1 = agent.get_user_profile("user_123")

# Second call - cache hit (much faster!)
profile2 = agent.get_user_profile("user_123")

# Search with caching
flights1 = agent.search_flights("NYC", "Paris", "2024-03-15")
flights2 = agent.search_flights("NYC", "Paris", "2024-03-15")  # Cached!
```


### Step 5: Cloud Storage for Documents

```python
import boto3
from datetime import datetime
import io

class S3DocumentStorage:
    """S3 storage for documents and files."""
    
    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        self.s3 = boto3.client('s3', region_name=region)
        self.bucket = bucket_name
    
    def upload_itinerary(self, user_id: str, itinerary_data: dict) -> str:
        """Upload itinerary as JSON to S3."""
        key = f"itineraries/{user_id}/{datetime.now().isoformat()}.json"
        
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=json.dumps(itinerary_data, indent=2),
            ContentType='application/json',
            Metadata={
                'user_id': user_id,
                'created_at': datetime.now().isoformat()
            }
        )
        
        return key
    
    def get_itinerary(self, key: str) -> dict:
        """Download itinerary from S3."""
        response = self.s3.get_object(Bucket=self.bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        return json.loads(data)
    
    def list_user_itineraries(self, user_id: str) -> list:
        """List all itineraries for a user."""
        prefix = f"itineraries/{user_id}/"
        
        response = self.s3.list_objects_v2(
            Bucket=self.bucket,
            Prefix=prefix
        )
        
        if 'Contents' not in response:
            return []
        
        return [
            {
                'key': obj['Key'],
                'size': obj['Size'],
                'last_modified': obj['LastModified']
            }
            for obj in response['Contents']
        ]
    
    def generate_presigned_url(self, key: str, expiration: int = 3600) -> str:
        """Generate temporary download URL."""
        url = self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=expiration
        )
        return url


# Usage
s3_storage = S3DocumentStorage(bucket_name="travel-agent-docs")

# Upload itinerary
itinerary = {
    "trip_name": "Paris Adventure",
    "days": 7,
    "activities": [...]
}
key = s3_storage.upload_itinerary("user_123", itinerary)

# List user's itineraries
itineraries = s3_storage.list_user_itineraries("user_123")

# Generate shareable link
url = s3_storage.generate_presigned_url(key)
print(f"Share this link: {url}")
```

## 🔄 Complete Example: Production Storage System

```python
from google import genai
import sqlite3
import redis
import json
from typing import Optional

class ProductionTravelAgent:
    """Production-ready agent with multi-tier storage."""
    
    def __init__(self, api_key: str, db_path: str = "travel.db"):
        self.client = genai.Client(api_key=api_key)
        self.db = SQLiteStorage(db_path)
        self.cache = RedisCache()
        
    def chat(self, user_id: str, message: str) -> str:
        """Chat with persistent storage."""
        # Load user context from storage
        user = self._get_user_with_cache(user_id)
        
        # Build context
        context = self._build_context(user)
        
        # Create agent
        agent = self.client.agentic.create_agent(
            model="gemini-2.0-flash-exp",
            system_instruction=context
        )
        
        # Get or create session
        session = self._get_session(user_id, agent)
        
        # Send message
        response = session.send_message(message)
        
        # Update storage
        self._update_user_activity(user_id)
        
        return response.text
    
    def _get_user_with_cache(self, user_id: str) -> dict:
        """Get user with cache-aside pattern."""
        # Try cache
        cached = self.cache.get_user_session(user_id)
        if cached:
            return cached
        
        # Load from DB
        user = self.db.get_user(user_id)
        if not user:
            # Create new user
            self.db.save_user(user_id)
            user = self.db.get_user(user_id)
        
        # Cache it
        self.cache.cache_user_session(user_id, user)
        
        return user
    
    def _build_context(self, user: dict) -> str:
        """Build context from user data."""
        context = "You are TravelMate Persistent, a travel assistant.\n"
        
        if user.get('name'):
            context += f"User's name: {user['name']}\n"
        
        # Add search history
        history = self.db.get_search_history(user['user_id'], limit=5)
        if history:
            context += "\nRecent searches:\n"
            for search in history:
                context += f"- {search['search_type']}: {search['origin']} → {search['destination']}\n"
        
        return context
    
    def _get_session(self, user_id: str, agent):
        """Get or create ADK session."""
        if not hasattr(self, '_sessions'):
            self._sessions = {}
        
        if user_id not in self._sessions:
            self._sessions[user_id] = self.client.agentic.create_session(agent=agent)
        
        return self._sessions[user_id]
    
    def _update_user_activity(self, user_id: str):
        """Update last activity timestamp."""
        self.db.save_user(user_id)
        # Invalidate cache
        self.cache.redis.delete(f"session:{user_id}")


# Usage
agent = ProductionTravelAgent(api_key='your_api_key_here')

# Multiple users, persistent across restarts
response1 = agent.chat("user_123", "Find flights to Paris")
response2 = agent.chat("user_456", "Show me hotels in Tokyo")

# Restart application...
agent = ProductionTravelAgent(api_key='your_api_key_here')

# Data persists!
response3 = agent.chat("user_123", "What about hotels?")
# Agent remembers previous Paris search
```

## 🎨 Storage Architecture Diagram

```mermaid
graph TB
    A[User Request] --> B[Agent]
    B --> C{Check Cache}
    C -->|Hit| D[Return Cached Data]
    C -->|Miss| E[Query Database]
    E --> F[PostgreSQL]
    F --> G[Update Cache]
    G --> D
    
    B --> H[Save State]
    H --> I[Write to DB]
    H --> J[Invalidate Cache]
    
    B --> K[Store Documents]
    K --> L[S3/Cloud Storage]
    
    style C fill:#4285f4,color:#fff
    style F fill:#34a853,color:#fff
    style L fill:#fbbc04
```

## 🧪 Hands-On Exercises

### Exercise 1: Add Data Migration

```python
class DatabaseMigration:
    """Handle database schema migrations."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_schema_version(self) -> int:
        """Get current schema version."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT version FROM schema_version")
            version = cursor.fetchone()[0]
        except sqlite3.OperationalError:
            version = 0
        
        conn.close()
        return version
    
    def migrate_to_v2(self):
        """Migrate from v1 to v2."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add new column
        cursor.execute("""
            ALTER TABLE users ADD COLUMN phone TEXT
        """)
        
        # Update version
        cursor.execute("""
            UPDATE schema_version SET version = 2
        """)
        
        conn.commit()
        conn.close()
    
    def run_migrations(self):
        """Run all pending migrations."""
        current_version = self.get_schema_version()
        
        if current_version < 2:
            print("Migrating to v2...")
            self.migrate_to_v2()
```

### Exercise 2: Implement Backup System

```python
import shutil
from datetime import datetime

class BackupManager:
    """Manage database backups."""
    
    def __init__(self, db_path: str, backup_dir: str = "./backups"):
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self) -> str:
        """Create database backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}.db"
        
        shutil.copy2(self.db_path, backup_path)
        
        print(f"Backup created: {backup_path}")
        return str(backup_path)
    
    def restore_backup(self, backup_path: str):
        """Restore from backup."""
        shutil.copy2(backup_path, self.db_path)
        print(f"Restored from: {backup_path}")
    
    def list_backups(self) -> list:
        """List all backups."""
        return sorted(self.backup_dir.glob("backup_*.db"), reverse=True)
    
    def cleanup_old_backups(self, keep_count: int = 5):
        """Keep only recent backups."""
        backups = self.list_backups()
        
        for backup in backups[keep_count:]:
            backup.unlink()
            print(f"Deleted old backup: {backup}")
```

### Exercise 3: Add Analytics Queries

```python
class AnalyticsQueries:
    """Analytics queries for insights."""
    
    def __init__(self, storage):
        self.storage = storage
    
    def get_user_stats(self) -> dict:
        """Get overall user statistics."""
        conn = sqlite3.connect(self.storage.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE last_active > datetime('now', '-7 days')
        """)
        active_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM search_history")
        total_searches = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_users": total_users,
            "active_users_7d": active_users,
            "total_searches": total_searches,
            "avg_searches_per_user": total_searches / total_users if total_users > 0 else 0
        }
    
    def get_popular_routes(self, limit: int = 10) -> list:
        """Get most popular travel routes."""
        conn = sqlite3.connect(self.storage.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT origin, destination, COUNT(*) as count
            FROM search_history
            WHERE origin IS NOT NULL AND destination IS NOT NULL
            GROUP BY origin, destination
            ORDER BY count DESC
            LIMIT ?
        """, (limit,))
        
        routes = [
            {"origin": row[0], "destination": row[1], "searches": row[2]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return routes
```

## 🐛 Common Issues and Solutions

### Issue 1: Database Locks

**Problem**: SQLite database locked error

**Solution**: Use connection pooling or WAL mode
```python
conn = sqlite3.connect(db_path, check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL")
```

### Issue 2: Cache Invalidation

**Problem**: Stale data in cache

**Solution**: Implement cache invalidation strategy
```python
def update_user(self, user_id: str, data: dict):
    # Update database
    self.db.save_user(user_id, **data)
    
    # Invalidate cache
    self.cache.redis.delete(f"session:{user_id}")
```

### Issue 3: Connection Pool Exhaustion

**Problem**: Too many database connections

**Solution**: Use connection pooling
```python
from psycopg2 import pool

class PooledPostgreSQLStorage:
    def __init__(self, connection_string: str, min_conn: int = 1, max_conn: int = 10):
        self.pool = pool.ThreadedConnectionPool(
            min_conn, max_conn, connection_string
        )
    
    @contextmanager
    def get_connection(self):
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        finally:
            self.pool.putconn(conn)
```

## 🎓 Key Takeaways

✅ **Persistent storage** enables data to survive application restarts

✅ **Multiple storage tiers** optimize for different use cases

✅ **Caching** dramatically improves performance

✅ **Database indexing** is crucial for query performance

✅ **Backup strategies** protect against data loss

✅ **Migration systems** handle schema evolution

## 🔗 Connection to Next Lab

In Lab 7, we'll build **Multi-Agent Systems** where specialized agents work together. With persistent storage, we can:
- Coordinate multiple agents with shared state
- Track agent-to-agent communications
- Store specialized agent knowledge
- Implement agent handoffs with context

## 📚 Additional Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [PostgreSQL Best Practices](https://www.postgresql.org/docs/)
- [Redis Caching Patterns](https://redis.io/docs/manual/patterns/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)

## ✅ Self-Check Quiz

1. What's the difference between cache and persistent storage?
2. When should you use SQLite vs PostgreSQL?
3. What is the cache-aside pattern?
4. How do you handle database migrations?
5. Why is connection pooling important?

---

← [Lab 5: Sessions and State](./Lab5_Guide_Sessions_State.md) | **Next**: [Lab 7: Multi-Agent](./Lab7_Guide_Multi_Agent.md) →
