import json
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

# Ensure the database tables exist
models.Base.metadata.create_all(bind=engine)

def seed_data():

    db: Session = SessionLocal()
    
    try:

        file_path = os.path.join(os.path.dirname(__file__), "data", "pilot_villages.json")
        
        if not os.path.exists(file_path):
            print(f"❌ File not found at {file_path}")
            return
            
        with open(file_path, "r") as file:
            villages = json.load(file)
            

        for v in villages:

            existing = db.query(models.LocalMarketData).filter(
                models.LocalMarketData.village_name == v["village_name"]
            ).first()
            
            if not existing:
                new_market_data = models.LocalMarketData(
                    village_name=v["village_name"],
                    population=v["population"],
                    nearby_market=v["nearby_weekly_market_haat"]
                )
                db.add(new_market_data)
                print(f"✅ Inserted data for {v['village_name']}")
            else:
                print(f"⚠️ Data for {v['village_name']} already exists. Skipping.")
                

        db.commit()
        print("🎉 Database seeding complete!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()