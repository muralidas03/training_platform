from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class Function(models.Model):
	function_name=models.CharField(max_length=100)
	function_id=models.CharField(max_length=100, unique=True,blank=True,null=True)
	description = models.TextField(max_length=800,blank=True, null=True)
	created_by = models.ForeignKey('User', on_delete=models.CASCADE,related_name="Function_created_by")
	created_at = models.DateTimeField(auto_now_add=True)
	update_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True,related_name="Function_update_by")
	update_at = models.DateTimeField(auto_now=True)
     
	def __str__(self):
		return self.function_name 

class Role(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=800,blank=True, null=True)
    permissions = models.ManyToManyField(Function)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE,related_name="Role_created_by")
    update_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True,related_name="Role_update_by")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)       
    def __str__(self):
        return self.name
    
class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("checker", True)
        return self.create_user(email, password, **other_fields)
    
    
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide a valid email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=False, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    password=models.CharField(max_length=100, blank=False, null=False)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    maker = models.BooleanField(default=False)
    checker = models.BooleanField(default=False)
    objects = CustomUserManager()
    REQUIRED_FIELDS = ["first_name"]
    USERNAME_FIELD = "email"
    def __str__(self) -> str:
        return self.email



# class Permission(models.Model):
# 	role = models.ForeignKey(Role, on_delete=models.CASCADE,blank=True, null=True)	
# 	permissions = models.ForeignKey(Function, on_delete=models.CASCADE,blank=True, null=True)	
# 	created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="permission_created_by")
# 	update_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="permission_update_by")
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	update_at = models.DateTimeField(auto_now=True)   