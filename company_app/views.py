# company_app/views.py (Nội dung mới)

from django.shortcuts import render,  get_object_or_404, redirect

# Import TẤT CẢ Models để sử dụng
from .models import (
    Index, About, Service, ServiceDetail, Blog, Portfolio,
    PricingPlan, TeamMember, Testimonial, Contact
)


# --- CORE PAGES ---

def index(request):
    # Truy vấn dữ liệu cho các phần trên trang chủ
    accIndex = Index.objects.first()
    accService = Service.objects.all()[:4]  # Lấy 4 dịch vụ
    accPortfolio = Portfolio.objects.all()[:6]  # Lấy 6 dự án
    accBlog = Blog.objects.all().order_by('-date_posted')[:3]  # Lấy 3 bài blog mới nhất
    accTestimonials = Testimonial.objects.all()

    context = {
        'title': 'Trang Chủ',
        'accIndex': accIndex,
        'accService': accService,
        'accPortfolio': accPortfolio,
        'accBlog': accBlog,
        'accTestimonials': accTestimonials,
    }
    return render(request, 'index.html', context=context)


def about(request):
    accAbout = About.objects.first()
    accTeam = TeamMember.objects.all()
    accTestimonials = Testimonial.objects.all()
    context = {
        'title': 'Về Chúng Tôi',
        'accAbout': accAbout,
        'accTeam': accTeam,
        'accTestimonials': accTestimonials,
    }
    return render(request, 'about.html', context=context)


def contact(request):
    return render(request, 'contact.html', {'title': 'Liên Hệ'})


def starter_page(request):
    return render(request, 'starter_page.html', {'title': 'Trang Khởi Đầu'})


# --- LIST PAGES (Danh sách) ---

def services(request):
    accService = Service.objects.all()
    context = {
        'title': 'Dịch Vụ',
        'accService': accService,
    }
    return render(request, 'services.html', context=context)


def blog(request):
    accBlog = Blog.objects.all()
    return render(request, 'blog.html', {'title': 'Blog', 'accBlog': accBlog})


def portfolio(request):
    accPortfolio = Portfolio.objects.all()
    return render(request, 'portfolio.html', {'title': 'Dự Án', 'accPortfolio': accPortfolio})


def pricing(request):
    # Sử dụng prefetch_related để tối ưu việc truy vấn các tính năng (features)
    accPricing = PricingPlan.objects.all().prefetch_related('features')
    return render(request, 'pricing.html', {'title': 'Bảng Giá', 'accPricing': accPricing})


def team(request):
    accTeam = TeamMember.objects.all()
    return render(request, 'team.html', {'title': 'Đội Ngũ', 'accTeam': accTeam})


def testimonials(request):
    accTestimonials = Testimonial.objects.all()
    return render(request, 'testimonials.html', {'title': 'Phản Hồi Khách Hàng', 'accTestimonials': accTestimonials})


# --- DETAIL PAGES (Chi tiết) ---

def service_details(request, pk):
    # Lấy đối tượng Service hoặc trả về lỗi 404 nếu không tìm thấy
    service = get_object_or_404(Service, pk=pk)
    accService = Service.objects.all()  # Dùng cho danh sách bên sidebar

    context = {
        'title': service.name,
        'service': service,
        'accService': accService,
    }
    return render(request, 'service-details.html', context=context)


def blog_details(request, pk):
    # Lấy đối tượng Blog
    post = get_object_or_404(Blog, pk=pk)
    # Lấy 5 bài viết gần đây, loại trừ bài hiện tại
    recent_posts = Blog.objects.exclude(pk=pk).order_by('-date_posted')[:5]

    context = {
        'title': post.title,
        'post': post,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog_details.html', context=context)


def portfolio_details(request, pk):
    # Lấy đối tượng Portfolio
    project = get_object_or_404(Portfolio, pk=pk)
    # Lấy tất cả ảnh của dự án (nếu bạn dùng related_name là 'images' trong models.py)
    images = project.portfolioimage_set.all()

    context = {
        'title': project.name,
        'project': project,
        'images': images,
    }
    return render(request, 'portfolio_details.html', context=context)


# --- THÊM LOGIC XỬ LÝ FORM LIÊN HỆ ---
def contact(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Kiểm tra dữ liệu và lưu vào database
        if name and email and subject and message:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            # Thêm thông báo thành công (cần import message từ django.contrib)
            # from django.contrib import messages
            # messages.success(request, 'Tin nhắn của bạn đã được gửi thành công!')

            # Tùy chọn: Chuyển hướng về trang liên hệ hoặc trang chủ
            return render(request, 'contact.html', {'message_sent': True})
        else:
            # Xử lý lỗi (ví dụ: thiếu trường dữ liệu)
            return render(request, 'contact.html', {'error_message': 'Vui lòng điền đầy đủ thông tin.'})

    # Xử lý GET request (lần đầu truy cập trang)
    return render(request, 'contact.html')