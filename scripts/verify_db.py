from papertrail.db.models import Document
from papertrail.db.session import SessionLocal

def check_saved_documents():
    db = SessionLocal()
    try:
        docs = db.query(Document).all()
        print(f"\nTotal documents found in DB: {len(docs)}")
        for doc in docs:
            print(f" - ID: {doc.id}")
            print(f" - Title: {doc.title}")
            print(f" - Filename: {doc.filename}")
            print(f" - SHA256: {doc.sha256[:12]}...")
            print(f" - Page Count: {doc.page_count}")
            print("-" * 30)
    except Exception as e:
        print(f"Error connecting to database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_saved_documents()