import cv2
import mediapipe as mp
import numpy as np
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *
from random import randint
from django.http import JsonResponse




def index(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect('admin_home')
            else:
                messages.error(request, "Invalid Credentials, Please try again")
                return redirect('index')
    package = Package.objects.order_by('id')[:5]
    return render(request, 'index.html', locals())


def registration(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['secondname']
        email = request.POST['email']
        pwd = request.POST['password']
        mobile = request.POST['mobile']
        address = request.POST['address']

        user = User.objects.create_user(first_name=fname, last_name=lname, email=email, password=pwd, username=email)
        Signup.objects.create(user=user, mobile=mobile, address=address)
        messages.success(request, "Register Successful")
        return redirect('user_login')
    return render(request, 'registration.html', locals())


def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        if user:
            if user.is_staff:
                messages.error(request, "Invalid User")
                return redirect('user_login')
            else:
                login(request, user)
                messages.success(request, "User Login Successful")
                return redirect('index')
        else:
            messages.error(request, "Invalid User")
            return redirect('user_login')
    return render(request, 'user_login.html', locals())


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    totalcategory = Category.objects.all().count()
    totalpackagetype = Packagetype.objects.all().count()
    totalpackage = Package.objects.all().count()
    totalbooking = Booking.objects.all().count()
    new = Booking.objects.filter(status="1")
    partial = Booking.objects.filter(status="2")
    full = Booking.objects.filter(status="3")
    return render(request, 'admin/admin_home.html', locals())



def Logout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('index')

def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('index')

def user_profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['secondname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']

        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname, email=email)
        Signup.objects.filter(user=request.user).update(mobile=mobile, address=address)
        messages.success(request, "Updation Successful")
        return redirect('user_profile')
    data = Signup.objects.get(user=request.user)
    return render(request, "user_profile.html", locals())

def user_change_password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('user_change_password')
    return render(request,'user_change_password.html')

def manageCategory(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.all()
    try:
        if request.method == "POST":
            categoryname = request.POST['categoryname']

            try:
                Category.objects.create(categoryname=categoryname)
                error = "no"
            except:
                error = "yes"
    except:
        pass
    return render(request, 'admin/manageCategory.html', locals())

def editCategory(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        categoryname = request.POST['categoryname']

        category.categoryname = categoryname

        try:
            category.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/editCategory.html', locals())

def deleteCategory(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('manageCategory')

@login_required(login_url='/admin_login/')
def reg_user(request):
    data = Signup.objects.all()
    d = {'data': data}
    return render(request, "admin/reg_user.html", locals())

@login_required(login_url='/admin_login/')
def delete_user(request, pid):
    data = Signup.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('reg_user')

def managePackageType(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    package = Packagetype.objects.all()
    category = Category.objects.all()
    try:
        if request.method == "POST":
            cid = request.POST['category']
            categoryid = Category.objects.get(id=cid)

            packagename = request.POST['packagename']

            try:
                Packagetype.objects.create(category=categoryid, packagename=packagename)
                error = "no"
            except:
                error = "yes"
    except:
        pass
    return render(request, 'admin/managePackageType.html', locals())

def editPackageType(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.all()
    package = Packagetype.objects.get(id=pid)
    if request.method == "POST":
        cid = request.POST['category']
        categoryid = Category.objects.get(id=cid)
        packagename = request.POST['packagename']

        package.category = categoryid
        package.packagename = packagename

        try:
            package.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/editPackageType.html', locals())


def deletePackageType(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    package = Packagetype.objects.get(id=pid)
    package.delete()
    return redirect('managePackageType')

def addPackage(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.all()
    packageid = request.GET.get('packagename', None)
    mypackage = None
    if packageid:
        mypackage = Packagetype.objects.filter(packagename=packageid)
    if request.method == "POST":
        cid = request.POST['category']
        categoryid = Category.objects.get(id=cid)
        packagename = request.POST['packagename']
        packageobj = Packagetype.objects.get(id=packagename)
        titlename = request.POST['titlename']
        duration = request.POST['duration']
        price = request.POST['price']
        description = request.POST['description']

        try:
            Package.objects.create(category=categoryid,packagename=packageobj,
                                   titlename=titlename, packageduration=duration,price=price,description=description)
            error = "no"
        except:
            error = "yes"
    mypackage = Packagetype.objects.all()
    return render(request, 'admin/addPackage.html',locals())

def managePackage(request):
    package = Package.objects.all()
    return render(request, 'admin/managePackage.html',locals())

@login_required(login_url='/user_login/')
def booking_history(request):
    data = Signup.objects.get(user=request.user)
    data = Booking.objects.filter(register=data)
    return render(request, "booking_history.html", locals())

@login_required(login_url='/admin_login/')
def new_booking(request):
    action = request.GET.get('action')
    data = Booking.objects.filter()
    if action == "New":
        data = data.filter(status="1")
    elif action == "Partial":
        data = data.filter(status="2")
    elif action == "Full":
        data = data.filter(status="3")
    elif action == "Total":
        data = data.filter()
    if request.user.is_staff:
        return render(request, "admin/new_booking.html", locals())
    else:
        return render(request, "booking_history.html", locals())


def booking_detail(request, pid):
    data = Booking.objects.get(id=pid)
    if request.method == "POST":
        price = request.POST['price']
        status = request.POST['status']
        data.status = status
        data.save()
        Paymenthistory.objects.create(booking=data, price=price, status=status)
        messages.success(request, "Action Updated")
        return redirect('booking_detail', pid)
    payment = Paymenthistory.objects.filter(booking=data)
    if request.user.is_staff:
        return render(request, "admin/admin_booking_detail.html", locals())
    else:
        return render(request, "user_booking_detail.html", locals())

def editPackage(request, pid):
    category = Category.objects.all()
    if request.method == "POST":
        cid = request.POST['category']
        categoryid = Category.objects.get(id=cid)
        packagename = request.POST['packagename']
        packageobj = Packagetype.objects.get(id=packagename)
        titlename = request.POST['titlename']
        duration = request.POST['duration']
        price = request.POST['price']
        description = request.POST['description']

        Package.objects.filter(id=pid).update(category=categoryid,packagename=packageobj,
                                   titlename=titlename, packageduration=duration,price=price,description=description)
        messages.success(request, "Updated Successful")
        return redirect('managePackage')
    data = Package.objects.get(id=pid)
    mypackage = Packagetype.objects.all()
    return render(request, "admin/editPackage.html", locals())

def load_subcategory(request):
    categoryid = request.GET.get('category')
    subcategory = Package.objects.filter(category=categoryid).order_by('PackageName')
    return render(request,'subcategory_dropdown_list_options.html',locals())

def deletePackage(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    package = Package.objects.get(id=pid)
    package.delete()
    return redirect('managePackage')

def deleteBooking(request, pid):
    booking = Booking.objects.get(id=pid)
    booking.delete()
    messages.success(request, "Delete Successful")
    return redirect('new_booking')

def bookingReport(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Booking.objects.filter(creationdate__gte=fromdate, creationdate__lte=todate)
        data2 = True
    return render(request, "admin/bookingReport.html", locals())

def regReport(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Signup.objects.filter(creationdate__gte=fromdate, creationdate__lte=todate)
        data2 = True
    return render(request, "admin/regReport.html", locals())


def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'admin/changePassword.html',locals())

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



@login_required(login_url='/user_login/')
def apply_booking(request, pid):
    data = Package.objects.get(id=pid)
    register = Signup.objects.get(user=request.user)
    booking = Booking.objects.create(package=data, register=register, bookingnumber=random_with_N_digits(10))
    messages.success(request, 'Booking Applied')
    return redirect('/')


# Helper function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    ab = a - b
    bc = c - b

    if np.linalg.norm(ab) == 0 or np.linalg.norm(bc) == 0:
        return 0.0  # Avoid division by zero

    angle = np.arccos(np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc)))
    return np.degrees(angle)


# Function to handle video processing and exercise detection
def handle_exercise_detection(video_file_path, exercise_type):
    cap = cv2.VideoCapture(video_file_path)
    correct_reps = 0
    incorrect_reps = 0
    feedback = ""
    total_reps = 0

    # Mediapipe setup
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Output video setup
    output_path = os.path.join(settings.MEDIA_ROOT, "output_video_with_feedback.mp4")
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (850, 500))

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (850, 500))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                pose_landmarks = results.pose_landmarks.landmark

                # Angle calculations
                left_elbow_angle = calculate_angle(
                    pose_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                    pose_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
                    pose_landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                )
                right_elbow_angle = calculate_angle(
                    pose_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                    pose_landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
                    pose_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                )

                # Exercise-specific logic
                if exercise_type == "Squat":
                    if 160 < left_elbow_angle < 180 and 160 < right_elbow_angle < 180:
                        feedback = "Good Squat!"
                        correct_reps += 1
                    else:
                        feedback = "Incorrect Squat. Adjust your form."
                        incorrect_reps += 1

                elif exercise_type == "Pushup":
                    if 160 < left_elbow_angle < 180 and 160 < right_elbow_angle < 180:
                        feedback = "Good Pushup!"
                        correct_reps += 1
                    else:
                        feedback = "Incorrect Pushup. Keep your body straight."
                        incorrect_reps += 1

                total_reps += 1

            # Add feedback text on video
            cv2.putText(image, f"Reps: {correct_reps}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"Feedback: {feedback}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Write the frame with feedback to the output video
            out.write(image)

        cap.release()
        out.release()

    # Calculate accuracy
    accuracy = (correct_reps / total_reps) * 100 if total_reps > 0 else 0

    return output_path, feedback, correct_reps, accuracy


# Django view to handle video upload and processing
def exercise_video(request):
    video_url = None
    feedback = ""
    count = 0
    accuracy = 0

    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']
        exercise_type = request.POST.get('exercise_type', "Unknown")

        # Save uploaded video file
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(video_file.name, video_file)
        video_file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Process the video and analyze exercise
        output_video_path, feedback, count, accuracy = handle_exercise_detection(video_file_path, exercise_type)

        # Get URL for the processed video
        video_url = fs.url(output_video_path)

    return render(request, 'exercise.html', {
        'video_url': video_url,
        'feedback': feedback,
        'count': count,
        'accuracy': accuracy
    })
