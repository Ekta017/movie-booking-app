from django.shortcuts import render
from apps.bookings.models import Booking
from django.db.models import Sum, Count


def dashboard(request):
    total_bookings = Booking.objects.count()

    total_revenue = Booking.objects.aggregate(
        total=Sum("total_price")
    )["total"] or 0

    popular_movies = (
        Booking.objects
        .values("movie__title")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    recent_bookings = Booking.objects.select_related("movie", "user").order_by("-created_at")[:5]

    return render(request, "dashboard/dashboard.html", {
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "popular_movies": popular_movies,
        "recent_bookings": recent_bookings
    })