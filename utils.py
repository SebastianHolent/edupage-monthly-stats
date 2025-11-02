import os
import re
import traceback
from dotenv import load_dotenv
from datetime import date, timedelta
from edupage_api import Edupage
from edupage_api.exceptions import BadCredentialsException, CaptchaException

load_dotenv()

def get_username_split():
    username = os.environ.get('MENO')
    partsname = re.findall('[A-Z][^A-Z]*', username)
    name = partsname[0] 
    surname = partsname[1]
    return f"{name} {surname}"

def get_subjects(edupage):
    return edupage.get_subjects()

def get_my_subjects_from_timetable(edupage):
    subjects = set()
    
    for i in range(7):
        day = date.today() + timedelta(days=i)
        timetable = edupage.get_my_timetable(day)
        
        if timetable and timetable.lessons:
            for lesson in timetable.lessons:
                if lesson.subject:
                    subjects.add(lesson.subject.short)
    
    return sorted(list(subjects))

def get_my_subjects_from_grades(grades):
    subjects = set()
    for grade in grades:
        if grade.subject_name:
            subjects.add(grade.subject_name)
    return sorted(list(subjects))

def init_edupage():
    return Edupage()

def login_edupage(edupage):
    username = os.environ.get('MENO')
    password = os.environ.get('HESLO')
    
    try:
        print("Prihlasujem sa do Edupage...")
        two_factor = edupage.login_auto(username=username, password=password)
        
        if two_factor:
            print("Vyžaduje sa dvojfaktorové overenie!")
            code = input("Zadajte overovací kód: ")
            two_factor.finish(code)
        
        print("✓ Prihlásenie úspešné!\n")
        return True
        
    except BadCredentialsException:
        print("✗ Chyba: Nesprávne meno alebo heslo!")
    except CaptchaException:
        print("✗ Chyba: Vyžaduje sa captcha! Skúste to neskôr.")
    except Exception as e:
        print(f"✗ Vyskytla sa chyba: {e}")
        traceback.print_exc()

def init_grade_analyzer(grades, month, year, student_id, subjects):
    from EdupageStats import EdupageStats
    return EdupageStats(grades=grades, month=month, year=year, student_id=student_id, subjects=subjects)