from django.core.mail import send_mail

def send_booking_email(user_email, booking):
    subject = "🎟️ Booking Confirmed"

    message = f"""
    Your booking is confirmed!

    Movie: {booking.movie.title}
    Seats: {booking.seats}
    Amount: ₹{booking.total_price}

    Enjoy your show! 🍿
    """

    send_mail(
        subject,
        message,
        "your_email@gmail.com",
        [user_email],
        fail_silently=False,
    )