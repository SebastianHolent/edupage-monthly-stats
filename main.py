from utils import *
from datetime import date
import traceback

             
def main():
    try:
        edupage = init_edupage()
        if not login_edupage(edupage):
            return 
        
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        
        print("Načítavam známky...")
        grades = edupage.get_grades()
        print(f"✓ Načítaných {len(grades)} známok\n")
        print("Načítavam predmety...")
        subjects = get_my_subjects_from_timetable(edupage)
        print(subjects)
        print(f"✓ Načítaných {len(subjects)} predmetov\n")
        
        gradeanalyze = init_grade_analyzer(grades, month, year)

        gradeanalyze.print_totals()
        
        
    except Exception as e:
        print(f"✗ Vyskytla sa chyba: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()