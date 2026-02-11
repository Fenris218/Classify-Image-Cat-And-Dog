from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import threading

from django.db import close_old_connections
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ImageUploadForm
from .models import UploadedImage, PredictionJob
import numpy as np

import tensorflow as tf
import cv2


_MODEL_LOCK = threading.Lock()
_MODEL = None
_EXECUTOR = ThreadPoolExecutor(max_workers=4)
_MODEL_PATH = Path(__file__).resolve().parent / "model.weights.h5"
_DEFAULT_IMG_SIZE = (224, 224)
_CLASS_NAMES = ["Cat", "Dog"]



def _load_model_once():
    global _MODEL
    if _MODEL is None:
        with _MODEL_LOCK:
            if _MODEL is None:
                _MODEL =  tf.keras.models.load_model("cats_dogs_model.keras", compile=False)
    return _MODEL



def predict_image(image_path):
    model = _load_model_once()
    img = cv2.imread(image_path)

    if img is None:
        return {
            "label": None,
            "confidence": None,
            "error": "Không đọc được ảnh. Kiểm tra lại đường dẫn.",
        }

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32") / 255.0   # chuẩn hóa giống lúc train
    img = np.expand_dims(img, axis=0)     # (1, 224, 224, 3)

    prediction = model.predict(img, verbose=0)
    class_id = int(np.argmax(prediction))
    confidence = float(np.max(prediction)) * 100

    return {
        "label": _CLASS_NAMES[class_id],
        "confidence": confidence,
        "error": None,
    }


def _run_prediction_job(job_id):
    close_old_connections()
    PredictionJob.objects.filter(id=job_id).update(status="running")
    try:
        job = PredictionJob.objects.select_related("user").get(id=job_id)
        result = predict_image(job.image.path)

        PredictionJob.objects.filter(id=job_id).update(
            status="done",
            prediction=result["label"],
            confidence=result["confidence"],
            completed_at=timezone.now(),
        )

        UploadedImage.objects.create(
            user=job.user,
            image=job.image,
            prediction=result["label"],
            confidence=result["confidence"],
        )
    except Exception as exc:
        PredictionJob.objects.filter(id=job_id).update(
            status="failed",
            error_message=str(exc),
            completed_at=timezone.now(),
        )
    finally:
        close_old_connections()

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
            job = PredictionJob.objects.create(
                user=request.user,
                image=image,
                status="queued",
            )

            _EXECUTOR.submit(_run_prediction_job, job.id)
            return redirect("result", job_id=job.id)
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
def result_view(request, job_id):
    job = get_object_or_404(PredictionJob, id=job_id, user=request.user)
    return render(request, "result.html", {
        "job": job,
    })


@login_required
def job_status_view(request, job_id):
    job = get_object_or_404(PredictionJob, id=job_id, user=request.user)
    return JsonResponse({
        "status": job.status,
        "label": job.prediction,
        "confidence": job.confidence,
        "error": job.error_message,
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
