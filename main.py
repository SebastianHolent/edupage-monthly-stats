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
        month = current_date.month - 1
        student_id = edupage.get_user_id()
        
        print("Načítavam známky...")
        grades = edupage.get_grades()
        print(f"✓ Načítaných {len(grades)} známok\n")
        print("Načítavam predmety...")
        subjects = get_my_subjects_from_timetable(edupage)
        print(subjects)
        print(f"✓ Načítaných {len(subjects)} predmetov\n")
        
        gradeanalyze = init_grade_analyzer(grades, month, year, student_id, subjects)

        gradeanalyze.print_totals()
        print(gradeanalyze.return_comparison_overview())
        
    except Exception as e:
        print(f"✗ Vyskytla sa chyba: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()