from email.message import EmailMessage
import os
import smtplib
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import csv
from .models import UserData, testUserData


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

            if not all([from_email, subject, description]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('campaign_html')

            # Save the image if it exists
            image_path = None
            if image:
                fs = FileSystemStorage()
                image_name = fs.save(image.name, image)
                image_path = fs.path(image_name)

            # Fetch all email addresses from the database
            email_addresses = testUserData.objects.values_list('username', flat=True)
            
            # Send emails to all addresses
            for email in email_addresses:
                try:
                    email_message = EmailMessage()
                    email_message['Subject'] = subject
                    email_message['From'] = from_email
                    email_message['To'] = email
                    email_message.set_content(description)
                    print("The email_message ",email_message['Subject'])

                    # Attach image if provided
                    if image_path:
                        with open(image_path, 'rb') as f:
                            image_data = f.read()
                        email_message.add_attachment(image_data, maintype='image', subtype='jpeg', filename=image_name)
                    print("Till here no blocker")

                    # Connect to SMTP server and send email
                    smtp = smtplib.SMTP('smtp.gmail.com', 587)
                   
                    smtp.starttls()
                    smtp.login('catherinematthew17@gmail.com', 'cat@hehe')
                  
                    smtp.send_message(email_message)

                    smtp.quit()  # Close SMTP connection

                    print(f"Email sent successfully to {email}")

                except Exception as e:
                    print(f'Failed to send email to {email}: {str(e)}')
                    messages.error(request, f'Failed to send email to {email}: {str(e)}')

            messages.success(request, 'Emails have been sent successfully.')
            return redirect('campaign_html')

        except Exception as e:
            messages.error(request, f'Failed to send emails: {str(e)}')

    return render(request, 'campaign.html')