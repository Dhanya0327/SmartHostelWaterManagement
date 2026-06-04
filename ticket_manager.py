def create_ticket(room_number, issue):

    ticket = {
        "room_number": room_number,
        "issue": issue,
        "status": "Assigned"
    }

    return ticket