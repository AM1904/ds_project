class Teacher:
    def __init__(self, teacher_id: int, name: str, subject: str, max_hours: int):
        self.teacher_id = teacher_id
        self.name = name
        self.subject = subject
        self.max_hours = max_hours

    def __eq__(self, other):
        return isinstance(other, Teacher) and self.teacher_id == other.teacher_id

    def __str__(self):
        return (f"  Teacher  | ID: {self.teacher_id:<3} | Name: {self.name:<20} "
                f"| Subject: {self.subject:<15} | MaxHrs/Week: {self.max_hours}")


class Course:
    def __init__(self, course_id: int, name: str, teacher_name: str, hours_per_week: int):
        self.course_id = course_id
        self.name = name
        self.teacher_name = teacher_name
        self.hours_per_week = hours_per_week

    def __eq__(self, other):
        return isinstance(other, Course) and self.course_id == other.course_id

    def __str__(self):
        return (f"  Course   | ID: {self.course_id:<3} | Name: {self.name:<25} "
                f"| Teacher: {self.teacher_name:<20} | Hrs/Week: {self.hours_per_week}")


class Classroom:
    def __init__(self, room_id: int, room_number: str, capacity: int):
        self.room_id = room_id
        self.room_number = room_number
        self.capacity = capacity

    def __eq__(self, other):
        return isinstance(other, Classroom) and self.room_id == other.room_id

    def __str__(self):
        return (f"  Classroom| ID: {self.room_id:<3} | Room No: {self.room_number:<10} "
                f"| Capacity: {self.capacity} students")


class TimeSlot:
    def __init__(self, slot_id: int, day: str, start_time: str, end_time: str):
        self.slot_id = slot_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        return isinstance(other, TimeSlot) and self.slot_id == other.slot_id

    def __str__(self):
        return (f"  TimeSlot | ID: {self.slot_id:<3} | Day: {self.day:<10} "
                f"| {self.start_time} - {self.end_time}")
