from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app=FastAPI(title='Usage Metering & Billing Engine')


def seed_plans():
    """Automatically seeds AI Free and Pro plans on application startup"""
    with engine.connect() as connection:
        #   CHECK AND INSERT FREE PLAN
        connection.execute(
            text(
                """INSERT INTO plans(id , name , api_call_limit , ai_token_limit , price_in_cents)
                VALUES('free' , 'free tier' , 2000 , 2000000, 0)
                ON CONFLICT(id) DO NOTHING;"""
            )
        )
        # CHECK AND INSERT PRO PLAN
        connection.execute(
            text(
                """
                INSERT INTO plans(id, name, api_call_limit, ai_token_limit, price_in_cents)
                VALUES('pro', 'PRO TIER', 50000, 50000000, 20000)
                ON CONFLICT(id) DO NOTHING;"""
            )
        )
        connection.commit()
@app.on_event("startup")
def on_startup():
    seed_plans()    
    print("Database Connected and default plans seeded successfully!")

@app.get('/')
def root():
    return {"message": "Metering and Billing Engine is running!"}