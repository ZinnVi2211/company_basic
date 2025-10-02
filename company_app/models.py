# company_app/models.py

from django.db import models
from django.utils import timezone


# =================================================================
# 1. MODELS CƠ BẢN (Index, About, Service)
# =================================================================

class Index(models.Model):
    # Dữ liệu cho phần Hero Section, Clients, Features, Call To Action, v.v.
    hero_title = models.CharField(max_length=255, default="We are professional")
    hero_subtitle = models.TextField(default="Lorem ipsum dolor sit amet...")

    # Có thể thêm các trường khác như logo client, tính năng chính...

    def __str__(self):
        return "Home Page Content"

    class Meta:
        verbose_name_plural = "Index (Home Page)"


class About(models.Model):
    # Dữ liệu cho trang About
    about_title = models.CharField(max_length=200, default="Who We Are")
    about_description = models.TextField()

    def __str__(self):
        return self.about_title

    class Meta:
        verbose_name_plural = "About Page Content"


class Service(models.Model):
    # Dữ liệu cho danh sách các dịch vụ (ví dụ: Web Design, Marketing, v.v.)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Biểu tượng (ví dụ: bi-briefcase)")
    description = models.TextField()

    def __str__(self):
        return self.name


class ServiceDetail(models.Model):
    # Dữ liệu chi tiết cho từng dịch vụ
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='details')
    detail_point = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.service.name} - {self.detail_point[:30]}"


# =================================================================
# 2. PRICING MODELS
# =================================================================

class PricingPlan(models.Model):
    # Dữ liệu cho các gói giá
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_featured = models.BooleanField(default=False)  # Gói nổi bật

    def __str__(self):
        return self.name


class PricingFeature(models.Model):
    # Dữ liệu cho các tính năng trong mỗi gói giá
    plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, related_name='features')
    feature_text = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)  # Có sẵn hay không (ví dụ: gạch ngang)

    def __str__(self):
        return f"{self.plan.name} - {self.feature_text}"


# =================================================================
# 3. TEAM & TESTIMONIAL MODELS
# =================================================================

class TeamMember(models.Model):
    # Dữ liệu cho trang Đội ngũ (team.html)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/')
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Team Members"


class Testimonial(models.Model):
    # Dữ liệu cho trang Đánh giá/Phản hồi (testimonials.html)
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100)  # Vị trí/Công ty
    image = models.ImageField(upload_to='testimonial_images/')
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])  # Đánh giá 1-5 sao

    def __str__(self):
        return f"Testimonial from {self.author_name}"


# =================================================================
# 4. BLOG MODELS
# =================================================================

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)  # Dùng cho URL thân thiện
    image = models.ImageField(upload_to='blog_images/')
    content = models.TextField()
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # Ví dụ: Web Design, Marketing
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"

    class Meta:
        verbose_name_plural = "Blog Comments"


# =================================================================
# 5. PORTFOLIO MODELS (Nơi chứa PortfolioImage bị lỗi ban đầu)
# =================================================================

class Portfolio(models.Model):
    # Dữ liệu cho trang Portfolio
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, help_text="Ví dụ: App, Product, Branding, Web")  # Dùng để lọc
    client = models.CharField(max_length=100, blank=True, null=True)
    project_date = models.DateField(blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Portfolios"


class PortfolioImage(models.Model):
    # Các ảnh chi tiết cho mỗi dự án Portfolio
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio_images/')
    alt_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.portfolio.name}"

    class Meta:
        verbose_name_plural = "Portfolio Images"


# =================================================================
# 6. CONTACT MODEL
# =================================================================

class Contact(models.Model):
    # Dữ liệu lưu trữ thông tin gửi từ Contact Form
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"