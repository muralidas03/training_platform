
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user_management.models import Role, User
from django.shortcuts import get_object_or_404
from user_management.decorators import check_permission
from django.contrib.auth.hashers import make_password
from django.db import transaction


def user_login(request):
    if request.method == 'POST':
        print('request.POST', request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a success page
            else:
                print('Invalid email or password')
                form.add_error(None, 'Invalid email or password')
        else:
            print('form', form.errors)
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'Auth/login.html', context)


def dashboard(request):
    return render(request, 'dashboard.html',{'dashboard':'active'})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('user_login')
    else:
        return redirect('user_login')

# Create
@login_required(login_url='/')
@check_permission('student_create')
def student_create(request):
    try:
        error_message = None

        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                error_message = "A user with this email already exists. Please use a different email."
            else:
                with transaction.atomic():
                    # ✅ Get or create the "student" role
                    student_role, created = Role.objects.get_or_create(
                        name="student",
                        defaults={
                            "description": "Default student role",
                            "created_by": request.user,
                        }
                    )
                    if not created and student_role.created_by is None:
                        student_role.created_by = request.user
                        student_role.save()

                    # ✅ Create User with student role
                    user = User.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone_number=phone_number,
                        password=make_password(password),
                        roles=student_role,
                        is_student=True,
                        checker=True,
                        maker=True
                    )
                    print("usergdgashdagdsad",user)

                    # ✅ Create Student
                    Student.objects.create(
                        user=user,
                        phone=phone_number,
                        address=address
                    )

                    return redirect('student_list')

        context = {
            'screen_name': 'Student',
            'error_message': error_message,
        }
        return render(request, 'student_create.html', context)

    except Exception as error:
        return render(request, '500.html', {'error': error})

