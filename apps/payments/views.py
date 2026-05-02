from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.movies.models import Movie
from apps.bookings.models import Booking, SeatReservation   # ✅ added
from apps.bookings.utils import send_booking_email


@login_required
def payment_page(request):
    data = request.session.get("booking_data")

    if not data:
        return redirect("/")

    movie = Movie.objects.get(id=data["movie_id"])
    seats = data["seats"]
    total_price = len(seats.split(",")) * 150

    return render(request, "payments/payment.html", {
        "movie": movie,
        "seats": seats,
        "price": total_price
    })


@login_required
def payment_success(request):
    data = request.session.get("booking_data")

    if not data:
        return redirect("/")

    movie = Movie.objects.get(id=data["movie_id"])
    seats = data["seats"]
    total_price = len(seats.split(",")) * 150

    # 🔥 Create booking NOW (after payment)
    booking = Booking.objects.create(
        user=request.user,
        movie=movie,
        seats=seats,
        total_price=total_price
    )

    # 📧 Send email
    if request.user.email:
        send_booking_email(request.user.email, booking)

    # 🔥 NEW: Clear temporary seat reservations (IMPORTANT)
    SeatReservation.objects.filter(
        user=request.user,
        movie=movie
    ).delete()

    # 🧹 Clear session
    request.session.pop("booking_data", None)

    return render(request, "bookings/success.html", {"booking": booking})


@login_required
def payment_failed(request):
    return render(request, "payments/failed.html")


from django.views.decorators.csrf import csrf_protect

@csrf_protect
@login_required
def process_payment(request):
    if request.method != "POST":
        return redirect("/")

    card_number = request.POST.get("card_number")
    cvv = request.POST.get("cvv")

    # 🔥 FAKE LOGIC
    if card_number == "1234" and cvv == "123":
        return redirect("payment_success")
    else:
        data = request.session.get("booking_data")

        movie = Movie.objects.get(id=data["movie_id"])
        seats = data["seats"]
        total_price = len(seats.split(",")) * 150

        return render(request, "payments/payment.html", {
            "movie": movie,
            "seats": seats,
            "price": total_price,
            "error": "Payment Failed! Invalid card details"
        })