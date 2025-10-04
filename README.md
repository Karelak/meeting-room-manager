---

## 🧩 **Project Overview**

**Title:** Meeting Room Booking System
**Candidate:** Kaarel Part
**Institution:** The College of Richard Collyer

This project is a **Computer Science NEA** (Non-Exam Assessment) focused on designing and developing a **digital meeting room booking system** for the **Civil Aviation Authority (CAA)** office in Crawley. It replaces the current **paper-based manual booking process** with a real-time, automated, and user-friendly web system.

---

## 🏢 **1. Problem Context and Rationale**

### Identified Problem

The current **manual booking process** at the CAA involves emails, paper forms, and noticeboards. This results in:

- Frequent **double bookings**
- **Inaccurate or outdated schedules**
- Heavy **administrative workload**
- No **real-time visibility** of room availability
- No ability for staff to **self-manage bookings**

### Real-World Impact

The inefficiency disrupts productivity across departments and creates unnecessary dependency on admin staff. There is a clear organizational need for a **centralized digital platform**.

---

## 🎯 **2. Project Aims and Objectives**

### Broad Aims

- Create a **web-based booking system** accessible on the CAA intranet.
- Allow staff to **view, book, cancel, and amend** meeting room reservations.
- Display **real-time room availability**.
- **Automate** conflict checking and reduce administrative workload.
- Provide **role-based permissions** for managers, staff, and administrators.
- Enable **on-the-spot bookings** and check-ins via physical room screens using **NFC/ID scanning**.
- Ensure **GDPR compliance** and secure data handling.

### Limitations

- Internal-only system (no external/mobile access).
- No integration with Outlook or Teams.
- Full digital **direct changeover** (no hybrid phase).
- Strict adherence to **Data Protection Act 2018**.

---

## 👥 **3. Stakeholder Analysis**

| Stakeholder               | Needs / Role                                                |
| ------------------------- | ----------------------------------------------------------- |
| **Administrative Staff**  | Reduce manual workload, automate conflict detection.        |
| **General Staff**         | Simple, fast, real-time booking access.                     |
| **Managers/Senior Staff** | Override ability for high-priority bookings.                |
| **IT Department**         | Security, reliability, GDPR compliance.                     |
| **External Visitors**     | Indirect benefit from smoother scheduling and coordination. |

---

## 🔍 **4. Investigation Methods**

### Method 1 – Questionnaires

- **Quantitative data** from employees and admin staff.
- Key findings:

  - Staff book 4–10 meetings/month.
  - Double bookings and scheduling conflicts are common.
  - Admins spend 5–20 minutes per booking.
  - High willingness to adopt a digital solution.

### Method 2 – Interviews

- **Qualitative insights** from both an employee and admin.
- Common issues: wasted time, lack of real-time data, high admin stress, and missed cancellations.
- Desired features: real-time availability, self-service bookings, auto notifications, reliability.

### Method 3 – Observation

- On-site observation at CAA offices.
- Found queues forming at admin desks and recurring double bookings.
- Manual paper-based tracking proved slow and error-prone.

---

## 💡 **5. Working Specification**

**The proposed system will:**

- Be web-based, accessible on the internal CAA network.
- Allow staff to log in and view real-time room availability.
- Enable booking creation, amendment, and cancellation.
- Include **physical check-in screens** at rooms for NFC or ID-based confirmation.
- Assign **role-based permissions** (staff, manager, admin).
- Automatically check for **conflicts and double bookings**.
- Store data securely and comply with **GDPR**.
- Significantly reduce administrative time.

---

## ⚙️ **6. Technical Choices**

| Component               | Choice              | Justification                                           |
| ----------------------- | ------------------- | ------------------------------------------------------- |
| **Language**            | Python              | High familiarity, readability, large support community. |
| **Framework**           | Web Framework       | Lightweight, easy for small-to-medium web apps.         |
| **Templating**          | Templating Engine   | Integrates with framework for dynamic pages.            |
| **Database**            | Relational Database | Simple, file-based, ideal for local deployment.         |
| **Email Notifications** | Email Service API   | Reliable, easy to integrate.                            |

---

## 🧱 **7. Design Overview**

### Decomposition

The system is divided into key functional components:

- **Main Dashboard**
- **Rooms Module**
- **Bookings Management**
- **Admin Dashboard**
- **Notifications System**
- **Support Ticket System**
- **Authentication (Login/Logout)**
- **FAQ/Help Section**

Each sub-system corresponds to one or more of the investigation objectives.

---

## 🖥️ **8. Inputs, Processes, and Outputs**

