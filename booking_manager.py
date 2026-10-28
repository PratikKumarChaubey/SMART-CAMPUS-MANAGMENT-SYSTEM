from validation_module import check_booking_data, InvalidInputError, BookingConflictError


class Booking:
    def __init__(self, booking_id, resource_id, user, date, start_time, end_time):
        check_booking_data(booking_id, resource_id, user, date, start_time, end_time)
        self.booking_id = str(booking_id).strip()
        self.resource_id = str(resource_id).strip()
        self.user = str(user).strip()
        self.date = str(date).strip()
        self.start_time = str(start_time).strip()
        self.end_time = str(end_time).strip()
        self.time_slot = (self.start_time, self.end_time)

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "resource_id": self.resource_id,
            "user": self.user,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time
        }


def check_time_conflict(new_booking, all_bookings):
    for b in all_bookings:
        if b.resource_id == new_booking.resource_id and b.date == new_booking.date:
            if new_booking.start_time < b.end_time and new_booking.end_time > b.start_time:
                raise BookingConflictError(
                    f"Conflict with Booking {b.booking_id}! {b.resource_id} is already booked "
                    f"on {b.date} from {b.start_time} to {b.end_time} by {b.user}."
                )


class BookingManager:
    def __init__(self, res_manager, file_handler):
        self.res_manager = res_manager
        self.file_handler = file_handler
        self.bookings = []
        self.load_from_file()

    def load_from_file(self):
        self.bookings = []
        rows = self.file_handler.load_bookings()
        for r in rows:
            b = Booking(
                r["booking_id"],
                r["resource_id"],
                r["user"],
                r["date"],
                r["start_time"],
                r["end_time"]
            )
            self.bookings.append(b)

    def save_to_file(self):
        dict_list = []
        for b in self.bookings:
            dict_list.append(b.to_dict())
        self.file_handler.save_bookings(dict_list)

    def add_booking(self, book_id, res_id, user, date_text, start_time, end_time):
        clean_id = str(book_id).strip()
        for b in self.bookings:
            if b.booking_id == clean_id:
                raise InvalidInputError("Booking ID already exists.")

        res = self.res_manager.get_by_id(res_id)
        if res is None:
            raise InvalidInputError("Resource ID does not exist.")

        if res.availability != "Available":
            raise InvalidInputError("This resource is currently Not Available for booking.")

        new_b = Booking(clean_id, res.resource_id, user, date_text, start_time, end_time)
        check_time_conflict(new_b, self.bookings)

        self.bookings.append(new_b)
        self.save_to_file()
        return new_b

    def cancel_booking(self, book_id):
        clean_id = str(book_id).strip()
        found = False
        new_list = []

        for b in self.bookings:
            if b.booking_id == clean_id:
                found = True
            else:
                new_list.append(b)

        if found:
            self.bookings = new_list
            self.save_to_file()
        return found
