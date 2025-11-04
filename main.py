from utils import *
from datetime import date
import traceback
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

    
app = FastAPI(title="Grade Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_grade_overview():
    try:
        edupage = init_edupage()
        if not login_edupage(edupage):
            raise HTTPException(status_code=401, detail="Couldn't login to edupage, check your credentials")
        
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        student_id = edupage.get_user_id()
        
        print("Načítavam známky...")
        grades = edupage.get_grades()
        print(f"✓ Načítaných {len(grades)} známok\n")
        
        print("Načítavam predmety...")
        subjects = get_my_subjects_from_timetable(edupage)
        print(f"✓ Načítaných {len(subjects)} predmetov\n")
        
        gradeanalyze = init_grade_analyzer(grades, month, year, student_id, subjects)
        summary = gradeanalyze.return_comparison_overview()
        
        return summary
        
    except HTTPException:
        raise 
    except Exception as e:
        print(f"✗ Vyskytla sa chyba: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Grade Analytics API",
        "endpoints": {
            "/api/overview": "Get complete grade overview",
            "/docs": "API documentation"
        }
    }

@app.get("/api/overview")
async def get_overview():
    overview = get_grade_overview()
    return overview

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)