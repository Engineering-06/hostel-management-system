from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Room,RoomAllocation
from django.shortcuts import render, redirect, get_object_or_404

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

    return render(request, "hostel/login.html")


@login_required
def dashboard(request):

    total_students = Student.objects.count()
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(status="Occupied").count()
    available_rooms = Room.objects.filter(status="Available").count()

    return render(request, "hostel/dashboard.html", {
        "total_students": total_students,
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "available_rooms": available_rooms,
    })


@login_required
def students(request):

    all_students = Student.objects.all().order_by("-id")

    return render(request, "hostel/students.html", {
        "students": all_students
    })


def logout_view(request):
    logout(request)
    return redirect("login")
@login_required
def add_student(request):

    if request.method == "POST":
        Student.objects.create(
            student_id=request.POST["student_id"],
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            course=request.POST["course"],
            branch=request.POST["branch"]
        )

        return redirect("students")

    return render(request, "hostel/add_student.html")
@login_required
def add_student(request):

    if request.method == "POST":

        Student.objects.create(
            student_id=request.POST["student_id"],
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            course=request.POST["course"],
            branch=request.POST["branch"],
            year=request.POST["year"]
        )

        return redirect("students")

    return render(request, "hostel/add_student.html")
@login_required
def edit_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        student.student_id = request.POST["student_id"]
        student.name = request.POST["name"]
        student.email = request.POST["email"]
        student.phone = request.POST["phone"]
        student.course = request.POST["course"]
        student.branch = request.POST["branch"]
        student.year = request.POST["year"]

        student.save()

        return redirect("students")

    return render(request, "hostel/edit_student.html", {
        "student": student
    })


@login_required
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect("students")

    return render(request, "hostel/delete_student.html", {
        "student": student
    })
@login_required
def rooms(request):
    all_rooms = Room.objects.all().order_by("room_number")

    return render(request, "hostel/rooms.html", {
        "rooms": all_rooms
    })


@login_required
def add_room(request):

    if request.method == "POST":

        Room.objects.create(
            room_number=request.POST["room_number"],
            capacity=request.POST["capacity"],
            status=request.POST["status"]
        )

        return redirect("rooms")

    return render(request, "hostel/add_room.html")
@login_required
def edit_room(request, id):

    room = get_object_or_404(Room, id=id)

    if request.method == "POST":

        room.room_number = request.POST["room_number"]
        room.capacity = request.POST["capacity"]
        room.status = request.POST["status"]

        room.save()

        return redirect("rooms")

    return render(request, "hostel/edit_room.html", {
        "room": room
    })


@login_required
def delete_room(request, id):

    room = get_object_or_404(Room, id=id)

    if request.method == "POST":
        room.delete()
        return redirect("rooms")

    return render(request, "hostel/delete_room.html", {
        "room": room
    })
@login_required
def allocations(request):

    all_allocations = RoomAllocation.objects.all().order_by("-id")

    return render(request, "hostel/allocations.html", {
        "allocations": all_allocations
    })


@login_required
def add_allocation(request):

    students = Student.objects.all()

    rooms = Room.objects.filter(status="Available")

    if request.method == "POST":

        student_id = request.POST["student"]
        room_id = request.POST["room"]

        student = Student.objects.get(id=student_id)
        room = Room.objects.get(id=room_id)

        # Check whether student already has a room
        if RoomAllocation.objects.filter(student=student).exists():
            return render(request, "hostel/add_allocation.html", {
                "students": students,
                "rooms": rooms,
                "error": "This student already has a room allocated."
            })

        # Check room capacity
        current_occupied = RoomAllocation.objects.filter(room=room).count()

        if current_occupied >= room.capacity:
            return render(request, "hostel/add_allocation.html", {
                "students": students,
                "rooms": rooms,
                "error": "This room is already full."
            })

        RoomAllocation.objects.create(
            student=student,
            room=room
        )

        return redirect("allocations")

    return render(request, "hostel/add_allocation.html", {
        "students": students,
        "rooms": rooms
    })
@login_required
def delete_allocation(request, id):

    allocation = get_object_or_404(RoomAllocation, id=id)

    if request.method == "POST":

        room = allocation.room

        allocation.delete()

        # Update occupied count
        room.occupied = RoomAllocation.objects.filter(room=room).count()

        if room.occupied >= room.capacity:
            room.status = "Occupied"
        else:
            room.status = "Available"

        room.save()

        return redirect("allocations")

    return render(request, "hostel/delete_allocation.html", {
        "allocation": allocation
    })