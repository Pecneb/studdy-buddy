from sqlalchemy import create_engine 
from sqlalchemy.orm import Session
from studdybuddy.db import Subject
import pandas as pd

def main():
    subjects = pd.read_excel("doc/subjects.xlsx")
    subjects = subjects.drop_duplicates(subset=['Kód'])
    engine = create_engine("sqlite:///instance/studdybuddy.db")
    with Session(engine) as session:
        for i in range(len(subjects)):
            try:
                subject = Subject(id=subjects.iloc[i, 1], name=subjects.iloc[i, 0])
                session.add(subject)
                session.flush()
            except Exception as e:
                continue
        session.commit()

if __name__ == "__main__":
    main()
        
