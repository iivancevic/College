from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import * 


# Create your views here.

@login_required(login_url='login')
def home(request):
    if str(request.user.uloga) == 'STUDENT':
        return redirect('enrollment_form', request.user.id)
    return render(request, 'home.html', {})

@login_required(login_url='login')
def subjects(request):
    if str(request.user.uloga) == 'ADMIN' or str(request.user.uloga) == 'PROFESOR':
        subjects = Predmet.objects.all()

        content = {
            "subjects" : subjects,
        }
        return render(request, 'subjects.html', {'content' : content})

@login_required(login_url='login')
def students(request):
    if str(request.user.uloga) == 'ADMIN':
        students = Korisnik.objects.filter(uloga__uloga__contains="STUDENT")

        content = {
            "students" : students,
        }
        return render(request, 'students.html', {'content' : content})

@login_required(login_url='login')
def professors(request):
    if str(request.user.uloga) == 'ADMIN':
        professors = Korisnik.objects.filter(uloga__uloga__contains="PROFESOR")
        print (professors)

        content = {
            "professors" : professors,
        }
        return render(request, 'professors.html', {'content' : content})


@login_required(login_url='login')
def create_subject(request):
    if str(request.user.uloga) == 'ADMIN':
        if request.method == 'GET':
            subjectForm = SubjectForm()
            return render(request, 'create_subject.html', {'form':subjectForm})
        elif request.method == 'POST' and request.user.is_authenticated:
            subjectForm = SubjectForm(request.POST)
            if subjectForm.is_valid():
                subjectForm.save()
                cleaned_data = subjectForm.cleaned_data
                print(cleaned_data)
                return redirect('subjects')            
            else:
                return HttpResponseNotAllowed()
        return redirect('login')

@login_required(login_url='login')
def create_user(request):
    if str(request.user.uloga) == 'ADMIN':
        if request.method == 'GET':
            userForm = RegistrationForm()
            return render(request, 'create_user.html', {'form':userForm})
        elif request.method == 'POST' and request.user.is_authenticated:
            userForm = RegistrationForm(request.POST)
            if userForm.is_valid():
                userForm.save()
                cleaned_data = userForm.cleaned_data
                if (str(cleaned_data['uloga']) == 'STUDENT'):
                    return redirect('students')
                elif str((cleaned_data['uloga']) == 'PROFESOR'): 
                    return redirect("professors")    
            else:
                return HttpResponseNotAllowed()
        return redirect('login')

@login_required(login_url='login')
def update_subject(request, subject_id):
    if str(request.user.uloga) == 'ADMIN':       
        subject_by_id = Predmet.objects.get(id=subject_id)
        if request.method == 'GET':
            data_to_update = SubjectForm(instance=subject_by_id)
            return render(request, 'update_subject.html', {'form': data_to_update})
        elif request.method == 'POST':
            data_to_update = SubjectForm(request.POST, instance=subject_by_id)
            if data_to_update.is_valid():
                data_to_update.save()
                return redirect('subjects')
        else:
            return HttpResponse("Something went wrong!")

@login_required(login_url='login')
def update_user(request, user_id):
    if str(request.user.uloga) == 'ADMIN':          
        user_by_id = Korisnik.objects.get(id=user_id)
        
        if request.method == 'GET':
            data_to_update = UserForm(instance=user_by_id)
            return render(request, 'update_user.html', {'form': data_to_update})
        elif request.method == 'POST':
            data_to_update = UserForm(request.POST, instance=user_by_id)
            if data_to_update.is_valid():
                data_to_update.save()
                cleaned_data = data_to_update.cleaned_data
                if (str(cleaned_data['uloga']) == 'STUDENT'):
                    return redirect('students')
                elif (str(cleaned_data['uloga']) == 'PROFESOR'): 
                    return redirect("professors")    
        else:
            return HttpResponse("Something went wrong!")

@login_required(login_url='login')
def delete_confirmation(request, subject_id):
    if str(request.user.uloga) == 'ADMIN':
        if request.method == 'GET':
            return render(request, 'delete_confirmation.html', {"data":subject_id})
        return HttpResponseNotAllowed()

@login_required(login_url='login')
def delete_confirmation_user(request, user_id):
    if str(request.user.uloga) == 'ADMIN':
        if request.method == 'GET':
            return render(request, 'delete_confirmation_user.html', {"data":user_id})
        return HttpResponseNotAllowed()

@login_required(login_url='login')
def delete_subject(request, subject_id):
    if str(request.user.uloga) == 'ADMIN':
        subject_by_id = Predmet.objects.get(id=subject_id)
        if 'Yes' in request.POST:
            subject_by_id.delete()
            return HttpResponse('Successfully deleted! <br><a href="..">Subjects</a><br>')
        return redirect('subjects')

