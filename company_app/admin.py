# company_app/admin.py

from django.contrib import admin
from .models import (
    Index, About, Service, ServiceDetail,
    Blog, BlogComment, Portfolio, PortfolioImage,
    PricingPlan, PricingFeature, TeamMember, Testimonial, Contact
)


# =================================================================
# 1. INLINE MODELS (Dùng cho các Models có quan hệ Foreign Key)
# =================================================================

class ServiceDetailInline(admin.TabularInline):
    """Quản lý các chi tiết của Dịch vụ ngay trong trang chỉnh sửa Service."""
    model = ServiceDetail
    extra = 1

class PricingFeatureInline(admin.TabularInline):
    """Quản lý các tính năng của Gói giá ngay trong trang chỉnh sửa PricingPlan."""
    model = PricingFeature
    extra = 3

class PortfolioImageInline(admin.TabularInline):
    """Quản lý các ảnh liên quan của Dự án ngay trong trang chỉnh sửa Portfolio."""
    model = PortfolioImage
    extra = 1

class BlogCommentInline(admin.TabularInline):
    """Hiển thị và quản lý các bình luận ngay trong bài Blog."""
    model = BlogComment
    extra = 0 # Không tạo form trống mặc định
    readonly_fields = ('name', 'email', 'comment_text', 'date_posted')
    can_delete = True
    show_change_link = True


# =================================================================
# 2. CUSTOM ADMIN CLASSES (Đăng ký và Tùy chỉnh hiển thị)
# =================================================================

@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ('id', 'hero_title')


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'about_title')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    search_fields = ('name',)
    inlines = [ServiceDetailInline] # Liên kết ServiceDetail


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_featured')
    list_filter = ('is_featured',)
    inlines = [PricingFeatureInline] # Liên kết PricingFeature


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')
    search_fields = ('name', 'position')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'author_title', 'rating')
    list_filter = ('rating',)
    search_fields = ('author_name', 'content')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'date_posted')
    list_filter = ('category', 'date_posted')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)} # Tự động tạo slug từ tiêu đề
    inlines = [BlogCommentInline] # Liên kết BlogComment


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'client', 'project_date')
    list_filter = ('category', 'client')
    search_fields = ('name', 'description')
    inlines = [PortfolioImageInline] # Liên kết PortfolioImage


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Dữ liệu liên hệ thường chỉ xem, không sửa
    list_display = ('id', 'name', 'email', 'subject', 'date_submitted')
    list_filter = ('date_submitted',)
    search_fields = ('name', 'email', 'subject', 'message')
    # Chỉ cho phép xem, không cho phép chỉnh sửa tin nhắn đã gửi
    readonly_fields = ('name', 'email', 'subject', 'message', 'date_submitted')