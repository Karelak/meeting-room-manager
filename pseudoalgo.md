# Meeting Room Manager - Core Algorithms

## 1. User Authentication Algorithm

```pseudocode
ALGORITHM authenticateUser(email, password)
BEGIN
    user = findUserByEmail(email)
    IF user EXISTS AND user.password = password THEN
        createUserSession(user.employeeId, user.role)
        RETURN success
    ELSE
        RETURN failure
    END IF
END
```

## 2. Room Booking Conflict Detection Algorithm

```pseudocode
ALGORITHM checkBookingConflict(roomId, startTime, endTime)
BEGIN
    conflictingBookings = findBookingsWhere(
        booking.roomId = roomId AND
        booking.startTime < endTime AND
        booking.endTime > startTime
    )

    IF conflictingBookings.count > 0 THEN
        RETURN true  // Conflict exists
    ELSE
        RETURN false // No conflict
    END IF
END
```

## 3. Booking Validation Algorithm

```pseudocode
ALGORITHM validateBooking(roomId, startTime, endTime, userId)
BEGIN
    // Check if room exists
    room = findRoomById(roomId)
    IF room NOT EXISTS THEN
        RETURN error("Invalid room")
    END IF

    // Validate time format and parse
    TRY
        parsedStartTime = parseDateTime(startTime)
        parsedEndTime = parseDateTime(endTime)
    CATCH dateTimeError
        RETURN error("Invalid date/time format")
    END TRY

    // Check if end time is after start time
    IF parsedEndTime <= parsedStartTime THEN
        RETURN error("End time must be after start time")
    END IF

    // Check if booking is not in the past
    currentTime = getCurrentDateTime()
    IF parsedStartTime < currentTime THEN
        RETURN error("Cannot create bookings in the past")
    END IF

    // Check booking duration limit (8 hours max)
    duration = parsedEndTime - parsedStartTime
    durationHours = duration.toHours()
    IF durationHours > 8 THEN
        RETURN error("Booking duration cannot exceed 8 hours")
    END IF

    // Check for scheduling conflicts
    hasConflict = checkBookingConflict(roomId, startTime, endTime)
    IF hasConflict THEN
        RETURN error("Room is already booked for selected time")
    END IF

    RETURN success
END
```

## 4. User Creation Validation Algorithm

```pseudocode
ALGORITHM validateNewUser(firstName, lastName, email, password, role)
BEGIN
    // Check all fields are provided
    IF firstName.isEmpty() OR lastName.isEmpty() OR
       email.isEmpty() OR password.isEmpty() OR role.isEmpty() THEN
        RETURN error("All fields are required")
    END IF

    // Validate role
    validRoles = ["staff", "senior", "admin"]
    IF role NOT IN validRoles THEN
        RETURN error("Invalid role selected")
    END IF

    // Validate email domain
    IF NOT email.endsWith("@caa.co.uk") THEN
        RETURN error("Email must be a valid @caa.co.uk address")
    END IF

    // Validate password length
    IF password.length < 8 THEN
        RETURN error("Password must be at least 8 characters long")
    END IF

    // Validate name lengths
    IF firstName.length < 2 OR lastName.length < 2 THEN
        RETURN error("Names must be at least 2 characters long")
    END IF

    // Check for existing email
    existingUser = findUserByEmail(email)
    IF existingUser EXISTS THEN
        RETURN error("Email already exists")
    END IF

    RETURN success
END
```

## 5. Room Creation Validation Algorithm

