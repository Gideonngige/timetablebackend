# timetableapp/utils.py
from datetime import datetime, timedelta
import random

SUBJECTS = ["English", "Kiswahili", "Mathematics", "Social Studies", "CRE", "IRE", "Science"]

TEACHERS = {
    "English": "Mr. John",
    "Kiswahili": "Ms. Mary",
    "Mathematics": "Mr. Peter",
    "Social Studies": "Ms. Grace",
    "CRE": "Mr. Samuel",
    "IRE": "Mr. Ali",
    "Science": "Ms. Jane"
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def generate_time_slots():
    slots = []
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("16:00", "%H:%M")
    lesson_duration = timedelta(minutes=35)

    while start_time < end_time:
        end_slot = start_time + lesson_duration

        # Insert short break between 10:35 - 11:05
        if start_time >= datetime.strptime("10:35", "%H:%M") and start_time < datetime.strptime("11:05", "%H:%M"):
            slots.append(("Break", "10:35 AM", "11:05 AM"))
            start_time = datetime.strptime("11:05", "%H:%M")
            continue

        # Insert lunch break between 1:05 - 2:05
        if start_time >= datetime.strptime("13:05", "%H:%M") and start_time < datetime.strptime("14:05", "%H:%M"):
            slots.append(("Lunch", "01:05 PM", "02:05 PM"))
            start_time = datetime.strptime("14:05", "%H:%M")
            continue

        # Normal lesson slot
        slots.append(("Lesson", start_time.strftime("%I:%M %p"), end_slot.strftime("%I:%M %p")))
        start_time = end_slot

    return slots



def distribute_subjects():
    # Shuffle subjects across the week
    subject_pool = SUBJECTS * 10  # more pool to cover many lessons
    random.shuffle(subject_pool)
    return subject_pool


def generate_timetable(classes):
    timetable = {}
    slots = generate_time_slots()

    for school_class in classes:
        timetable[school_class] = {}
        weekly_subjects = distribute_subjects()
        subject_index = 0

        for day in DAYS:
            timetable[school_class][day] = []
            for slot in slots:
                if slot[0] == "Lesson":
                    subject = weekly_subjects[subject_index % len(weekly_subjects)]
                    teacher = TEACHERS[subject]
                    subject_index += 1
                    timetable[school_class][day].append({
                        "time": f"{slot[1]} - {slot[2]}",
                        "subject": subject,
                        "teacher": teacher
                    })
                else:
                    timetable[school_class][day].append({
                        "time": f"{slot[1]} - {slot[2]}",
                        "subject": slot[0],  # Break or Lunch
                        "teacher": "-"
                    })
    return timetable
