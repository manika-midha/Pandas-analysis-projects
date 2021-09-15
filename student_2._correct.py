
import pandas as pd
import json

def func(file_m,file_s1,file_t1,file_c1,file_output): #pass the file names from command line
#file_m = 'marks.csv'
#file_s1 = 'students_1.csv'
#file_t1 = 'tests_1.csv'
#file_c1 = 'courses_1.csv'
#file_output = 'manika_output.json'

    #display all columns and full width 
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    #create individual data frames for each csv file
    data_m = pd.read_csv(file_m)
    data_s = pd.read_csv(file_s1)
    data_t = pd.read_csv(file_t1)
    data_c = pd.read_csv(file_c1)

    '''combine data from different csv files and make one dataframe'''
    #merge csv files - marks.csv and students_1.csv
    output_s_m = pd.merge(data_m,data_s,on = 'student_id',how = 'left')
    #disply dataframe in the order of columns as mentioned
    marks_students = output_s_m[['student_id','student_name','test_id','mark']]

    #merge output of mix of marks.csv and students_1.csv with tests1.csv
    output_s_m_t = pd.merge(marks_students,data_t,on = 'test_id',how = 'left')
    ##disply dataframe in the order of columns as mentioned
    marks_students_tests = output_s_m_t[['student_id','student_name','test_id','mark','weight','course_id']]

    #merge output of mix of marks.csv and students_1.csv, tests1.csv with courses.csv
    final_df = pd.merge(marks_students_tests,data_c,on = 'course_id', how = 'left')
    #--------------------------------------
    student_list,course_avg_list_per_s,list_of_courses = [],[],[]
    result_dict = {'students': student_list}
    student_dict,course_dict = {},{}
    course_avg = 0
    #--------------------------------------

    for i in range(1,4):
            s_c = final_df[final_df['student_id'] == i] #dataset of one student whose id = i

            #create a dict for each student
            student_dict['id'] = i
            student_dict['name'] = s_c.iloc[0,1] #any row (here 0) but column 1
            student_list.append(student_dict) #student_list is the value for key 'students' in the result dict
            
            '''iterate through all courses taken by a student'''
            for j in range(1,4) : #courses = 1,2,3
                c_per_s = s_c[s_c['course_id'] == j] #dataset for 1 course taken by a student
                if not c_per_s.empty: #proceed if the dataset for a course is not empty. Necessary as not all students took all courses.
                    for k in range(len(c_per_s)):
                        #for 1 course, mutiply marks by weight for each test and then sum them
                        course_avg = course_avg + (c_per_s.iloc[k,3] * c_per_s.iloc[k,4])/100 #(course_avg = course_avg + (marks * weight))
                        
                    #add avg of all courses taken by a student to a list.this will be usefult o calculate total avg for a student
                    course_avg_list_per_s.append(round(course_avg,2))

                    '''make a dict for each course taken by a student'''
                    course_dict['id'] = j
                    course_dict['name'] = c_per_s.iloc[0,6] #any row(0) but column 6
                    course_dict['teacher'] = c_per_s.iloc[0,7]
                    course_dict['courseAverage'] = round(course_avg,2) #round the number to 2 decimal points
                    list_of_courses.append(course_dict)
                    course_dict = {}
                    course_avg = 0
            
            t_avg = round(sum(course_avg_list_per_s)/len(course_avg_list_per_s),2) #total average for each student. 
            #combine the averages of all courses taken by a student and divide by num of courses. round off to 2 decimal points.

            '''continue adding to the dict for each student'''
            student_dict['totalAverage'] = t_avg
            student_dict['courses'] = list_of_courses
            student_dict = {}
            list_of_courses,course_avg_list_per_s = [],[]

    #create empty file manika_output.json and load the result_dict in it. 
    with open(file_output,'w') as f :
        json.dump(result_dict,f,indent=4)



        
   

