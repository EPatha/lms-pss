from ninja import NinjaAPI, UploadedFile, File, Form
from ninja.responses import Response
from lms_core.schema import CourseSchemaOut, CourseMemberOut, CourseSchemaIn
from lms_core.schema import CourseContentMini, CourseContentFull
from lms_core.schema import CourseCommentOut, CourseCommentIn
from lms_core.models import Course, CourseMember, CourseContent, Comment
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja.pagination import paginate, PageNumberPagination

from django.contrib.auth.models import User
from lms_core.schema import UserRegisterIn, UserOut
from django.db import IntegrityError

apiv1 = NinjaAPI()
apiv1.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@apiv1.post("/register/", response={201: UserOut, 400: dict})
def register_user(request, payload: UserRegisterIn):
    try:
        user = User.objects.create_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name
        )
        return 201, UserOut(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
    except IntegrityError:
        return 400, {"error": "Username atau email sudah terdaftar."}

