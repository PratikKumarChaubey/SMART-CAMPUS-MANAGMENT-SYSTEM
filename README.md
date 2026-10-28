# Smart Campus Resource Management System

A 4-member team project building a Python application to streamline the management and booking of shared campus facilities—including classrooms, laboratories, seminar halls, and auditoriums. 

Instead of relying on manual registers or scattered spreadsheets, this system helps faculty, students, and administrators quickly find venues that match their required seating capacity, check real-time availability, and prevent double bookings.

---

## Project Objectives (Our Plan)
Our goal is to build a clean, menu-driven system that can:
- **Centralize Resource Data:** Store and manage venue details including ID, name, type, seating capacity, location, and availability status (`Available` / `Not Available`).
- **Manage Campus Venues:** Allow administrators to add new resources, remove existing ones, and update availability statuses (e.g., when a lab is under maintenance).
- **Search Efficiently:** Filter venues by ID, room type, or minimum seating capacity, while comparing **Linear Search O(n)** and **Binary Search O(\log n)** execution times.
- **Prevent Double Bookings:** Allow users to reserve venues for specific dates and time slots (`HH:MM`), automatically detecting and blocking overlapping reservations.
- **Persist Data Automatically:** Save all resource and booking records permanently to local `CSV` and `JSON` files so data is never lost when the program closes.

---

## Current Progress (MVP Prototype)
we have built a working **Minimum Viable Product (MVP)** around 40-50% of working code, using Python's built-in standard library (`csv`, `json`, `os`, `datetime`, `time`). 

- **Completed as of now:** Core Object-Oriented Design (OOP), File Handling (`CSV`/`JSON`), Input Validation & Custom Exceptions, Linear vs. Binary Search, and Booking with Conflict Detection.
- **Scheduled next:** Advanced usage statistics (most/least utilized rooms, peak hours) and data visualization using `Pandas` and `Matplotlib`.

---

## System Architecture & Program Flow

```text
+-------------------------------------------------------------------------+
|                         USER / CONSOLE (main.py)                        |
|               Displays menu (0-8) & collects user input                 |
+------------------------------------+------------------------------------+
                                     |
         +---------------------------+---------------------------+
         |                           |                           |
         v                           v                           v
+------------------+       +-------------------+       +------------------+
| search_module.py |       |resource_manager.py|       |booking_manager.py|
| Linear & Binary  |<------|  OOP Resource &   |<------|  Checks room ID  |
| search on        |       | Subclass Registry |       |  & availability  |
| res_mgr.resources|       | (List, Set, Dict) |       |  via get_by_id() |
+------------------+       +---------+---------+       +---------+--------+
                                     |                           |
                                     +-------------+-------------+
                                                   |
                                                   v
                                     +---------------------------+
                                     |   validation_module.py    |
                                     | Gatekeeper: checks types, |
                                     | capacities, dates & times |
                                     +-------------+-------------+
                                                   |
                                                   v
                                     +---------------------------+
                                     |      file_handler.py      |
                                     |  Persistent Storage Layer |
                                     | Reads/writes Dictionaries |
                                     | to CSV & JSON on hard disk|
                                     +---------------------------+
