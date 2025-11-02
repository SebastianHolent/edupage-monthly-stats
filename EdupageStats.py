from constants import MONTHS_SK
from utils import get_username_split

class EdupageStats():    
    def __init__(self, grades: list, month: int, year: int, student_id, subjects):
        self.grades = grades
        self.month = month
        self.year = year
        self.student_id = student_id
        self.subjects = subjects
        
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
            return 1
        elif percent >= 75:
            return 2
        elif percent >= 50:
            return 3
        elif percent >= 30:
            return 4
        else:
            return 5
    
    def objective_grade(self, grade, percent, max_points):
        grades = [1.0, 2.0, 3.0, 4.0, 5.0]
        if grade in grades:
            return int(grade)
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
        
    def get_weighted_grades(self, month):
        month_grades = self.filter_by_custom_month(month)
        grades = []
        for i in month_grades:
            grade = i.grade_n
            percent = i.percent
            max_points = i.max_points
            weight = i.importance
            obj_grade = self.objective_grade(grade, percent, max_points)
            if isinstance(obj_grade, int):
                grades.append((obj_grade, weight))
        return grades
    
    def get_weighted_grades_subject(self, subject, month):
        subject_grades_in_month = self.filter_by_subject(subject, month)
        grades = []
        for i in subject_grades_in_month:
            grade = i.grade_n
            percent = i.percent
            max_points = i.max_points
            weight = i.importance
            obj_grade = self.objective_grade(grade, percent, max_points)
            if isinstance(obj_grade, int):
                grades.append((obj_grade, weight))
        return grades
          
    def get_overall_grade_list_only_int(self, month):
        month_grades = self.filter_by_custom_month(month)
        grades = []
        for i in month_grades:
            grade = i.grade_n
            percent = i.percent
            max_points = i.max_points
            obj_grade = self.objective_grade(grade, percent, max_points)
            if isinstance(obj_grade, int):
                grades.append(obj_grade)
        return grades
        
    def get_overall_grade_list(self,month):
        month_grades = self.filter_by_custom_month(month)
        grades = []
        for i in month_grades:
            grade = i.grade_n
            percent = i.percent
            max_points = i.max_points
            obj_grade = self.objective_grade(grade, percent, max_points)
            grades.append(obj_grade)
        return grades
    
    def distribute_grades(self, month):
        grade_list = self.get_overall_grade_list_only_int(month)
        counted_grades = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }
        for i in grade_list:
            counted_grades[i] += 1
            
        return counted_grades
        
    def overall_distributed_grades(self):
        this_month_distribution = self.distribute_grades(self.month)
        last_month_distribution = self.distribute_grades(self.month - 1)
        return {
            1: this_month_distribution[1] + last_month_distribution[1],
            2: this_month_distribution[2] + last_month_distribution[2],
            3: this_month_distribution[3] + last_month_distribution[3],
            4: this_month_distribution[4] + last_month_distribution[4],
            5: this_month_distribution[5] + last_month_distribution[5],
        }
        
    def get_grade_list_only_int(self, subject, month):
        subject = self.get_subject_stats(subject, month)
        grades = []
        for i in subject:
            grade = i.grade_n
            percent = i.percent
            max_points = i.max_points
            obj_grade = self.objective_grade(grade, percent, max_points)
            if isinstance(obj_grade, int):
                grades.append(obj_grade)
        return grades
    
    def count_grades(self, last_month, this_month):
        ltm = len(this_month)
        llm = len(last_month)
        return ltm, llm   
    
    def calculate_overall_average_grade(self, month):
        grades = self.get_overall_grade_list_only_int(month)
        if len(grades) != 0:
            return round(sum(grades) / len(grades), 2)
        else:
            return 0
        
    def calculate_average_grade(self, subject, month):
        grades = self.get_grade_list_only_int(subject, month)
        if len(grades) != 0:
            return round(sum(grades) / len(grades), 2)
        else:
            return 0
    
    def calculate_overall_average_delta_grade(self, this_month, last_month):
        average_this = self.calculate_overall_average_grade(this_month)
        average_last = self.calculate_overall_average_grade(last_month)
        
        return round(average_last - average_this, 2)
    
    def calculate_average_delta_grade(self, subject, month_this, month_last):
        average_this = self.calculate_average_grade(subject, month_this)
        average_last = self.calculate_average_grade(subject, month_last)
        
        return round(average_last - average_this, 2)
    
    def calculate_average_weighted_overall(self, month):
        weighted_grades = self.get_weighted_grades(month)
        weighted = []
        length_weighted = 0
        for i in weighted_grades:
            length_weighted += 1*i[1]
            weighted.append(i[0]*i[1])
            
        if length_weighted == 0:
            return 0
        else: 
            return round(sum(weighted) / length_weighted, 2)
    
    def calculate_class_average(self, month):
        grades = self.filter_by_custom_month(month)
        class_averages = []
        for i in grades:
            class_avg = i.class_grade_avg
            percent = i.percent
            grade = i.grade_n
            max_p = i.max_points
            class_avg = self.objective_grade(class_avg, percent, max_p)
            if isinstance(class_avg, int):
                class_averages.append(class_avg)
        if len(class_averages) == 0:
            return 0
        else:
            return round(sum(class_averages) / len(class_averages), 2)
    
    def get_compared_subjects(self, subject):
        grades_this = self.get_subject_stats(subject, self.month)
        grades_last = self.get_subject_stats(subject, self.month - 1)
        return grades_last, grades_this
    
    def calculate_average_weighted(self, subject, month):
        weighted_grades = self.get_weighted_grades_subject(subject, month)
        weighted = []
        length_weighted = 0
        for i in weighted_grades:
            length_weighted += 1*i[1]
            weighted.append(i[0]*i[1])
            
        if length_weighted == 0:
            return 0
        else: 
            return round(sum(weighted) / length_weighted, 2)
    
    def calculate_avg_subject(self, subject, month):
        monthly_grade = self.filter_by_subject(subject, month)
        average_grade = []
        for g in monthly_grade:
            avg_g = g.class_grade_avg
            max_p = g.max_points
            percent = g.percent
            avg_g = self.objective_grade(avg_g, percent, max_p)
            if isinstance(avg_g, int):
                average_grade.append(avg_g)
        if len(average_grade) == 0:
            return 0
        else: 
            return round(sum(average_grade) / len(average_grade), 2)
        
    def get_each_subject_stats(self):
        subject_stats = {
            
        }
        for subject in self.subjects:
            subject_stats[subject] = {
                "counts": {
                  "counts": {
                      "this_month": len(self.filter_by_subject(subject, self.month)),
                      "last_month": len(self.filter_by_subject(subject, self.month - 1))
                  },
                  "averages": {
                      "last": self.calculate_average_grade(subject, self.month - 1),
                      "this": self.calculate_average_grade(subject, self.month),
                      "delta": self.calculate_average_delta_grade(subject, self.month, self.month - 1),
                      "weighted_this": self.calculate_average_weighted(subject, self.month),
                      "weighted_last": self.calculate_average_weighted(subject, self.month - 1),
                      "class_average_this": self.calculate_avg_subject(subject, self.month),
                      "class_average_last": self.calculate_avg_subject(subject, self.month - 1),
                  },  
                 "distribution": {
                     "distribution_this": self.distribute_grades(self.month),
                     "distribution_this": self.distribute_grades(self.month - 1)
                    }
                 }
            }
        
        return subject_stats
    
    def return_comparison_overview(self):
        return {
            "summary" : {
                "metadata": {
                    "student_id": self.student_id,
                    "student_name": get_username_split(),
                    "year_this": self.year,
                    "month_this": self.month,
                    "last_month": self.month - 1,
                },
                "overall": {
                  "counts": {
                      "this_month": len(self.filter_by_custom_month(self.month)),
                      "last_month": len(self.filter_by_custom_month(self.month - 1))
                  },
                  "averages": {
                      "last": self.calculate_overall_average_grade(self.month - 1),
                      "this": self.calculate_overall_average_grade(self.month),
                      "delta": self.calculate_overall_average_delta_grade(self.month, self.month - 1),
                      "weighted_this": self.calculate_average_weighted_overall(self.month),
                      "weighted_last": self.calculate_average_weighted_overall(self.month - 1),
                      "class_average_this": self.calculate_class_average(self.month),
                      "class_average_last": self.calculate_class_average(self.month - 1),
                  },  
                 "distribution": self.overall_distributed_grades(),
                },
                "by_subject": self.get_each_subject_stats(),
                    
            }
        }   
        
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
        