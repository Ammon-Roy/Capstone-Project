import csv

class WriteCsv():
   
    def __init__(self, cursor,file_name):
        self.cursor = cursor
        self.file_name = file_name
        
    
    def csv_creation(self, header_row):
        try:
            with open(f"{self.file_name}.csv") as csv_file:
                pass
        except:
            with open(f"{self.file_name}.csv","w")as csv_file:
                wrt = csv.writer(csv_file)
                wrt.writerow(header_row)
    
    def wipe(self, header):
        with open(f"{self.file_name}.csv","w")as csv_file:
            wrt = csv.writer(csv_file)
            wrt.writerow(header)
    
    def csv_write(self):
        pass

class ResultCsv(WriteCsv):
    
    def __init__(self, cursor, file_name):
        super().__init__(cursor, file_name)
    
    def csv_write(self):
        creation = WriteCsv(self.cursor, self.file_name)
        creation.csv_creation(["user_id","comp_id","assessment_id","score","date_taken","manager"])
        rows = self.cursor.execute("SELECT user_id,comp_id,assessment_id,score,date_taken,manager FROM Assessments_results").fetchall()
        
        with open(f"{self.file_name}.csv","a") as result_file:
            wrt = csv.writer(result_file)
            wrt.writerows(rows)

class UserReport(WriteCsv):
    
    def __init__(self, cursor, file_name, user_id):
        self.user_id = user_id
        super().__init__(cursor, file_name)
    
    def csv_write(self):
        creation = WriteCsv(self.cursor,self.file_name)
        creation.csv_creation(["name","comp_scores","avg_comp"])
        
        rows = self.cursor.execute("SELECT comp_id,assessment_id,score FROM Assessments_results WHERE user_id=? ORDER BY date_taken",(self.user_id,)).fetchall()
        user_name = self.cursor.execute("SELECT first_name, last_name FROM Users WHERE user_id =?",(self.user_id,)).fetchone()
        user_name = f"{user_name[0]} {user_name[1]}"
        avg_list = []
        score_list =[]
        
        for row in rows:
            comp_name = self.cursor.execute(f"SELECT name FROM Competencies WHERE comp_id ={row[0]}").fetchone()
            test_name = self.cursor.execute(f"SELECT name FROM Assessments WHERE assessment_id = {row[1]}").fetchone()
            avg_list.append(row[2])
            score_list.append((comp_name[0], test_name[0], row[2]))
        
        length = len(avg_list)
        avg_sum = sum(avg_list)
        avg = avg_sum/length
        
        with open(f"{self.file_name}.csv", "a") as user_report:
            wrt = csv.writer(user_report)
            wrt.writerow([user_name, score_list, avg])

class CompReport(WriteCsv):

    def __init__(self, cursor, file_name, comp_id):
        self.comp_id = comp_id
        super().__init__(cursor, file_name)

    def csv_write(self):
        creation = WriteCsv(self.cursor, self.file_name)
        creation.csv_creation(["User","Score"])
    
        name_row = self.cursor.execute("SELECT user_id, first_name, last_name FROM Users WHERE active = 1 AND user_type = 'user'").fetchall()
        test_row = self.cursor.execute("SELECT user_id, score FROM Assessments_results WHERE comp_id = ? ORDER BY date_taken",(self.comp_id,)).fetchall()
        
        file_list = []
        for name in name_row:
            avg_list = []
            for test in test_row:
                if name[0] == test[0]:
                    avg_list.append(test[1])
                else:
                    continue
            try:  
                length = len(avg_list)
                avg_sum = sum(avg_list)
                avg = avg_sum/length
            except:
                avg = 0
            user_name = f"{name[1]} {name[2]}"
            user_tuple = [user_name, avg]
            file_list.append(user_tuple)
            with open(f"{self.file_name}.csv", "a") as comp_report:
                wrt = csv.writer(comp_report)
                for item in file_list:
                    wrt.writerow(item)

        return file_list       


