from email.message import EmailMessage
import os
import smtplib
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import csv
from .models import UserData, testUserData
from django.core.mail import send_mail


def index(request):
    # Replace with your logic for the index view
    return render(request, 'campaigns/index.html')


def campaign_html_view(request):
    return render(request,'campaign.html')


def index(request):
    return render(request,'index.html')

def upload_csv(request):
    print("Upload csv is called")
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')
            return redirect('upload_csv')

        # Process CSV file
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_url = fs.url(filename)

        # Read and save usernames from CSV to UserData model
        with fs.open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row if exists
            for row in reader:
                username = row[0]  # Assuming username is in the first column
                UserData.objects.create(username=username)

        messages.success(request, f'File "{csv_file.name}" uploaded successfully.')
        return render(request, 'upload.html', {'uploaded_file_url': uploaded_file_url})

    return render(request, 'upload.html')

def add_campaign(request):
    if request.method == 'POST':
        try:
            from_email = request.POST.get('from_email')
            subject = request.POST.get('subject')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            # if not all([from_email, subject, description]):
            #     messages.error(request, 'Please fill in all required fields.')
            #     return redirect('campaign_html')

            # # Save the image if it exists
            # image_path = None
            # if image:
            #     fs = FileSystemStorage()
            #     image_name = fs.save(image.name, image)
            #     image_path = fs.path(image_name)

            # Fetch all email addresses from the database
            email_addresses = testUserData.objects.values_list('username', flat=True)

            # List of recipients
            recipient_list = list(email_addresses)
            print("The recipient_list ",recipient_list)

            # Send email using send_mail function
            send_mail(
                subject,
                description,
                from_email,
                recipient_list,
                fail_silently=False,  # Set to False to see exceptions
                html_message=None,    # Optional HTML message
            )
            print("Sent")

            messages.success(request, 'Emails have been sent successfully.')
            return render(request, 'campaign.html')

        except Exception as e:
            print("Not snet")
            print(f'Failed to send emails: {str(e)}')
            messages.error(request, f'Failed to send emails: {str(e)}')

    return render(request, 'campaign.html')

