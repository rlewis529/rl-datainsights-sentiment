import sqlite3
from datetime import datetime, timedelta

def main():
    print("🧹 News Article Deletion Tool")
    print("Choose deletion mode:")
    print("1. Delete articles OLDER than X days")
    print("2. Delete articles NEWER than X days")
    print("3. DELETE ALL articles")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice not in {"1", "2", "3"}:
        print("❌ Invalid choice. Exiting.")
        return

    comparison = None
    date_cutoff_str = None

    if choice in {"1", "2"}:
        try:
            days = int(input("Enter number of days (X): ").strip())
        except ValueError:
            print("❌ Invalid number. Exiting.")
            return

        date_cutoff = datetime.utcnow() - timedelta(days=days)
        date_cutoff_str = date_cutoff.isoformat()
        comparison = "<" if choice == "1" else ">"

        print(f"\n⚠️ This will delete all articles where published_at {comparison} '{date_cutoff_str}'")
    else:
        print("\n⚠️ This will DELETE ALL records in the ArticleEntitySentiment table!")

    confirm = input("Are you sure? Type 'yes' to proceed: ").strip().lower()
    if confirm != "yes":
        print("❎ Deletion cancelled.")
        return

    # Connect and delete
    conn = sqlite3.connect("news_sentiment.db")
    cursor = conn.cursor()

    if choice == "3":
        cursor.execute("DELETE FROM ArticleEntitySentiment")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='ArticleEntitySentiment'")
    else:
        cursor.execute(f"""
            DELETE FROM ArticleEntitySentiment
            WHERE published_at {comparison} ?
        """, (date_cutoff_str,))

    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    print(f"✅ Deleted {deleted} article(s) from ArticleEntitySentiment.")

if __name__ == "__main__":
    main()
