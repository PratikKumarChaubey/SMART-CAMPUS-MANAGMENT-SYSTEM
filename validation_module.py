from datetime import datetime


class SmartCampusError(Exception):
    pass


class InvalidInputError(SmartCampusError):
    pass


class BookingConflictError(SmartCampusError):
    pass


def check_resource_data(res_id, name, res_type, capacity, location, status):
    if str(res_id).strip() == "":
        raise InvalidInputError("Resource ID cannot be empty.")
    if str(name).strip() == "":
        raise InvalidInputError("Resource name cannot be empty.")
    if str(res_type).strip() == "":
        raise InvalidInputError("Resource type cannot be empty.")

    try:
        cap_num = int(capacity)
    except ValueError:
        raise InvalidInputError("Capacity must be a whole number.")

    if cap_num <= 0:
        raise InvalidInputError("Capacity must be greater than 0.")

    if str(location).strip() == "":
        raise InvalidInputError("Location cannot be empty.")

    clean_status = str(status).strip().title()
    if clean_status != "Available" and clean_status != "Not Available":
        raise InvalidInputError("Status must be 'Available' or 'Not Available'.")

    return clean_status


def check_booking_data(book_id, res_id, user_name, date_text, start_time, end_time):
    if str(book_id).strip() == "" or str(res_id).strip() == "" or str(user_name).strip() == "":
        raise InvalidInputError("Booking ID, Resource ID, and User Name cannot be empty.")

    try:
        datetime.strptime(date_text, "%d-%m-%Y")
    except ValueError:
        raise InvalidInputError("Wrong date format. Please use DD-MM-YYYY.")

    try:
        t1 = datetime.strptime(start_time, "%H:%M")
        t2 = datetime.strptime(end_time, "%H:%M")
    except ValueError:
        raise InvalidInputError("Wrong time format. Please use HH:MM (24-hour format).")

    if t2 <= t1:
        raise InvalidInputError("End time must be after start time.")
