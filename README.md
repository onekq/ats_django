# Website Entries

## Superuser
http://ats-django.us-west-1.elasticbeanstalk.com/admin

A superuser has already been generated, whose username is "admin", and the assword is "1*******".

## HR
http://ats-django.us-west-1.elasticbeanstalk.com/jobs/login/

HR personnel can create their own accounts by registering to the website, then log in.

## Applicants
http://ats-django.us-west-1.elasticbeanstalk.com/jobs/apply/

Applicants do not need to login. To apply for a job, they just need to visit the URL above and submit their
names, emails, and resumes.

# Applicant Dashboard

Only logged-in HR personnel are able to view the applicant dashboard. While examining the dashboard, they can
drag an application and drop it to another stage.

# Application Status Checking

After applying for a job, the applicant will receive the application number and passcode in the success page.
To check the application progress, the applicant can visit the following URL and fill in the application number and passcode.

http://ats-django.us-west-1.elasticbeanstalk.com/jobs/check_status/

# Job Requirements

Only superuser can add or modify job requirements. To do so, visit admin URL below, log in as superuser (username "admin"), then add or edit existing **Job requirements** under the **JOBS** section.

http://ats-django.us-west-1.elasticbeanstalk.com/admin
