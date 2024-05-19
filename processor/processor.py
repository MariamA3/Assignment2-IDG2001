import time
import redis
import json
from backend.config.databaseConnect import get_db_connection

# Connect to Redis
redis_host = 'redis'
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)

# Get database connection
db_connection = get_db_connection()


def process_likes():
    while True:
        # Check Redis for pending likes
        pending_likes = redis_client.lrange('pending_likes', 0, -1)
        if pending_likes:
            # Process likes in batches
            batch_size = 100
            for i in range(0, len(pending_likes), batch_size):
                batch = pending_likes[i:i+batch_size]
                process_likes_batch(batch)

            # Remove processed likes from Redis
            redis_client.ltrim('pending_likes', len(pending_likes), -1)

        # Wait for some time before checking again
        time.sleep(60)

def process_likes_batch(batch):
    # Example: Update database with likes
    for like in batch:
        process_like(json.loads(like)) 

def process_like(like):
    # Process individual like
    if db_connection:
        try:
            with db_connection.cursor() as cursor:
                # Example: Insert like into database
                sql = "INSERT INTO likes (user_id, post_id) VALUES (%s, %s)"
                cursor.execute(sql, (like['user_id'], like['post_id']))
                db_connection.commit()
                print("Like inserted successfully!")
        except Exception as e:
            print(f"Error inserting like into the database: {e}")

if __name__ == '__main__':
    process_likes()
