from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate
from email2.models import User
import random
from email2.serializers import UserRegistrationSerializer, UserLoginSerializer, UserOTPVerifySerializer 

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        id = random.randint(100000, 999999)        
        email = serializer.validated_data['email']
        
        
        # Check if the user already exists in the database
        try:
            user = User.objects.get(email=email)
            return Response({'error': 'User already exists. Please log in.'}, status=400)
        except User.DoesNotExist:
            pass
        
        # Generate OTP
        otp = str(random.randint(1000, 9999))  # Generate a random 4-digit number

        # Create the email message object
        subject = 'OTP Verification'
        text = f'Your OTP: {otp}'
        from_email = 'surendharcloud168@gmail.com'
        to_emails = [email]

        msg = EmailMultiAlternatives(subject, text, from_email, to_emails)

        try:
            # Send the email
            msg.send()
            user = User(id=id, email=email, otp=otp)
            user.save()

            return Response({'message': 'Email sent successfully and user registered'})
        except Exception as e:
            return Response({'error': f'An error occurred while sending the email: {str(e)}'}, status=500)
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def otp_verify(request):
    serializer = UserOTPVerifySerializer(data=request.data)
    if serializer.is_valid():
        email= serializer.validated_data['email']    
        otp = serializer.validated_data['otp']
        try:
            user = User.objects.get(otp=otp,email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found. Please register first.'}, status=400)

        # Update the user's email_status field
        user.email_status = 'Active'
        user.otp = None  # Clear the OTP field
        user.password = 'Password'
        user.save()

        return Response({'message': 'Status activated successfully'})

    return Response(serializer.errors, status=400)




@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        users = User.objects.filter(email=email)

        if not users:
            return Response({'error': 'User not found. Please register first.'}, status=400)

        active_users = [user for user in users if user.email_status == 'Active']

        if not active_users:
            return Response({'error': 'Please verify your OTP'}, status=400)
        
        '''
        user = User.updateOne({email : email}, {'$set':{password : password}})
        user.save()
        '''
            
        for user in active_users:
            
            user.password = password
            user.save()
            
            response_data = {
                'message': 'Login successful',
                'email': email,
                'password': password
                }
            return Response(response_data)

        return Response({'error': 'Invalid password'}, status=400)

    return Response(serializer.errors, status=400)
