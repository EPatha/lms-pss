from flask import Blueprint, request, jsonify
from lms_core.models import User, db

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Validasi data
    if not all(k in data for k in ("first_name", "last_name", "email", "password")):
        return jsonify({"error": "Missing fields"}), 400
    # Cek email sudah terdaftar
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
    # Simpan user baru
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from .models import Course, Enrollment

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        required = ['first_name', 'last_name', 'email', 'password']
        if not all(k in data for k in required):
            return JsonResponse({'error': 'Missing fields'}, status=400)
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)
        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required
def batch_enroll(request, course_id):
    if request.method == 'POST':
        try:
            course = Course.objects.get(id=course_id, teacher=request.user)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized or course not found'}, status=403)
        data = json.loads(request.body)
        student_ids = data.get('student_ids', [])
        results = []
        for sid in student_ids:
            try:
                student = User.objects.get(id=sid)
                if Enrollment.objects.filter(course=course, student=student).exists():
                    results.append({'student_id': sid, 'status': 'already enrolled'})
                else:
                    Enrollment.objects.create(course=course, student=student)
                    results.append({'student_id': sid, 'status': 'enrolled'})
            except User.DoesNotExist:
                results.append({'student_id': sid, 'status': 'not found'})
        return JsonResponse({'results': results}, status=200)
    return JsonResponse({'error': 'Invalid method'}, status=405)