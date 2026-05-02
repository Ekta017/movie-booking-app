from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from apps.movies.models import Movie
from .models import Booking, SeatReservation


@login_required
def create_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # 🧹 Remove expired reservations (older than 5 mins)
    SeatReservation.objects.filter(
        reserved_at__lt=timezone.now() - timedelta(minutes=5)
    ).delete()

    # 🔥 Get already booked seats (permanent)
    bookings = Booking.objects.filter(movie=movie)
    booked_seats = []

    for b in bookings:
        if b.seats:
            booked_seats.extend(b.seats.split(","))

    # 🔥 Get temporary reserved seats
    reserved = SeatReservation.objects.filter(movie=movie)
    reserved_seats = [r.seat for r in reserved]

    # 🔥 Combine both (FINAL BLOCKED SEATS)
    all_blocked_seats = booked_seats + reserved_seats

    if request.method == "POST":
        seats = request.POST.get("seats")

        # ⚠️ Safety check
        if not seats:
            return render(request, "bookings/book.html", {
                "movie": movie,
                "booked_seats": all_blocked_seats,
                "error": "Please select at least one seat"
            })

        seat_list = seats.split(",")

        # 🔥 Prevent double booking (check BOTH booked + reserved)
        for seat in seat_list:
            if seat in all_blocked_seats:
                return render(request, "bookings/book.html", {
                    "movie": movie,
                    "booked_seats": all_blocked_seats,
                    "error": f"Seat {seat} already taken!"
                })

        # 🔥 TEMPORARY RESERVATION (NEW LOGIC)
        for seat in seat_list:
            SeatReservation.objects.create(
                user=request.user,
                movie=movie,
                seat=seat
            )

        # 🔥 Store booking temporarily in session (NO DB SAVE YET)
        request.session["booking_data"] = {
            "movie_id": movie.id,
            "seats": seats
        }

        # 👉 Redirect to fake payment page
        return redirect("payment_page")

    return render(request, "bookings/book.html", {
        "movie": movie,
        "booked_seats": all_blocked_seats
    })