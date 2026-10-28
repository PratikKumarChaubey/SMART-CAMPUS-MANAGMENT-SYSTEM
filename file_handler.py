import csv
import json
import os

RESOURCE_COLUMNS = ["resource_id", "name", "resource_type", "capacity", "location", "availability"]
BOOKING_COLUMNS = ["booking_id", "resource_id", "user", "date", "start_time", "end_time"]


class FileHandler:
    def __init__(self, folder_name="data"):
        self.folder_name = folder_name
        self.res_csv = os.path.join(folder_name, "resources.csv")
        self.book_csv = os.path.join(folder_name, "bookings.csv")
        self.res_json = os.path.join(folder_name, "resources.json")
        self.book_json = os.path.join(folder_name, "bookings.json")
        self.setup_files()

    def setup_files(self):
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
        if not os.path.exists(self.res_csv):
            self.save_resources([])
        if not os.path.exists(self.book_csv):
            self.save_bookings([])

    def save_resources(self, res_list):
        with open(self.res_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=RESOURCE_COLUMNS)
            writer.writeheader()
            writer.writerows(res_list)

        with open(self.res_json, mode="w", encoding="utf-8") as f:
            json.dump(res_list, f, indent=4)

    def load_resources(self):
        if not os.path.exists(self.res_csv):
            return []
        data = []
        try:
            with open(self.res_csv, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["capacity"] = int(row["capacity"])
                    data.append(row)
        except Exception as e:
            print("Warning: Could not read resources file properly:", e)
        return data

    def save_bookings(self, book_list):
        with open(self.book_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=BOOKING_COLUMNS)
            writer.writeheader()
            writer.writerows(book_list)

        with open(self.book_json, mode="w", encoding="utf-8") as f:
            json.dump(book_list, f, indent=4)

    def load_bookings(self):
        if not os.path.exists(self.book_csv):
            return []
        data = []
        try:
            with open(self.book_csv, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print("Warning: Could not read bookings file properly:", e)
        return data

    def add_sample_data(self):
        sample_res = [
            {"resource_id": "R101", "name": "Room 101 Lecture Hall", "resource_type": "Classroom", "capacity": 60, "location": "Block A, Floor 1", "availability": "Available"},
            {"resource_id": "R102", "name": "Room 102 Smart Room", "resource_type": "Classroom", "capacity": 80, "location": "Block A, Floor 1", "availability": "Available"},
            {"resource_id": "R103", "name": "Python Lab 1", "resource_type": "Laboratory", "capacity": 45, "location": "CS Block, Floor 2", "availability": "Available"},
            {"resource_id": "R104", "name": "Main Seminar Hall", "resource_type": "Seminar Hall", "capacity": 200, "location": "Admin Block", "availability": "Available"},
            {"resource_id": "R105", "name": "Auditorium", "resource_type": "Auditorium", "capacity": 500, "location": "Central Block", "availability": "Available"},
            {"resource_id": "R106", "name": "Hardware Lab", "resource_type": "Laboratory", "capacity": 35, "location": "ECE Block", "availability": "Not Available"}
        ]
        sample_book = [
            {"booking_id": "B001", "resource_id": "R101", "user": "Dr. Sharma", "date": "28-10-2026", "start_time": "09:00", "end_time": "11:00"},
            {"booking_id": "B002", "resource_id": "R103", "user": "Prof. Verma", "date": "28-10-2026", "start_time": "10:00", "end_time": "12:00"},
            {"booking_id": "B003", "resource_id": "R104", "user": "IEEE Club", "date": "28-10-2026", "start_time": "14:00", "end_time": "16:00"}
        ]
        self.save_resources(sample_res)
        self.save_bookings(sample_book)
