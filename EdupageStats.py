from constants import MONTHS_SK

class EdupageStats():    
    def __init__(self, grades: list, month: int, year: int):
        self.grades = grades
        self.month = month
        self.year = year 
        
    def filter_by_last_month(self):
        filtered_months = []
        for g in self.grades:
            month = g.date.month 
            if month == self.month:
                filtered_months.append(g)
        return filtered_months
    
    def filter_by_custom_month(self, month):
        filtered_months = []
        for g in self.grades:
            if g.date.month == month:
                filtered_months.append(g)
        return filtered_months
    
    def filter_by_subject(self, subject_name, month):
        filtered_months = self.filter_by_custom_month(month)
        filtered = []
        for g in filtered_months:
            if g.subject_name == subject_name:
                filtered.append(g)
        return filtered
    
    def convert_points_to_percent(self, points, max_points):
        if max_points == 0:
            return None
        percent = (points / max_points) * 100
        return self.convert_percent_to_grade(percent)

    def convert_percent_to_grade(self, percent):
        if percent >= 90:
            return 1.0
        elif percent >= 75:
            return 2.0
        elif percent >= 50:
            return 3.0
        elif percent >= 30:
            return 4.0
        else:
            return 5.0
    
    def objective_grade(self, grade, percent, max_points):
        grades = [1.0, 2.0, 3.0, 4.0, 5.0]
        if grade in grades:
            return grade
        elif percent:
            return self.convert_percent_to_grade(percent)
        elif max_points and isinstance(grade, (int, float)):
            return self.convert_points_to_percent(grade, max_points)
        else:
            return grade
        
    def get_subject_stats(self, subject, month):
        subject_grades = self.filter_by_subject(subject, month)
        return subject_grades   
    
    def get_grade_list(self, subject, month):
        subject = self.get_subject_stats(subject, month)
        grades = []
        for i in subject:
            grade = i.grade_n
            percent = i.percent
            max_points = i.max_points
            grades.append(self.objective_grade(grade, percent, max_points))
        return grades
    
    def count_grades(self, last_month, this_month):
        ltm = len(this_month)
        llm = len(last_month)
        return ltm, llm   
    
    def calculate_average_grade(self, subject, month):
        grades = self.get_grade_list(subject, month)
        return sum(grades) / len(grades)
    
    def calculate_average_delta_grade(self, subject, month_this, month_last):
        grades_this = self.get_grade_list(subject, month_this)
        grades_last = self.get_grade_list(subject, month_last)
        average_this = self.calculate_average_grade(subject, month_this)
        average_last = self.calculate_average_grade(subject, month_last)
        
        return average_this - average_last
    
    def get_compared_subjects(self, subject):
        grades_this = self.get_subject_stats(subject, self.month)
        grades_last = self.get_subject_stats(subject, self.month - 1)
        return grades_last, grades_this
    
    def get_comparison_overview(self):
        #TODO
        #treba dokoncit vela funkcii este
        pass
        
    def print_totals(self):
        filtered_month = self.filter_by_last_month()
        print(f"Vypisujem známky...")
        print(f"Dátum: {MONTHS_SK[self.month]} {self.year}")
        print()
        
        print(f"{'PREDMET':<15} {'UČITEĽ':<20} {'NÁZOV':<30} {'ZNÁMKA':<12} {'BODY':<12} {'MAX. BODY':<12} {'PERCENTO':<10} {'DÁTUM':<12}")
        print("=" * 140)
        
        for g in filtered_month:
            subject = g.subject_name or 'N/A'
            teacher = g.teacher.name if g.teacher else 'N/A'
            points = f"{g.grade_n}/{g.max_points}" if g.max_points != None else '-'
            max_points = f"{g.max_points}" if g.max_points else '-'
            percent = f"{g.percent}%" if g.percent else '-'
            objective_grade = self.objective_grade(g.grade_n, g.percent, g.max_points)
            date = g.date.strftime('%Y-%m-%d')
            title = g.title
            
            print(f"{subject:<15} {teacher:<20} {title:<30} {str(objective_grade):<12} {str(points):<12} {max_points:<12} {percent:<10} {date:<12}")
        