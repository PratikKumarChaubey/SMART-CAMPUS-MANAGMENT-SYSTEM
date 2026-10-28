from file_handler import FileHandler
from resource_manager import ResourceManager
from booking_manager import BookingManager
from search_module import (
    linear_search_by_id,
    binary_search_by_id,
    search_by_type,
    search_by_min_capacity
)
from validation_module import SmartCampusError


def show_resources(res_list):
    print("\n--- CAMPUS RESOURCES ---")
    if len(res_list) == 0:
        print("No resources found.")
        return

    print(f"{'ID':<6} | {'Name':<24} | {'Type':<14} | {'Cap':<5} | {'Location':<18} | {'Status'}")
    print("-" * 80)
    for r in res_list:
        print(f"{r.resource_id:<6} | {r.name:<24} | {r.resource_type:<14} | {r.capacity:<5} | {r.location:<18} | {r.availability}")


def show_bookings(book_list):
    print("\n--- STORED BOOKINGS ---")
    if len(book_list) == 0:
        print("No bookings found.")
        return

    print(f"{'BookID':<7} | {'ResID':<6} | {'Date':<11} | {'Time Slot':<12} | {'Booked By'}")
    print("-" * 62)
    for b in book_list:
        slot = f"{b.start_time}-{b.end_time}"
        print(f"{b.booking_id:<7} | {b.resource_id:<6} | {b.date:<11} | {slot:<12} | {b.user}")


def main():
    fh = FileHandler()
    res_mgr = ResourceManager(fh)

    if len(res_mgr.resources) == 0:
        fh.add_sample_data()
        res_mgr.load_from_file()

    book_mgr = BookingManager(res_mgr, fh)

    while True:
        print("\n==============================================")
        print("   SMART CAMPUS RESOURCE MANAGEMENT SYSTEM")
        print("==============================================")
        print("1. Show All Resources")
        print("2. Add New Resource")
        print("3. Remove Resource")
        print("4. Update Resource Status (Available / Not Available)")
        print("5. Search Resource (ID / Type / Capacity)")
        print("6. Show All Bookings")
        print("7. Book a Resource")
        print("8. Cancel a Booking")
        print("0. Exit")
        print("----------------------------------------------")

        choice = input("Enter choice (0-8): ").strip()

        if choice == "1":
            show_resources(res_mgr.resources)

        elif choice == "2":
            try:
                r_id = input("Enter Resource ID (e.g. R107): ")
                name = input("Enter Name: ")
                r_type = input("Enter Type (Classroom/Laboratory/Seminar Hall/Auditorium): ")
                cap = input("Enter Capacity: ")
                loc = input("Enter Location: ")
                status = input("Enter Status (Available / Not Available): ")
                res_mgr.add_resource(r_id, name, r_type, cap, loc, status)
                print("Resource added successfully!")
            except SmartCampusError as e:
                print("Error:", e)

        elif choice == "3":
            r_id = input("Enter Resource ID to remove: ")
            if res_mgr.remove_resource(r_id):
                print("Resource removed successfully!")
            else:
                print("Resource ID not found.")

        elif choice == "4":
            try:
                r_id = input("Enter Resource ID: ")
                status = input("Enter New Status (Available / Not Available): ")
                res_mgr.update_status(r_id, status)
                print("Status updated successfully!")
            except SmartCampusError as e:
                print("Error:", e)

        elif choice == "5":
            print("  1. Search by ID (Linear vs Binary Search)")
            print("  2. Search by Type")
            print("  3. Search by Minimum Capacity")
            sub = input("  Choose search type (1-3): ").strip()

            if sub == "1":
                target = input("  Enter Resource ID: ")
                res1, t_lin = linear_search_by_id(res_mgr.resources, target)
                res2, t_bin = binary_search_by_id(res_mgr.resources, target)
                if res1 is not None:
                    show_resources([res1])
                else:
                    print("  Resource not found.")
                print(f"  Linear Search Time: {t_lin:.4f} ms | Binary Search Time: {t_bin:.4f} ms")

            elif sub == "2":
                t_name = input("  Enter Type: ")
                matches = search_by_type(res_mgr.resources, t_name)
                show_resources(matches)

            elif sub == "3":
                try:
                    c_val = int(input("  Enter Minimum Capacity: "))
                    matches = search_by_min_capacity(res_mgr.resources, c_val)
                    show_resources(matches)
                except ValueError:
                    print("  Please enter a valid number.")

        elif choice == "6":
            show_bookings(book_mgr.bookings)

        elif choice == "7":
            try:
                b_id = input("Enter Booking ID (e.g. B005): ")
                r_id = input("Enter Resource ID (e.g. R101): ")
                user = input("Enter Your Name / Department: ")
                date_str = input("Enter Date (DD-MM-YYYY): ")
                s_time = input("Enter Start Time (HH:MM): ")
                e_time = input("Enter End Time (HH:MM): ")
                book_mgr.add_booking(b_id, r_id, user, date_str, s_time, e_time)
                print("Booking confirmed and saved!")
            except SmartCampusError as e:
                print("Booking Failed:", e)

        elif choice == "8":
            b_id = input("Enter Booking ID to cancel: ")
            if book_mgr.cancel_booking(b_id):
                print("Booking cancelled successfully!")
            else:
                print("Booking ID not found.")

        elif choice == "0":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 0 to 8.")


if __name__ == "__main__":
    main()
