# IFI App - Insight for Innovation Backend

A comprehensive Frappe/ERPNext application for managing educational volunteer programs. This backend powers the IFI mobile application, providing role-based access for Volunteers, Quality Assurance personnel, Coordinators, and District Coordinators.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [DocTypes](#doctypes)
- [API Documentation](#api-documentation)
- [User Roles & Permissions](#user-roles--permissions)
- [Authentication Flow](#authentication-flow)
- [Custom Workflows](#custom-workflows)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

**IFI App** is the backend system for a volunteer-driven educational initiative. Built on the Frappe Framework, it provides:

- **Multi-role user management** (Volunteer, QA, Coordinator, District Coordinator)
- **Student tracking and performance monitoring**
- **Class session management**
- **Attendance tracking with automatic calculations**
- **Assessment systems** (Maths & English with multiple test levels)
- **Evaluation and quality assurance workflows**
- **Rewards and gamification** using Frappe Energy Points
- **Institution management** (Schools, Colleges, Corporates)
- **Geographic data** (States, Districts)
- **Profile approval workflows**

## Features

### 🔐 Authentication & User Management
- Custom signup with email verification via OTP
- Secure password reset flow with single-use tokens
- API key generation for mobile app authentication
- Role-based access control (RBAC)
- Profile approval workflow using Frappe Workflows

### 👥 Role-Based Features

#### Volunteer
- Manage assigned students
- Submit class sessions with automatic hour calculation (optional)
- Mark bulk attendance for students
- Conduct and submit Maths & English tests
- View student progress and skills assessment
- Earn reward points for activities
- Search and view student details

#### Quality Assurance (QA)
- Search and filter volunteers
- Conduct teachback evaluations
- Perform volunteer assessments
- Access evaluation history
- Review volunteer performance metrics

#### Coordinator
- View school and college statistics
- Access student lists by institution
- Monitor volunteer assignments
- Track institutional performance

#### District Coordinator
- Add new institutions (Schools, Colleges, Corporates)
- Map schools to colleges
- Assign volunteers to schools
- View mapping statistics and details
- Manage district-level operations

### 📊 Data Management
- **Student Management**: Complete student profiles with skills assessment (8 skill categories)
- **Attendance Tracking**: Automatic attendance percentage calculation on student records
- **Assessment System**:
  - Maths: Initial and Final tests with topic-wise tracking
  - English: Initial, Intermediate, and Final tests with grade levels
  - Bulk mark submission with create/update logic
- **Class Sessions**: Track session date, time, duration, topics, and modules
- **Rewards System**: Integrated with Frappe Energy Points for gamification
- **Profile Images**: Custom avatar selection system

### 🔄 Custom Workflows
- **UserSignup Approval**: Draft → Approval Pending → Approved
- **Auto-creation**: Approved UserSignups automatically create AppUser records with unique IFI ID

### 🔔 Notifications
- FCM (Firebase Cloud Messaging) token management for push notifications
- Email notifications for OTP verification
- System notifications for workflow actions

## Architecture

### Technology Stack
- **Framework**: Frappe Framework (Python-based)
- **Database**: MariaDB/MySQL
- **ORM**: Frappe ORM
- **API**: REST API with whitelisted methods
- **Authentication**: Token-based (API Key/Secret)
- **Queue**: Frappe Background Jobs (Redis)
- **Email**: Frappe Email Queue

### Project Structure

```
IFIApp/
├── ifiapp/
│   ├── ifiapi.py                      # Custom API endpoints
│   ├── hooks.py                       # App hooks and configurations
│   ├── config/                        # Desktop and module configurations
│   ├── fixtures/                      # Default data (States, Districts, etc.)
│   ├── ifiapp/
│   │   └── doctype/                   # All DocType definitions
│   │       ├── appuser/               # Approved user profiles
│   │       ├── attendance/            # Student attendance records
│   │       ├── class/                 # Class master (4-10)
│   │       ├── classsession/          # Volunteer session records
│   │       ├── student/               # Student master with skills
│   │       ├── evaluation/            # QA evaluation records
│   │       ├── mathsmark/             # Maths test scores (child table)
│   │       ├── englishmark/           # English test scores (child table)
│   │       ├── reward/                # Reward records
│   │       ├── school/                # School master
│   │       ├── college/               # College master
│   │       ├── corporate/             # Corporate master
│   │       ├── mappedschools/         # School-College mapping (child table)
│   │       ├── states/                # State master
│   │       ├── districts/             # District master
│   │       ├── ifimodule/             # Learning modules master
│   │       ├── topic/                 # Topics master
│   │       ├── question/              # Assessment questions master
│   │       ├── questiontable/         # Question mapping (child table)
│   │       ├── usersignups/           # User registration requests
│   │       └── profileimages/         # Avatar images master
│   └── templates/                     # Web templates (if any)
└── pyproject.toml                     # Python project configuration
```

## Installation

### Prerequisites
- Frappe Bench installed
- Python 3.10+
- MariaDB 10.6+ or MySQL 8.0+
- Redis
- Node.js 18+ (for frontend assets)

### Setup

1. **Get the app**
```bash
cd frappe-bench
bench get-app https://github.com/JinsoRaj/IFIApp.git
```

2. **Install on site**
```bash
bench --site your-site.local install-app ifiapp
```

3. **Run migrations**
```bash
bench --site your-site.local migrate
```

4. **Import fixtures** (States, Districts, Classes, etc.)
```bash
bench --site your-site.local import-doc --path apps/ifiapp/ifiapp/fixtures
```

5. **Start development server**
```bash
bench start
```

## Configuration

### System Settings

Configure in Frappe System Settings:
- **reset_password_link_expiry_duration**: OTP expiry time (default: 1800 seconds / 30 minutes)

### Email Configuration

Configure SMTP settings in Email Account:
```
Email ID: your-email@domain.com
SMTP Server: smtp.gmail.com
Port: 587
Use TLS: Yes
```

### Fixtures Included

The app includes pre-configured data:
- **States**: Indian states
- **Districts**: Indian districts
- **Classes**: 4 to 10
- **Colleges**: Sample institutions
- **Corporates**: Sample corporates
- **Topics & Modules**: Learning curriculum
- **Questions**: Sample assessment questions
- **Roles**: Volunteer, Coordinator, Quality Assurance, District Coordinator, ifiuser, ifiadmin
- **Workflows**: UserApproval workflow
- **Energy Point Rules**: Reward point rules

## DocTypes

### Core DocTypes

#### AppUser
Stores approved user profiles with roles and permissions.

**Key Fields**:
- `ifi_id`: Unique identifier (IFI-XXXXXX)
- `user_details`: Link to UserSignups
- `full_name`, `gender`, `ph_number`, `email_id`
- `state`, `district`, `college_name`
- `is_volunteer`, `is_coordinator`, `is_qa`, `is_dis_coordinator`: Role flags
- `points_gained`: Total reward points
- `schools`: Table of mapped schools (for District Coordinators)
- `students_list`: Table of assigned students (for Volunteers)

**Auto-naming**: By field `user_details`

#### Student
Student master with skills assessment and academic tracking.

**Key Fields**:
- `full_name`, `gender`, `contact_number`
- `school_name`, `school_district`, `class_name`, `grade`
- `english_level`, `maths_level`
- `total_attendance`: Auto-calculated attendance percentage
- Skills (8 types): `visual_spatial`, `linguistic_verbal`, `interpersonal`, `intrapersonal`, `logical_mathematical`, `musical`, `bodily_kinesthetic`, `naturalistic`
- `maths_marks`: Child table (MathsMark)
- `english_marks`: Child table (EnglishMark)

**Auto-naming**: `STUD-.YYYY.-` (e.g., STUD-2024-00001)

#### Attendance
Daily attendance records for students.

**Key Fields**:
- `student_id`: Link to Student
- `is_present`: True/False
- `date`: Auto-set on creation

**Hooks**: Updates `total_attendance` on Student on save

#### ClassSession
Records of volunteer teaching sessions.

**Key Fields**:
- `ifi_id`: Volunteer's IFI ID
- `school_name`: Link to School
- `session_date`, `session_start_time`, `session_end_time`
- `session_total_time`: Hours (manually entered)
- `class_name`: Link to Class
- `topic`: Link to Topic
- `module`: Link to IFIModule
- `session_strength`: Number of students

#### MathsMark (Child Table)
Stores Maths test scores for students.

**Key Fields**:
- `topic`: Link to Topic
- `initial_test_mark`, `initial_total_mark`
- `final_test_mark`, `final_total_mark`

**Parent**: Student (`maths_marks` field)

#### EnglishMark (Child Table)
Stores English test scores for students.

**Key Fields**:
- `topic`: Link to Topic
- `initial_test_mark`, `initial_total_mark`, `initial_grade_level`
- `intermediate_test_mark`, `intermediate_total_mark`, `intermediate_grade_level`
- `final_test_mark`, `final_total_mark`, `final_grade_level`

**Parent**: Student (`english_marks` field)

#### Evaluation
QA evaluation records for volunteers.

**Key Fields**:
- `ifi_id`: Volunteer's IFI ID (evaluatee)
- `evaluator_id`: QA's IFI ID
- `volunteer`, `evaluator`: Auto-filled from IFI IDs
- `full_name`, `profile_pic`: Auto-filled from volunteer
- `evaluation_date`, `evaluation_time`
- `evaluation_mode`: Online/Offline
- `table_questions`: Child table (QuestionTable)
- `final_score`: Auto-calculated from questions

#### Reward
Reward records for volunteers.

**Key Fields**:
- `ifi_id`: Volunteer's IFI ID
- `app_user`: Auto-filled from IFI ID
- Reward type fields (dynamic based on reward)

**Hooks**: Creates Energy Point Log entry

#### School, College, Corporate
Institution masters.

**Common Fields**:
- `institution_name`
- `district`: Link to Districts
- `address`, `landmark`
- `contact_number`, `email`

#### UserSignups
User registration requests with approval workflow.

**Key Fields**:
- `email_id`, `full_name`, `ph_number`, `gender`
- `state`, `district`, `college_name`
- `emp_status`: Student/Employee/Un-Employee
- `res_address`, `profile_pic`
- `workflow_state`: Draft/Approval Pending/Approved

**Hooks**: On approval, creates AppUser with unique IFI ID

### Master Data DocTypes

- **States**: Indian states
- **Districts**: Districts within states
- **Class**: Class levels (4-10)
- **IFIModule**: Learning modules
- **Topic**: Subject topics
- **Question**: Assessment questions
- **ProfileImages**: Avatar images

### Child Tables

- **Students**: Links students to volunteers (in AppUser)
- **MappedSchools**: Maps schools to colleges (in AppUser for District Coordinators)
- **QuestionTable**: Links questions to evaluations
- **MathsMark**: Stores maths scores (in Student)
- **EnglishMark**: Stores English scores (in Student)

## API Documentation

For complete API documentation with request/response examples, authentication details, and usage guides, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md).

### Quick API Reference

#### Authentication APIs
- `POST /api/method/ifiapp.ifiapi.sign_up` - User registration
- `POST /api/method/ifiapp.ifiapi.verify_mail` - Verify email OTP
- `POST /api/method/ifiapp.ifiapi.resend_mail` - Resend OTP
- `POST /api/method/ifiapp.ifiapi.app_login` - Mobile app login
- `POST /api/method/ifiapp.ifiapi.verify_otp_code` - Verify OTP (with reset token)
- `POST /api/method/ifiapp.ifiapi.reset_password` - Reset password with token
- `POST /api/method/frappe.client.change_password` - Change password (authenticated)

#### Custom Whitelisted Methods
- `GET /api/method/ifiapp.ifiapp.doctype.appuser.appuser.get_appuser_and_students` - Get volunteer dashboard data
- `POST /api/method/ifiapp.ifiapp.doctype.student.student.manage_student` - Create/Update student
- `GET /api/method/ifiapp.ifiapp.doctype.student.student.get_student_details` - Get student by ID
- `POST /api/method/ifiapp.ifiapp.doctype.attendance.attendance.submit_attendance` - Bulk attendance submission
- `POST /api/method/ifiapp.ifiapp.doctype.mathsmark.mathsmark.bulk_create_or_update_maths_mark_entries` - Bulk maths marks
- `POST /api/method/ifiapp.ifiapp.doctype.englishmark.englishmark.bulk_add_or_update_english_marks` - Bulk English marks
- `POST /api/method/ifiapp.ifiapp.doctype.evaluation.evaluation.send_evaluation` - Submit evaluation
- `POST /api/method/ifiapp.ifiapp.doctype.reward.reward.add_rewards` - Add reward
- `GET /api/method/ifiapp.ifiapp.doctype.reward.reward.get_recent_rewards` - Get recent rewards

#### Standard Frappe REST APIs
All DocTypes support standard Frappe REST operations:
- `GET /api/resource/{DocType}` - List documents
- `GET /api/resource/{DocType}/{name}` - Get document
- `POST /api/resource/{DocType}` - Create document
- `PUT /api/resource/{DocType}/{name}` - Update document
- `DELETE /api/resource/{DocType}/{name}` - Delete document

**Filtering**: Use `filters` parameter with JSON array:
```
filters=[["field","operator","value"]]
```

**Child Table Filtering**:
```
filters=[["ChildTable","field","=","value",false]]
```

## User Roles & Permissions

### Role Hierarchy

1. **System Manager**: Full system access (Frappe default)
2. **ifiadmin**: Administrative access to all IFI doctypes
3. **ifiuser**: Base role for all app users (assigned on email verification)
4. **Volunteer**: Teaching volunteers
5. **Coordinator**: Institution coordinators
6. **Quality Assurance**: QA evaluators
7. **District Coordinator**: District-level administrators

### Role Assignments

Roles are managed in the Frappe User doctype and synchronized to AppUser via hooks:
- On User role update → `add_roles_in_appuser` hook updates role flags in AppUser
- Role flags: `is_volunteer`, `is_coordinator`, `is_qa`, `is_dis_coordinator`

### Permission Rules

**AppUser**:
- System Manager: Full CRUD
- ifiuser: Create, Read, Write, Export, Print, Share
- Volunteer: Read, Write, Delete, Export, Print, Share

**Student**:
- System Manager: Full CRUD
- ifiuser: Read, Write, Export, Print, Share
- Volunteer: Full CRUD, Export, Print, Share

**Attendance, ClassSession, Evaluation, Reward**:
- System Manager: Full CRUD
- Volunteer/QA/Coordinator: Role-specific permissions

**Master Data (School, College, States, Districts, etc.)**:
- Read access for authenticated users
- Write access for District Coordinator and System Manager

### Custom Permissions

Permissions are managed via:
- DocType Permission Rules (in JSON files)
- User Permissions (for district-level data isolation - commented out in code)
- Workflow States (for UserSignups approval)

## Authentication Flow

### 1. Registration & Verification

```
User Registration (sign_up)
    ↓
System creates disabled User with OTP
    ↓
Email sent with 6-digit OTP
    ↓
User verifies email (verify_mail)
    ↓
System enables User and assigns 'ifiuser' role
    ↓
User redirected to profile setup
```

### 2. Profile Setup & Approval

```
User fills UserSignups form
    ↓
Workflow state: Draft
    ↓
User submits for approval
    ↓
Workflow state: Approval Pending
    ↓
Admin approves
    ↓
Workflow state: Approved
    ↓
Hook triggers: add_as_appuser
    ↓
AppUser created with unique IFI ID (IFI-XXXXXX)
    ↓
User profile complete
```

### 3. Login Flow

```
User enters credentials (app_login)
    ↓
Frappe LoginManager authenticates
    ↓
System generates/retrieves API Key & Secret
    ↓
Response includes:
  - API Key & Secret (token)
  - User details
  - Role information
  - Profile status
  - IFI ID (if approved)
    ↓
Mobile app stores token in local storage
    ↓
Mobile app registers FCM token
    ↓
All subsequent requests use:
  Authorization: token {api_key}:{api_secret}
```

### 4. Password Reset Flow

```
User requests reset (resend_mail)
    ↓
System generates 6-digit OTP
    ↓
Email sent with OTP
    ↓
User verifies OTP (verify_otp_code with purpose="password_reset")
    ↓
System generates single-use reset token (stored in cache, 10 min expiry)
    ↓
User submits new password with reset token (reset_password)
    ↓
System validates token from cache
    ↓
Password updated
    ↓
Token deleted from cache (single-use)
```

### 5. Token Management

- **API Key/Secret**: Generated on first login, stored in User doctype
- **FCM Token**: Registered after login, stored in custom field (if configured)
- **Reset Token**: Single-use, cache-based, 10-minute expiry
- **OTP**: 6-digit code, stored in `reset_password_key`, expiry from System Settings

## Custom Workflows

### UserSignups Approval Workflow

**States**:
1. **Draft**: Initial state after profile form submission
2. **Approval Pending**: Submitted for admin review
3. **Approved**: Admin approved (triggers AppUser creation)

**Transitions**:
- Draft → Approval Pending (User submits)
- Approval Pending → Approved (Admin approves)
- Approval Pending → Draft (Admin rejects)

**Hook**: `on_update` → `add_as_appuser` creates AppUser when state = Approved

### Attendance Auto-Calculation

**Hook**: `Attendance.on_update` → `change_total_attendance`

**Logic**:
1. Get all Attendance records for student
2. Count records where `is_present` = 'True'
3. Calculate percentage: (present / total) × 100
4. Update `Student.total_attendance` field

### Energy Points Integration

**Hook**: `Energy Point Log.after_insert` → `increase_points`

**Logic**:
1. Sum all Energy Point Logs for user (excluding Reviews)
2. Update `AppUser.points_gained` field

**Reward Workflow**:
1. Volunteer performs activity (e.g., completes session)
2. System creates Reward record
3. Energy Point Rule triggers Energy Point Log creation
4. Hook updates volunteer's total points

## Development

### Setting Up Development Environment

1. **Enable Developer Mode**
```bash
bench --site your-site.local set-config developer_mode 1
bench --site your-site.local clear-cache
```

2. **Watch for changes**
```bash
bench watch
```

3. **Create new DocType**
```bash
bench --site your-site.local console
# In console:
frappe.get_doc({
    "doctype": "DocType",
    "module": "IFIApp",
    "name": "YourDocType",
    ...
}).insert()
```

### Adding Custom API Methods

1. Create method in appropriate file (e.g., `ifiapi.py` or DocType `.py` file)
2. Add `@frappe.whitelist()` decorator
3. For guest access, use `@frappe.whitelist(allow_guest=True)`
4. Handle errors and set proper HTTP status codes:

```python
@frappe.whitelist()
def custom_method(**kwargs):
    try:
        # Your logic here
        frappe.response["http_status_code"] = 200
        frappe.response["status"] = "success"
        frappe.response["data"] = result
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Custom Method Error")
        frappe.response["http_status_code"] = 500
        frappe.response["status"] = "error"
        frappe.response["message_text"] = str(e)
```

### Adding Fixtures

1. Add data via Frappe UI
2. Export to fixtures in `hooks.py`:

```python
fixtures = [
    "YourDocType",
    {
        'dt': 'YourDocType',
        'filters': {'name': ('in', ('value1', 'value2'))}
    }
]
```

3. Export fixtures:
```bash
bench --site your-site.local export-fixtures
```

### Database Migrations

After modifying DocType structure:
```bash
bench --site your-site.local migrate
```

### Debugging

Enable detailed logging:
```python
frappe.log_error(frappe.get_traceback(), "Error Title")
```

View logs:
- **Error Log** doctype in Frappe
- Console: `bench --site your-site.local console` then `frappe.get_last_doc("Error Log")`

## Testing

### Manual Testing

1. Use Frappe REST API client or Postman
2. Base URL: `http://your-site.local:8000`
3. Authentication:
   - Header: `Authorization: token {api_key}:{api_secret}`
   - Get token from login response

### Example cURL Requests

**Login**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapi.app_login \
  -H "Content-Type: application/json" \
  -d '{"usr": "user@example.com", "pwd": "password"}'
```

**Get Students** (authenticated):
```bash
curl -X GET "http://your-site.local:8000/api/resource/Student?limit_page_length=10" \
  -H "Authorization: token {api_key}:{api_secret}"
```

**Bulk Attendance**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.attendance.attendance.submit_attendance \
  -H "Authorization: token {api_key}:{api_secret}" \
  -H "Content-Type: application/json" \
  -d '{
    "attendance_list": [
      {"student_id": "STUD-2024-00001", "is_present": "True"},
      {"student_id": "STUD-2024-00002", "is_present": "False"}
    ]
  }'
```

### Unit Tests

Create test files in doctype folders:
```python
# test_student.py
import frappe
import unittest

class TestStudent(unittest.TestCase):
    def test_student_creation(self):
        student = frappe.get_doc({
            "doctype": "Student",
            "full_name": "Test Student",
            ...
        })
        student.insert()
        self.assertTrue(frappe.db.exists("Student", student.name))
```

Run tests:
```bash
bench --site your-site.local run-tests --app ifiapp
```

## Deployment

### Production Setup

1. **Disable Developer Mode**
```bash
bench --site your-site.local set-config developer_mode 0
```

2. **Setup Production Config**
```bash
bench setup production your-user
```

3. **Setup SSL**
```bash
bench setup lets-encrypt your-site.com
```

4. **Enable Scheduler**
```bash
bench --site your-site.local enable-scheduler
```

5. **Setup Supervisor & Nginx**
```bash
sudo service supervisor restart
sudo service nginx reload
```

### Environment Variables

Configure in `site_config.json`:
```json
{
  "db_name": "your_db",
  "db_password": "your_password",
  "developer_mode": 0,
  "mail_server": "smtp.gmail.com",
  "mail_port": 587,
  "use_tls": 1,
  "mail_login": "your-email@domain.com",
  "mail_password": "your-password"
}
```

### Backup

**Manual Backup**:
```bash
bench --site your-site.local backup
```

**Automatic Backups**:
Configure in Site Config or use cron jobs:
```bash
bench --site your-site.local backup --with-files
```

**Restore**:
```bash
bench --site your-site.local restore /path/to/backup.sql.gz
```

## Contributing

### Guidelines

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Follow code standards**:
   - Use meaningful variable/function names
   - Add docstrings to functions
   - Handle exceptions gracefully
   - Log errors with `frappe.log_error()`
4. **Test your changes**
5. **Commit with clear messages**: `git commit -m "Add: Description of feature"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create Pull Request** on GitHub

### Code Style

- Follow PEP 8 for Python code
- Use tabs for indentation (Frappe convention)
- Maximum line length: 120 characters
- Use Frappe conventions for DocType methods

### Commit Message Format

```
Type: Short description

Detailed description (if needed)

Types: Add, Update, Fix, Remove, Refactor, Docs, Test
```

## Troubleshooting

### Common Issues

**Issue**: User can't login after signup
- **Solution**: Check if email is verified (`User.enabled = 1`) and role is assigned

**Issue**: Attendance not updating student percentage
- **Solution**: Check if `doc_events` hook is configured in `hooks.py`

**Issue**: API returns 403 Forbidden
- **Solution**: Check permissions in DocType and ensure user has correct role

**Issue**: Bulk operations failing
- **Solution**: Check request payload format and error logs in Error Log doctype

**Issue**: OTP not received
- **Solution**: Check Email Queue and SMTP configuration in Email Account

### Logs & Debugging

- **Error Logs**: Home → Error Log
- **Email Queue**: Home → Email Queue (check Failed status)
- **Scheduled Jobs**: Home → Scheduled Job Log
- **Background Jobs**: Check Redis queue with `bench doctor`

## License

MIT License

Copyright (c) 2024 JinsoRaj

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Quick Start

```bash
# Install the app
bench get-app https://github.com/JinsoRaj/IFIApp.git
bench --site your-site.local install-app ifiapp

# Run migrations and import fixtures
bench --site your-site.local migrate
bench --site your-site.local import-doc --path apps/ifiapp/ifiapp/fixtures

# Start development
bench start
```

## Support

For issues and feature requests, please visit:
- **GitHub**: https://github.com/JinsoRaj/IFIApp
- **Flutter App**: https://github.com/anthrapper/insight-app

## Acknowledgments

Built with [Frappe Framework](https://frappeframework.com/)

---

**Version**: 1.0.0
**Last Updated**: November 2024
**Maintainer**: JinsoRaj (jinsoraj2000@gmail.com)