```pseudocode
ALGORITHM validateNewRoom(roomName, floor, capacity)
BEGIN
    // Check all fields are provided
    IF roomName.isEmpty() OR floor.isEmpty() OR capacity.isEmpty() THEN
        RETURN error("All fields are required")
    END IF

    // Validate room name
    IF roomName.length < 1 THEN
        RETURN error("Room name cannot be empty")
    END IF

    // Validate floor is valid integer
    TRY
        floorNumber = parseInt(floor)
    CATCH parseError
        RETURN error("Floor must be a valid number")
    END TRY

    // Validate floor is non-negative
    IF floorNumber < 0 THEN
        RETURN error("Floor must be 0 or greater")
    END IF

    // Validate capacity is valid integer
    TRY
        capacityNumber = parseInt(capacity)
    CATCH parseError
        RETURN error("Capacity must be a valid number")
    END TRY

    // Validate capacity limits
    IF capacityNumber <= 0 THEN
        RETURN error("Capacity must be greater than 0")
    END IF

    IF capacityNumber > 200 THEN
        RETURN error("Capacity cannot exceed 200")
    END IF

    // Check for duplicate room on same floor
    existingRoom = findRoomByFloorAndName(floorNumber, roomName)
    IF existingRoom EXISTS THEN
        RETURN error("Room with this name already exists on this floor")
    END IF

    RETURN success
END
```

## 6. Authorization Check Algorithm

```pseudocode
ALGORITHM checkUserAuthorization(userId, requiredRole, resourceOwnerId)
BEGIN
    user = findUserById(userId)
    IF user NOT EXISTS THEN
        RETURN false
    END IF

    // Admin can access everything
    IF user.role = "admin" THEN
        RETURN true
    END IF

    // Check if user has required role level
    roleHierarchy = ["staff": 1, "senior": 2, "admin": 3]
    userLevel = roleHierarchy[user.role]
    requiredLevel = roleHierarchy[requiredRole]

    IF userLevel >= requiredLevel THEN
        RETURN true
    END IF

    // Check if user owns the resource
    IF resourceOwnerId IS PROVIDED AND user.id = resourceOwnerId THEN
        RETURN true
    END IF

    RETURN false
END
```

## 7. Support Ticket Assignment Algorithm

```pseudocode
ALGORITHM assignSupportTicket(employeeId, subject, message)
BEGIN
    // Find available admin
    availableAdmin = findFirstAdmin()
    IF availableAdmin NOT EXISTS THEN
        RETURN error("No admin available")
    END IF

    // Create support ticket
    ticket = createSupportTicket(
        employeeId: employeeId,
        adminId: availableAdmin.id,
        subject: subject,
        message: message,
        createdAt: getCurrentDateTime()
    )

    saveTicket(ticket)
    RETURN success
END
```

## 8. Room Availability Search Algorithm

```pseudocode
ALGORITHM findAvailableRooms(startTime, endTime, minimumCapacity)
BEGIN
    allRooms = getAllRooms()
    availableRooms = []

    FOR each room IN allRooms DO
        // Check capacity requirement
        IF minimumCapacity IS PROVIDED AND room.capacity < minimumCapacity THEN
            CONTINUE
        END IF

        // Check for booking conflicts
        hasConflict = checkBookingConflict(room.id, startTime, endTime)
        IF NOT hasConflict THEN
            availableRooms.add(room)
        END IF
    END FOR

    RETURN availableRooms
END
```

## 9. User Session Management Algorithm

```pseudocode
ALGORITHM manageUserSession(sessionData)
BEGIN
    // Check if user is logged in
    IF sessionData.employeeId NOT EXISTS THEN
        RETURN false
    END IF

    // Validate session user still exists
    user = findUserById(sessionData.employeeId)
    IF user NOT EXISTS THEN
        clearSession()
        RETURN false
    END IF

    // Update session with current user data
    sessionData.role = user.role
    sessionData.lastActivity = getCurrentDateTime()

    RETURN true
END
```

## 10. Booking Cancellation Algorithm

```pseudocode
ALGORITHM cancelBooking(bookingId, userId, userRole)
BEGIN
    booking = findBookingById(bookingId)
    IF booking NOT EXISTS THEN
        RETURN error("Booking not found")
    END IF

    // Check authorization
    canCancel = (booking.employeeId = userId) OR (userRole = "admin")
    IF NOT canCancel THEN
        RETURN error("You can only cancel your own bookings")
    END IF

    // Perform cancellation
    deleteBooking(bookingId)
    RETURN success
END
```
