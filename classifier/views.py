from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ImageUploadForm
from .models import UploadedImage



# Demo predict function (sau này thay bằng model ML thật)
def predict_image(image_file):
    # giả lập kết quả
    return {
        "label": "Cat",
        "confidence": 0.92
    }

def home_view(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("upload")
        else:
                return render(request, "login.html", {"error": "Sai tài khoản hoặc mật khẩu"})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def upload_view(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            result = predict_image(image)

            UploadedImage.objects.create(
                user=request.user,
                image=image,
                prediction=result["label"],
                confidence=result["confidence"]
            )

            request.session["result"] = result
            request.session["image_name"] = image.name
            return redirect("result")
    else:
        form = ImageUploadForm()

    return render(request, "upload.html", {"form": form})


@login_required
def history_view(request):
    histories = (
        UploadedImage.objects
        .filter(user=request.user)
        .order_by("-uploaded_at")
    )

    return render(request, "history.html", {
        "histories": histories
    })



@login_required
def result_view(request):
    result = request.session.get("result")
    image_name = request.session.get("image_name")

    if not result:
        return redirect("upload")

    return render(request, "result.html", {
        "result": result,
        "image_name": image_name
    })

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # validate cơ bản
        if not username or not password or not confirm_password:
            return render(request, "signup.html", {
                "error": "Vui lòng nhập đầy đủ thông tin"
            })

        if password != confirm_password:
            return render(request, "signup.html", {
                "error": "Mật khẩu xác nhận không khớp"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username đã tồn tại"
            })

        # tạo user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # auto login sau khi đăng ký
        login(request, user)
        return redirect("upload")

    return render(request, "signup.html")