@login_required(login_url='login')
def delete_user(request, user_id):
    if str(request.user.uloga) == 'ADMIN':
        user_by_id = Korisnik.objects.get(id=user_id)
        if (str(user_by_id.uloga) == 'STUDENT'):
            if 'Yes' in request.POST:
                user_by_id.delete()
                return HttpResponse('Successfully deleted! <br><a href="..">Students</a><br>')
            return redirect('students')
        elif (str(user_by_id.uloga) == 'PROFESOR'):
            if 'Yes' in request.POST:
                user_by_id.delete()
                return HttpResponse('Successfully deleted! <br><a href="..">Professors</a><br>')
            return redirect('professors')

@login_required(login_url='login')
def enrollment_form(request, student_id):
    if str(request.user.uloga) == 'ADMIN' or str(request.user.uloga) == 'PROFESOR' or request.user.id == student_id:
        student_by_id = Korisnik.objects.get(id=student_id)
        subjects = Predmet.objects.all()
        enrolled = Upisi.objects.filter(student=student_by_id)
        enrolled_ids = Upisi.objects.filter(student=student_by_id).values_list('predmet', flat=True)
        not_enrolled = {}
        
        for subject in subjects:
            print (subject.sem_red)
            if subject.id not in enrolled_ids:
                not_enrolled[subject.id] = subject

        content = {
            "student" : student_by_id,
            'subjects' : subjects,
            'enrolled' : enrolled,
            'not_enrolled' : not_enrolled
        }
        return render(request, 'enrollment_form.html', {'content' : content})

@login_required(login_url='login')
def enroll_subject(request, student_id, subject_id):
    if str(request.user.uloga) == 'ADMIN' or request.user.id == student_id:
        subject = Predmet.objects.get(id=subject_id)
        student = Korisnik.objects.get(id=student_id)
        Upisi.objects.create(predmet=subject, student=student, status='enrolled')
        return redirect('enrollment_form', student_id)

@login_required(login_url='login')
def remove_subject(request, student_id, subject_id):
    if str(request.user.uloga) == 'ADMIN' or request.user.id == student_id:
        subject = Upisi.objects.filter(id=subject_id, student=student_id)
        if 'Yes' in request.POST:
            subject.delete()
            return HttpResponse(f'Successfully deleted! <br><a href="/home/enrollment_form/{student_id}">Subjects</a><br>')
        return redirect('enrollment_form', student_id)

@login_required(login_url='login')
def remove_confirmation_subject(request, student_id, subject_id):
    if str(request.user.uloga) == 'ADMIN' or request.user.id == student_id:
        if request.method == 'GET':
            data = {
                "student_id" : student_id,
                "subject_id" : subject_id
            }
            return render(request, 'remove_confirmation_subject.html', {"data":data})
        return HttpResponseNotAllowed()

@login_required(login_url='login')
def students_by_subject(request, subject_id):
    if str(request.user.uloga) == 'ADMIN' or str(request.user.uloga) == 'PROFESOR':
        subject_by_id = Predmet.objects.get(id=subject_id)
        enrolls = Upisi.objects.filter(predmet_id=subject_id)

        content = {
            "subject" : subject_by_id,
            "enrolls" : enrolls
        }
        return render (request, 'students_by_subject.html', {"content" : content})

@login_required(login_url='login')
def pass_subject(request, subject_id, enrollment_id):
    if str(request.user.uloga) == 'ADMIN' or str(request.user.uloga) == 'PROFESOR':
        query = Upisi.objects.filter(id = enrollment_id).update(status='passed')
        return redirect('students_by_subject', subject_id)

@login_required(login_url='login')
def fail_subject(request, subject_id, enrollment_id):
    if str(request.user.uloga) == 'ADMIN' or str(request.user.uloga) == 'PROFESOR':
        query = Upisi.objects.filter(id = enrollment_id).update(status='failed')
        return redirect('students_by_subject', subject_id)


@login_required(login_url='login')
def all_subjects(request):
    if str(request.user.uloga) == 'ADMIN':
        subjects = Predmet.objects.all()
        number_of_students = []
        number_of_students_red = {}
        number_of_students_izv = {}
        red_students = []
        izv_students = []


        for subject in subjects:
            number_of_students_red[subject] = 0
            number_of_students_izv[subject] = 0
            enrolls = Upisi.objects.filter(predmet=subject)
            number_of_students.append(enrolls.count())
            for enroll in enrolls:
                if (enroll.student.status == 'red'): 
                        red_students.append(enroll.student)
                        number_of_students_red[subject] += 1
                else:
                    number_of_students_izv[subject] += 1
                    izv_students.append(enroll.student)

        print ("Redovni studenti: ")
        print (red_students)
        print ("Izvanredni studenti: ")
        print (izv_students)

        content = {
            "subjects" : subjects,
            "number_of_students_red" : number_of_students_red,
            "number_of_students_izv" : number_of_students_izv
        }
       
        return render (request, 'all_subjects.html', {"content" : content})