from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year = models.IntegerField()
    address = models.TextField()
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class Room(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)
    room_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.room_number


class RoomAllocation(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )

    allocation_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        room = self.room
        room.occupied = RoomAllocation.objects.filter(room=room).count()

        if room.occupied >= room.capacity:
            room.status = "Occupied"
        else:
            room.status = "Available"

        room.save()

    def __str__(self):
        return f"{self.student.name} - Room {self.room.room_number}"


class Fee(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, default="Pending")
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.amount}"


class Complaint(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="Pending")

    def __str__(self):
        return f"{self.student.name} - {self.title}"