# Read - List View
@login_required(login_url='/')
@check_permission('student_view')
def student_list(request):
    """
    Displays a list of all Student records.

    - Fetches all records from the Student model.
    - Passes the records to the template for rendering.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        records = Student.objects.all()
        context = {
            'records': records, 'screen_name': 'Student'
        }
        return render(request, 'student_list.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Read - Detail View
@login_required(login_url='/')
@check_permission('student_view')
def student_detail(request, pk):
    """
    Displays the details of a specific Student record.

    - Fetches the record based on the primary key (pk).
    - Passes the record to the form for viewing.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        record = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=record)
        context = {
            'screen_name': 'Student', 'view': True, 'form': form
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Update
@login_required(login_url='/')
@check_permission('student_update')
def student_update(request, pk):
    """
    Handles the updating of an existing Student record.

    - If the request method is POST, the form data is validated and, if valid, the record is updated.
    - If the request method is GET, the existing record is displayed in the form.
    - Upon successful update, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        student = get_object_or_404(Student, pk=pk)
        if request.method == "POST":
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()  # Save the updated record
                return redirect('student_list')
        else:
            form = StudentForm(instance=student)  # Display the existing record in the form
        context = {
            'form': form, 'screen_name': 'Student'
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Delete
@login_required(login_url='/')
@check_permission('student_delete')
def student_delete(request, pk):
    """
    Handles the deletion of an existing Student record.

    - Fetches the record based on the primary key (pk).
    - Deletes the record from the database.
    - Upon successful deletion, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        record = get_object_or_404(Student, pk=pk)
        record.delete()  # Delete the record
        return redirect('student_list')
    except Exception as error:
        return render(request, '500.html', {'error': error})
# Create
@login_required(login_url='/')
@check_permission('course_create')
def course_create(request):
    """
    Handles the creation of a new Course record.

    - If the request method is POST, the form data is validated and, if valid, the new record is saved.
    - If the request method is GET, an empty form is displayed.
    - Upon successful creation, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        if request.method == "POST":
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()  # Save the form data as a new record
                return redirect('course_list')
        else:
            form = CourseForm()  # Display an empty form
        context = {
            'form': form, 'screen_name': 'Course'
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Read - List View
@login_required(login_url='/')
@check_permission('course_view')
def course_list(request):
    """
    Displays a list of all Course records.

    - Fetches all records from the Course model.
    - Passes the records to the template for rendering.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        records = Course.objects.all()
        context = {
            'records': records, 'screen_name': 'Course'
        }
        return render(request, 'course_list.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Read - Detail View
@login_required(login_url='/')
@check_permission('course_view')
def course_detail(request, pk):
    """
    Displays the details of a specific Course record.

    - Fetches the record based on the primary key (pk).
    - Passes the record to the form for viewing.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        record = get_object_or_404(Course, pk=pk)
        form = CourseForm(instance=record)
        context = {
            'screen_name': 'Course', 'view': True, 'form': form
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Update
@login_required(login_url='/')
@check_permission('course_update')
def course_update(request, pk):
    """
    Handles the updating of an existing Course record.

    - If the request method is POST, the form data is validated and, if valid, the record is updated.
    - If the request method is GET, the existing record is displayed in the form.
    - Upon successful update, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        course = get_object_or_404(Course, pk=pk)
        if request.method == "POST":
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()  # Save the updated record
                return redirect('course_list')
        else:
            form = CourseForm(instance=course)  # Display the existing record in the form
        context = {
            'form': form, 'screen_name': 'Course'
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Delete
@login_required(login_url='/')
@check_permission('course_delete')
def course_delete(request, pk):
    """
    Handles the deletion of an existing Course record.

    - Fetches the record based on the primary key (pk).
    - Deletes the record from the database.
    - Upon successful deletion, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        record = get_object_or_404(Course, pk=pk)
        record.delete()  # Delete the record
        return redirect('course_list')
    except Exception as error:
        return render(request, '500.html', {'error': error})
# Create
@login_required(login_url='/')
@check_permission('trainingschedule_create')
def trainingschedule_create(request):
    """
    Handles the creation of a new TrainingSchedule record.

    - If the request method is POST, the form data is validated and, if valid, the new record is saved.
    - If the request method is GET, an empty form is displayed.
    - Upon successful creation, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        if request.method == "POST":
            form = TrainingScheduleForm(request.POST)
            if form.is_valid():
                form.save()  # Save the form data as a new record
                return redirect('trainingschedule_list')
        else:
            form = TrainingScheduleForm()  # Display an empty form
        context = {
            'form': form, 'screen_name': 'TrainingSchedule'
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Read - List View
@login_required(login_url='/')
@check_permission('trainingschedule_view')
def trainingschedule_list(request):
    """
    Displays a list of all TrainingSchedule records.

    - Fetches all records from the TrainingSchedule model.
    - Passes the records to the template for rendering.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        records = TrainingSchedule.objects.all()
        context = {
            'records': records, 'screen_name': 'TrainingSchedule'
        }
        return render(request, 'trainingschedule_list.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Read - Detail View
@login_required(login_url='/')
@check_permission('trainingschedule_view')
def trainingschedule_detail(request, pk):
    """
    Displays the details of a specific TrainingSchedule record.

    - Fetches the record based on the primary key (pk).
    - Passes the record to the form for viewing.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        record = get_object_or_404(TrainingSchedule, pk=pk)
        form = TrainingScheduleForm(instance=record)
        context = {
            'screen_name': 'TrainingSchedule', 'view': True, 'form': form
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Update
@login_required(login_url='/')
@check_permission('trainingschedule_update')
def trainingschedule_update(request, pk):
    """
    Handles the updating of an existing TrainingSchedule record.

    - If the request method is POST, the form data is validated and, if valid, the record is updated.
    - If the request method is GET, the existing record is displayed in the form.
    - Upon successful update, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        trainingschedule = get_object_or_404(TrainingSchedule, pk=pk)
        if request.method == "POST":
            form = TrainingScheduleForm(request.POST, instance=trainingschedule)
            if form.is_valid():
                form.save()  # Save the updated record
                return redirect('trainingschedule_list')
        else:
            form = TrainingScheduleForm(instance=trainingschedule)  # Display the existing record in the form
        context = {
            'form': form, 'screen_name': 'TrainingSchedule'
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Delete
@login_required(login_url='/')
@check_permission('trainingschedule_delete')
def trainingschedule_delete(request, pk):
    """
    Handles the deletion of an existing TrainingSchedule record.

    - Fetches the record based on the primary key (pk).
    - Deletes the record from the database.
    - Upon successful deletion, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        record = get_object_or_404(TrainingSchedule, pk=pk)
        record.delete()  # Delete the record
        return redirect('trainingschedule_list')
    except Exception as error:
        return render(request, '500.html', {'error': error})
# Create
@login_required(login_url='/')
@check_permission('studenttraining_create')
def studenttraining_create(request):
    """
    Handles the creation of a new StudentTraining record.

    - If the request method is POST, the form data is validated and, if valid, the new record is saved.
    - If the request method is GET, an empty form is displayed.
    - Upon successful creation, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        if request.method == "POST":
            form = StudentTrainingForm(request.POST)
            if form.is_valid():
                form.save()  # Save the form data as a new record
                return redirect('studenttraining_list')
        else:
            form = StudentTrainingForm()  # Display an empty form
        context = {
            'form': form, 'screen_name': 'StudentTraining'
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Read - List View
@login_required(login_url='/')
@check_permission('studenttraining_view')
def studenttraining_list(request):
    """
    Displays a list of all StudentTraining records.

    - Fetches all records from the StudentTraining model.
    - Passes the records to the template for rendering.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        records = StudentTraining.objects.all()
        context = {
            'records': records, 'screen_name': 'StudentTraining'
        }
        return render(request, 'studenttraining_list.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Read - Detail View
@login_required(login_url='/')
@check_permission('studenttraining_view')
def studenttraining_detail(request, pk):
    """
    Displays the details of a specific StudentTraining record.

    - Fetches the record based on the primary key (pk).
    - Passes the record to the form for viewing.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        record = get_object_or_404(StudentTraining, pk=pk)
        form = StudentTrainingForm(instance=record)
        context = {
            'screen_name': 'StudentTraining', 'view': True, 'form': form
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Update
@login_required(login_url='/')
@check_permission('studenttraining_update')
def studenttraining_update(request, pk):
    """
    Handles the updating of an existing StudentTraining record.

    - If the request method is POST, the form data is validated and, if valid, the record is updated.
    - If the request method is GET, the existing record is displayed in the form.
    - Upon successful update, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        studenttraining = get_object_or_404(StudentTraining, pk=pk)
        if request.method == "POST":
            form = StudentTrainingForm(request.POST, instance=studenttraining)
            if form.is_valid():
                form.save()  # Save the updated record
                return redirect('studenttraining_list')
        else:
            form = StudentTrainingForm(instance=studenttraining)  # Display the existing record in the form
        context = {
            'form': form, 'screen_name': 'StudentTraining'
        }
        return render(request, 'create.html', context)
    except Exception as error:
        return render(request, '500.html', {'error': error})

# Delete
@login_required(login_url='/')
@check_permission('studenttraining_delete')
def studenttraining_delete(request, pk):
    """
    Handles the deletion of an existing StudentTraining record.

    - Fetches the record based on the primary key (pk).
    - Deletes the record from the database.
    - Upon successful deletion, redirects to the list view.
    - In case of an error, renders a custom 500 error page.
    """
    try:
        record = get_object_or_404(StudentTraining, pk=pk)
        record.delete()  # Delete the record
        return redirect('studenttraining_list')
    except Exception as error:
        return render(request, '500.html', {'error': error})
