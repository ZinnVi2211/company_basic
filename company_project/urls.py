from django.contrib import admin
from django.urls import path
from company_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # --- Trang Đơn (Static/List) ---
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("blog/", views.blog, name="blog"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("services/", views.services, name="services"),
    path("pricing/", views.pricing, name="pricing"),
    path("team/", views.team, name="team"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("starter_page/", views.starter_page, name="starter_page"),

    # --- Trang Chi Tiết (Dynamic Routing) ---
    path("blog/details/<int:pk>/", views.blog_details, name="blog_details"),
    path("portfolio/details/<int:pk>/", views.portfolio_details, name="portfolio_details"),
    path("service/details/<int:pk>/", views.service_details, name="service_details"),
]