from .models import Employee

#genrate random username for employee
def generate_username(email):
    username = email.split('@')[0]
    try:
        user = Employee.objects.get(username=username)
        username = username + str(user.id)
    except Employee.DoesNotExist:
        pass
    return username