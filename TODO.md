# Meeting Room Manager - Implementation TODO

## Custom Sorting Algorithm Implementation

### 1. Create Sorting Algorithms Module

- [ ] Create `sorting_algorithms.py` file
- [ ] Implement recursive QuickSort for rooms
- [ ] Implement recursive MergeSort for employees
- [ ] Implement recursive QuickSort for bookings
- [ ] Add helper functions for merging sorted lists

### 2. Update Route Files

- [ ] Modify `routes/rooms.py` to use custom QuickSort instead of SQLAlchemy `order_by()`
- [ ] Modify `routes/bookings.py` to use custom sorting for booking lists
- [ ] Update `routes/dashboard.py` admin dashboard to use custom sorting algorithms
- [ ] Remove all SQLAlchemy `.order_by()` calls and replace with `.all()` + custom sort

### 3. Update Database Queries

- [ ] Change `Room.query.order_by()` to `Room.query.all()` + `quicksort_rooms()`
- [ ] Change `Booking.query.order_by()` to `Booking.query.all()` + `quicksort_bookings()`
- [ ] Change `Employee.query.order_by()` to `Employee.query.all()` + `merge_sort_employees()`

### 4. Test Custom Sorting

- [ ] Test room sorting by floor and name
- [ ] Test booking sorting by time
- [ ] Test employee sorting by last name, first name
- [ ] Verify sorting works in both ascending and descending order
- [ ] Test edge cases (empty lists, single items, duplicate values)

### 5. Update Algorithms Documentation

- [ ] Add QuickSort algorithm to `algorithms.md`
- [ ] Add MergeSort algorithm to `algorithms.md`
- [ ] Include proper pseudocode with recursion clearly shown
- [ ] Document key functions and sorting criteria used

###