| Function         | Input                      | Process                   | Output               |
| ---------------- | -------------------------- | ------------------------- | -------------------- |
| Login            | Employee ID + Password     | Validate credentials      | Access system        |
| View Rooms       | Date/time filter           | Query DB                  | Display availability |
| Make Booking     | Booking form               | Validate, check conflicts | Confirmation message |
| Cancel Booking   | Booking ID                 | Update DB, notify users   | Updated schedule     |
| Check-In         | ID/NFC scan                | Update room status        | Confirmation log     |
| Manager Override | Manager ID + Justification | Override rules            | Approved booking     |
| Search Rooms     | Filter criteria            | Filter query              | Matching rooms list  |
| Notifications    | Booking events             | Trigger SMTP              | Email/alert sent     |
| Admin Oversight  | System query               | Retrieve logs             | Usage dashboard      |

---

## 🗂️ **9. Database Design**

### Tables

The database uses an **SQLite relational schema** with foreign key constraints enabled for referential integrity.

- **Employees**

  - `employeeid` (INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE)
  - `fname` (TEXT NOT NULL)
  - `lname` (TEXT NOT NULL)
  - `email` (TEXT NOT NULL)
  - `role` (TEXT NOT NULL DEFAULT 'staff' CHECK (role IN ('staff','senior','admin')))

- **Rooms**

  - `roomid` (INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE)
  - `floor` (INTEGER NOT NULL)
  - `roomname` (TEXT NOT NULL)
  - `capacity` (INTEGER NOT NULL)

- **Bookings**

  - `bookingid` (INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE)
  - `employeeid` (INTEGER NOT NULL, FOREIGN KEY REFERENCES Employees(employeeid) ON DELETE CASCADE ON UPDATE CASCADE)
  - `roomid` (INTEGER NOT NULL, FOREIGN KEY REFERENCES Rooms(roomid) ON DELETE CASCADE ON UPDATE CASCADE)
  - `timebegin` (TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)
  - `timefinish` (TEXT)

- **Notifications**

  - `notificationid` (INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE)
  - `employeeid` (INTEGER NOT NULL, FOREIGN KEY REFERENCES Employees(employeeid) ON DELETE CASCADE ON UPDATE CASCADE)
  - `message` (TEXT NOT NULL)
  - `is_read` (INTEGER NOT NULL)
  - `created_at` (TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)

- **SupportTickets**

  - `ticketid` (INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE)
  - `employeeid` (INTEGER NOT NULL, FOREIGN KEY REFERENCES Employees(employeeid) ON DELETE CASCADE ON UPDATE CASCADE)
  - `adminid` (INTEGER NOT NULL, FOREIGN KEY REFERENCES Admins(adminid) ON DELETE CASCADE ON UPDATE CASCADE)
  - `subject` (TEXT NOT NULL)
  - `message` (TEXT NOT NULL)
  - `created_at` (TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)

- **Admins**
  - `adminid` (INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE)
  - `fname` (TEXT NOT NULL)
  - `lname` (TEXT NOT NULL)
  - `email` (TEXT NOT NULL)

Each table includes defined **primary keys, foreign keys**, and **validation rules** (e.g. NOT NULL, UNIQUE, CHECK constraints).

---

## 🔐 **10. Data Security and Validation**

- Role-based access control (admins, managers, employees).
- GDPR compliance (limited data visibility).
- Validation techniques:

  - SQL constraints (NOT NULL, UNIQUE)
  - Input checks and exception handling
  - Form validation in Python (try/except blocks)

---

## 🧮 **11. Algorithms**

Each subsystem (e.g., booking creation, conflict checking, check-in/out, notifications) is accompanied by algorithmic logic represented in pseudocode within the design document. These govern how the system processes bookings, validates data, manages priorities, and updates room statuses.

---

## ✅ **12. Success Criteria**

The system will be considered successful if:

1. Staff can book, amend, and cancel meetings independently.
2. Room availability updates instantly and accurately.
3. Double bookings are automatically prevented.
4. Admin workload is reduced.
5. Managers can override bookings responsibly.
6. On-the-spot check-ins/out function correctly.
7. Data remains secure and GDPR-compliant.
8. Staff find the system simple and reliable to use.

---

## 📘 **Summary**

This NEA project demonstrates a **real-world system analysis, design, and implementation** cycle. It transforms a **manual paper-based system** into a **streamlined, automated digital platform**, aligning with both technical and organizational requirements.
It effectively integrates **user research, stakeholder feedback, database design, and system planning**, reflecting a complete software development process from **investigation → design → implementation**.

---
