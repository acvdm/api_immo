from app import create_app
from app.common.database import db
print("📦 Importing in run.py")
print(f"📦 db object id: {id(db)}") 

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crée toutes les tables
        db.create_all()
        print("✓ Database tables created!")

    app.run(host='0.0.0.0', port=5000, debug=True)