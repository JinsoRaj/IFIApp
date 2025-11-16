# IFI App API Documentation

Complete API reference for the IFI (Insight for Innovation) Backend Application.

## Table of Contents

1. [Introduction](#introduction)
2. [Base URLs & Environment](#base-urls--environment)
3. [Authentication](#authentication)
4. [Error Handling](#error-handling)
5. [Authentication APIs](#authentication-apis)
6. [Profile Setup APIs](#profile-setup-apis)
7. [Volunteer APIs](#volunteer-apis)
8. [QA APIs](#qa-apis)
9. [District Coordinator APIs](#district-coordinator-apis)
10. [Coordinator APIs](#coordinator-apis)
11. [Standard Frappe REST APIs](#standard-frappe-rest-apis)
12. [Bulk Operations](#bulk-operations)
13. [Advanced Querying](#advanced-querying)
14. [Appendix](#appendix)

---

## Introduction

The IFI App backend is built on the Frappe Framework and provides RESTful APIs for managing educational volunteers, students, assessments, and institutional data. The API supports role-based access control with four primary user roles: Volunteer, Quality Assurance (QA), Coordinator, and District Coordinator.

### Key Features
- Token-based authentication
- Role-based permissions
- Bulk operations support
- Real-time data synchronization
- File upload capabilities
- Advanced filtering and querying

---

## Base URLs & Environment

### Development
```
Base URL: http://your-site.local:8000
```

### Production
```
Base URL: https://your-domain.com
```

### API Paths
- **Custom Methods**: `/api/method/{module.path.method}`
- **Standard REST**: `/api/resource/{DocType}`
- **Authentication**: `/api/method/ifiapp.ifiapi.*`

---

## Authentication

All API requests (except registration and login) require authentication using API tokens.

### Authentication Header

```
Authorization: token {api_key}:{api_secret}
```

### Obtaining Tokens

Tokens are obtained through the login API (`app_login`). The response includes:
- `api_key`: Public key
- `api_secret`: Secret key

Store these securely in your application (e.g., Hive local storage in Flutter).

### Example Request with Authentication

```bash
curl -X GET "https://your-domain.com/api/resource/Student?limit_page_length=10" \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json"
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "http_status_code": 400,
  "status": "error",
  "message_text": "Email is required.",
  "exc_type": "ValidationError"
}
```

---

## Authentication APIs

### 1. Sign Up

Register a new user account.

**Endpoint**: `POST /api/method/ifiapp.ifiapi.sign_up`

**Authentication**: None (Guest access)

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address |
| password | string | Yes | Password (min 8 characters) |
| full_name | string | Yes | Full name of user |
| redirect_to | string | No | Redirect URL after signup |

**Request Example**:
```json
{
  "email": "volunteer@example.com",
  "password": "SecureP@ss123",
  "full_name": "John Doe",
  "redirect_to": ""
}
```

**Success Response** (200):
```json
{
  "status": 1,
  "message_text": "Created user"
}
```

**Error Response** (400):
```json
{
  "status": 0,
  "message_text": "Already Registered"
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapi.sign_up \
  -H "Content-Type: application/json" \
  -d '{
    "email": "volunteer@example.com",
    "password": "SecureP@ss123",
    "full_name": "John Doe"
  }'
```

**Notes**:
- User is created in disabled state
- 6-digit OTP sent via email
- OTP expires in 30 minutes (configurable)
- User must verify email before login

---

### 2. Verify Email

Verify email address using OTP.

**Endpoint**: `POST /api/method/ifiapp.ifiapi.verify_mail`

**Authentication**: None (Guest access)

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address |
| number_code | string | Yes | 6-digit OTP from email |

**Request Example**:
```json
{
  "email": "volunteer@example.com",
  "number_code": "123456"
}
```

**Success Response** (200):
```json
{
  "status": 1,
  "message_text": "Verified"
}
```

**Error Response** (400):
```json
{
  "status": 0,
  "message_text": "Mail is not verified"
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapi.verify_mail \
  -H "Content-Type: application/json" \
  -d '{
    "email": "volunteer@example.com",
    "number_code": "123456"
  }'
```

**Notes**:
- Enables user account
- Assigns 'ifiuser' role
- User can now login

---

### 3. Resend OTP

Resend verification OTP to email.

**Endpoint**: `POST /api/method/ifiapp.ifiapi.resend_mail`

**Authentication**: None (Guest access)

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address |

**Request Example**:
```json
{
  "email": "volunteer@example.com"
}
```

**Success Response** (200):
```json
{
  "status": 1,
  "message_text": "Generated a new code."
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapi.resend_mail \
  -H "Content-Type: application/json" \
  -d '{"email": "volunteer@example.com"}'
```

---

### 4. Login

Authenticate user and obtain API tokens.

**Endpoint**: `POST /api/method/ifiapp.ifiapi.app_login`

**Authentication**: None (Guest access)

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| usr | string | Yes | Email address |
| pwd | string | Yes | Password |

**Request Example**:
```json
{
  "usr": "volunteer@example.com",
  "pwd": "SecureP@ss123"
}
```

**Success Response** (200):
```json
{
  "message": "Logged In",
  "key_details": {
    "api_key": "abc123def456",
    "api_secret": "xyz789uvw012"
  },
  "user_details": [
    {
      "name": "volunteer@example.com",
      "first_name": "John",
      "last_name": null,
      "user_roles": ["ifiuser", "Volunteer"]
    }
  ],
  "profile_form": {
    "details": true,
    "approved": true,
    "ifi_id": "IFI-123456"
  }
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapi.app_login \
  -H "Content-Type: application/json" \
  -d '{
    "usr": "volunteer@example.com",
    "pwd": "SecureP@ss123"
  }'
```

**Notes**:
- Returns API key/secret for subsequent requests
- `profile_form` indicates profile setup and approval status
- Store tokens securely in app

---

### 5. Verify OTP for Password Reset

Verify OTP and get reset token.

**Endpoint**: `POST /api/method/ifiapp.ifiapi.verify_otp_code`

**Authentication**: None (Guest access)

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address |
| number_code | string | Yes | 6-digit OTP |
| purpose | string | Yes | "password_reset" |

**Request Example**:
```json
{
  "email": "volunteer@example.com",
  "number_code": "123456",
  "purpose": "password_reset"
}
```

**Success Response** (200):
```json
{
  "http_status_code": 200,
  "status": "success",
  "message_text": "OTP Verified",
  "reset_token": "abc123xyz789randomtoken"
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapi.verify_otp_code \
  -H "Content-Type: application/json" \
  -d '{
    "email": "volunteer@example.com",
    "number_code": "123456",
    "purpose": "password_reset"
  }'
```

**Notes**:
- Reset token valid for 10 minutes
- Token is single-use only
- Stored in cache, deleted after use

---

### 6. Reset Password

Reset password using verification token.

**Endpoint**: `POST /api/method/ifiapp.ifiapi.reset_password`

**Authentication**: None (Guest access)

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address |
| new_password | string | Yes | New password |
| reset_token | string | Yes | Token from verify_otp_code |

**Request Example**:
```json
{
  "email": "volunteer@example.com",
  "new_password": "NewP@ssword123",
  "reset_token": "abc123xyz789randomtoken"
}
```

**Success Response** (200):
```json
{
  "http_status_code": 200,
  "status": "success",
  "message_text": "Password reset successful."
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapi.reset_password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "volunteer@example.com",
    "new_password": "NewP@ssword123",
    "reset_token": "abc123xyz789randomtoken"
  }'
```

---

### 7. Change Password

Change password for authenticated user.

**Endpoint**: `POST /api/method/frappe.client.change_password`

**Authentication**: Required

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| old_password | string | Yes | Current password |
| new_password | string | Yes | New password |

**Request Example**:
```json
{
  "old_password": "OldP@ssword123",
  "new_password": "NewP@ssword456"
}
```

**Success Response** (200):
```json
{
  "message": "Password changed successfully"
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/frappe.client.change_password \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "OldP@ssword123",
    "new_password": "NewP@ssword456"
  }'
```

---

## Profile Setup APIs

### 1. Get States

Retrieve list of states.

**Endpoint**: `GET /api/resource/States`

**Authentication**: Required

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| fields | array | Fields to return (JSON array) |
| limit_page_length | int | Number of records (default: 20) |

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/resource/States?fields=[\"name\",\"state_name\"]&limit_page_length=50" \
  -H "Authorization: token abc123:xyz789"
```

**Success Response** (200):
```json
{
  "data": [
    {
      "name": "Kerala",
      "state_name": "Kerala"
    },
    {
      "name": "Tamil Nadu",
      "state_name": "Tamil Nadu"
    }
  ]
}
```

---

### 2. Get Districts by State

Retrieve districts filtered by state.

**Endpoint**: `GET /api/resource/Districts`

**Authentication**: Required

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| filters | array | Filter conditions (JSON) |
| fields | array | Fields to return |

**Filter Example**:
```json
[["state","=","Kerala"]]
```

**cURL Example**:
```bash
curl -X GET 'http://your-site.local:8000/api/resource/Districts?filters=[["state","=","Kerala"]]&fields=["name","district_name"]' \
  -H "Authorization: token abc123:xyz789"
```

**Success Response** (200):
```json
{
  "data": [
    {
      "name": "Ernakulam",
      "district_name": "Ernakulam"
    },
    {
      "name": "Thiruvananthapuram",
      "district_name": "Thiruvananthapuram"
    }
  ]
}
```

---

### 3. Get Colleges by District

Retrieve colleges filtered by district.

**Endpoint**: `GET /api/resource/College`

**Authentication**: Required

**Filter Example**:
```json
[["district","=","Ernakulam"]]
```

**cURL Example**:
```bash
curl -X GET 'http://your-site.local:8000/api/resource/College?filters=[["district","=","Ernakulam"]]&fields=["name","institution_name"]' \
  -H "Authorization: token abc123:xyz789"
```

---

### 4. Get Corporates

Retrieve list of corporates.

**Endpoint**: `GET /api/resource/Corporate`

**Authentication**: Required

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/resource/Corporate?fields=[\"name\",\"institution_name\"]&limit_page_length=100" \
  -H "Authorization: token abc123:xyz789"
```

---

### 5. Get Profile Images

Retrieve available avatar images.

**Endpoint**: `GET /api/resource/ProfileImages`

**Authentication**: Required

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/resource/ProfileImages?fields=[\"name\",\"profile_image\"]" \
  -H "Authorization: token abc123:xyz789"
```

**Response Example**:
```json
{
  "data": [
    {
      "name": "Avatar 1",
      "profile_image": "/files/avatar1.png"
    }
  ]
}
```

---

### 6. Create User Profile

Submit user profile for approval.

**Endpoint**: `POST /api/resource/UserSignups`

**Authentication**: Required

**Request Body**:
```json
{
  "email_id": "volunteer@example.com",
  "full_name": "John Doe",
  "ph_number": "1234567890",
  "gender": "Male",
  "state": "Kerala",
  "district": "Ernakulam",
  "college_name": "Example College",
  "emp_status": "Student",
  "res_address": "123 Main St, City",
  "profile_pic": "/files/avatar1.png"
}
```

**Success Response** (200):
```json
{
  "data": {
    "name": "volunteer@example.com",
    "workflow_state": "Draft"
  }
}
```

---

### 7. Upload File

Upload profile picture or document.

**Endpoint**: `POST /api/method/upload_file`

**Authentication**: Required

**Form Data**:
| Field | Type | Description |
|-------|------|-------------|
| file | file | File to upload |
| is_private | int | 0 for public, 1 for private |

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/upload_file \
  -H "Authorization: token abc123:xyz789" \
  -F "file=@/path/to/image.jpg" \
  -F "is_private=0"
```

**Success Response** (200):
```json
{
  "message": {
    "file_url": "/files/image.jpg",
    "file_name": "image.jpg"
  }
}
```

---

## Volunteer APIs

### 1. Get Dashboard Data

Retrieve volunteer profile and assigned students.

**Endpoint**: `GET /api/method/ifiapp.ifiapp.doctype.appuser.appuser.get_appuser_and_students`

**Authentication**: Required

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ifi_id | string | Yes | Volunteer's IFI ID |

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.appuser.appuser.get_appuser_and_students?ifi_id=IFI-123456" \
  -H "Authorization: token abc123:xyz789"
```

**Success Response** (200):
```json
{
  "data": {
    "ifi_user_details": {
      "name": "volunteer@example.com",
      "profile_pic": "/files/avatar1.png",
      "ifi_id": "IFI-123456",
      "full_name": "John Doe",
      "gender": "Male",
      "points_gained": 150,
      "is_volunteer": 1,
      "is_coordinator": 0,
      "is_qa": 0,
      "state": "Kerala",
      "district": "Ernakulam"
    },
    "student_details": [
      {
        "student_id": "STUD-2024-00001",
        "full_name": "Alice Smith",
        "school_name": "Example School",
        "class_name": "5",
        "school_district": "Ernakulam",
        "grade": "A"
      }
    ]
  }
}
```

---

### 2. Search Students

Search for students by name or ID.

**Endpoint**: `GET /api/resource/Student`

**Authentication**: Required

**Filter for Search**:
```json
[["full_name","like","%search_term%"]]
```

**cURL Example**:
```bash
curl -X GET 'http://your-site.local:8000/api/resource/Student?filters=[["full_name","like","%Alice%"]]&fields=["name","full_name","school_name","class_name"]' \
  -H "Authorization: token abc123:xyz789"
```

---

### 3. Get Student Details

Get detailed information about a student.

**Endpoint**: `GET /api/method/ifiapp.ifiapp.doctype.student.student.get_student_details`

**Authentication**: Required

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| student_id | string | Yes | Student ID (e.g., STUD-2024-00001) |

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.student.student.get_student_details?student_id=STUD-2024-00001" \
  -H "Authorization: token abc123:xyz789"
```

**Success Response** (200):
```json
{
  "http_status_code": 200,
  "data": {
    "name": "STUD-2024-00001",
    "full_name": "Alice Smith",
    "school_name": "Example School",
    "school_district": "Ernakulam",
    "class_name": "5",
    "grade": "A",
    "gender": "Female",
    "contact_number": "9876543210",
    "english_level": "Intermediate",
    "maths_level": "Advanced",
    "total_attendance": 85,
    "skills": [
      "linguistic_verbal",
      "logical_mathematical",
      "interpersonal"
    ],
    "maths_marks": [],
    "english_marks": []
  }
}
```

**Notes**:
- Skills are returned as array of skill names
- Individual skill fields (visual_spatial, etc.) are removed from response
- Maths and English marks are child tables

---

### 4. Create Student

Add a new student to the system.

**Endpoint**: `POST /api/method/ifiapp.ifiapp.doctype.student.student.manage_student`

**Authentication**: Required

**Request Body**:
```json
{
  "full_name": "Bob Johnson",
  "school_name": "Example School",
  "school_district": "Ernakulam",
  "class_name": "6",
  "grade": "B",
  "gender": "Male",
  "contact_number": "9123456780",
  "english_level": "Beginner",
  "maths_level": "Intermediate",
  "skills": [
    "bodily_kinesthetic",
    "musical",
    "naturalistic"
  ]
}
```

**Success Response** (200):
```json
{
  "http_status_code": 200,
  "status": "success",
  "message_text": "Student added successfully."
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.student.student.manage_student \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Bob Johnson",
    "school_name": "Example School",
    "school_district": "Ernakulam",
    "class_name": "6",
    "grade": "B",
    "gender": "Male",
    "contact_number": "9123456780",
    "english_level": "Beginner",
    "maths_level": "Intermediate",
    "skills": ["bodily_kinesthetic","musical","naturalistic"]
  }'
```

**Notes**:
- Skills are provided as array of skill names
- Backend converts to individual check fields
- All other skill fields set to 0

---

### 5. Update Student

Update existing student information.

**Endpoint**: `PUT /api/method/ifiapp.ifiapp.doctype.student.student.manage_student`

**Authentication**: Required

**Request Body**:
```json
{
  "name": "STUD-2024-00001",
  "full_name": "Alice Smith Updated",
  "english_level": "Advanced",
  "skills": [
    "linguistic_verbal",
    "logical_mathematical"
  ]
}
```

**Success Response** (200):
```json
{
  "http_status_code": 200,
  "status": "success",
  "message_text": "Student updated successfully."
}
```

**cURL Example**:
```bash
curl -X PUT http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.student.student.manage_student \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "STUD-2024-00001",
    "full_name": "Alice Smith Updated",
    "skills": ["linguistic_verbal","logical_mathematical"]
  }'
```

---

### 6. Submit Class Session

Record a teaching session.

**Endpoint**: `POST /api/resource/ClassSession`

**Authentication**: Required

**Request Body**:
```json
{
  "ifi_id": "IFI-123456",
  "school_name": "Example School",
  "session_date": "2024-11-15",
  "session_start_time": "2024-11-15 10:00:00",
  "session_end_time": "2024-11-15 11:00:00",
  "session_total_time": 1,
  "class_name": "5",
  "topic": "Addition",
  "module": "Basic Arithmetic",
  "session_strength": 25
}
```

**Success Response** (200):
```json
{
  "data": {
    "name": "SESS-2024-00001",
    "ifi_id": "IFI-123456",
    "session_date": "2024-11-15"
  }
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/resource/ClassSession \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "ifi_id": "IFI-123456",
    "school_name": "Example School",
    "session_date": "2024-11-15",
    "session_start_time": "2024-11-15 10:00:00",
    "session_end_time": "2024-11-15 11:00:00",
    "session_total_time": 1,
    "class_name": "5",
    "topic": "Addition",
    "module": "Basic Arithmetic",
    "session_strength": 25
  }'
```

**Notes**:
- `session_total_time` is manually entered (hours)
- Auto-calculation disabled per requirements
- Links to Topic and IFIModule masters

---

### 7. Submit Bulk Attendance

Mark attendance for multiple students at once.

**Endpoint**: `POST /api/method/ifiapp.ifiapp.doctype.attendance.attendance.submit_attendance`

**Authentication**: Required

**Request Body**:
```json
{
  "attendance_list": [
    {
      "student_id": "STUD-2024-00001",
      "is_present": "True"
    },
    {
      "student_id": "STUD-2024-00002",
      "is_present": "False"
    },
    {
      "student_id": "STUD-2024-00003",
      "is_present": "True"
    }
  ]
}
```

**Success Response** (200):
```json
{
  "status": true,
  "info": "Bulk Attendance marked"
}
```

**Error Response** (500):
```json
{
  "status": false,
  "info": "Bulk Attendance failed"
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.attendance.attendance.submit_attendance \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "attendance_list": [
      {"student_id": "STUD-2024-00001", "is_present": "True"},
      {"student_id": "STUD-2024-00002", "is_present": "False"}
    ]
  }'
```

**Notes**:
- Creates new attendance records
- Does NOT update existing records
- Duplicate entries will cause error
- Automatically updates student's total_attendance percentage

---

### 8. Submit Bulk Maths Marks

Submit or update maths test marks for multiple students.

**Endpoint**: `POST /api/method/ifiapp.ifiapp.doctype.mathsmark.mathsmark.bulk_create_or_update_maths_mark_entries`

**Authentication**: Required

**Request Body**:
```json
{
  "topic": "Addition",
  "initial_total_mark": 10,
  "final_total_mark": -1,
  "marks_list": [
    {
      "student_id": "STUD-2024-00001",
      "initial_test_mark": 8
    },
    {
      "student_id": "STUD-2024-00002",
      "initial_test_mark": 7
    }
  ]
}
```

**Success Response** (200):
```json
{
  "status": "success",
  "message_text": "Bulk MathsMark entries processed successfully"
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.mathsmark.mathsmark.bulk_create_or_update_maths_mark_entries \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Addition",
    "initial_total_mark": 10,
    "final_total_mark": -1,
    "marks_list": [
      {"student_id": "STUD-2024-00001", "initial_test_mark": 8},
      {"student_id": "STUD-2024-00002", "initial_test_mark": 7}
    ]
  }'
```

**Notes**:
- Creates new entry if not exists, updates if exists
- Use -1 for marks not being submitted
- Stored as child table in Student
- Supports initial and final tests

---

### 9. Submit Bulk English Marks

Submit or update English test marks for multiple students.

**Endpoint**: `POST /api/method/ifiapp.ifiapp.doctype.englishmark.englishmark.bulk_add_or_update_english_marks`

**Authentication**: Required

**Request Body**:
```json
{
  "topic": "Reading Comprehension",
  "initial_total_mark": 20,
  "intermediate_total_mark": -1,
  "final_total_mark": -1,
  "marks_list": [
    {
      "student_id": "STUD-2024-00001",
      "initial_test_mark": 15,
      "initial_grade_level": "Level 3"
    },
    {
      "student_id": "STUD-2024-00002",
      "initial_test_mark": 12,
      "initial_grade_level": "Level 2"
    }
  ]
}
```

**Success Response** (200):
```json
{
  "status": "success",
  "message_text": "Bulk English marks and grades processed successfully."
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.englishmark.englishmark.bulk_add_or_update_english_marks \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Reading Comprehension",
    "initial_total_mark": 20,
    "marks_list": [
      {"student_id": "STUD-2024-00001", "initial_test_mark": 15, "initial_grade_level": "Level 3"}
    ]
  }'
```

**Notes**:
- Supports initial, intermediate, and final tests
- Each test level has marks + grade level
- Creates or updates existing records
- Stored as child table in Student

---

### 10. Get Recent Rewards

Retrieve recent reward points for volunteer.

**Endpoint**: `GET /api/method/ifiapp.ifiapp.doctype.reward.reward.get_recent_rewards`

**Authentication**: Required

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ifi_id | string | Yes | Volunteer's IFI ID |

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.reward.reward.get_recent_rewards?ifi_id=IFI-123456" \
  -H "Authorization: token abc123:xyz789"
```

**Success Response** (200):
```json
{
  "status": "success",
  "info": "Recent Rewards",
  "recent_points": [
    {
      "rule": "Completed Session",
      "points": 10
    },
    {
      "rule": "Student Assessment",
      "points": 5
    }
  ]
}
```

---

## QA APIs

### 1. Search Volunteers

Search and filter volunteers for evaluation.

**Endpoint**: `GET /api/resource/AppUser`

**Authentication**: Required

**Filters**:
```json
[["is_volunteer","=",1],["district","=","Ernakulam"]]
```

**cURL Example**:
```bash
curl -X GET 'http://your-site.local:8000/api/resource/AppUser?filters=[["is_volunteer","=",1]]&fields=["name","ifi_id","full_name","district","profile_pic"]&limit_page_length=20' \
  -H "Authorization: token abc123:xyz789"
```

**Response Example**:
```json
{
  "data": [
    {
      "name": "volunteer@example.com",
      "ifi_id": "IFI-123456",
      "full_name": "John Doe",
      "district": "Ernakulam",
      "profile_pic": "/files/avatar1.png"
    }
  ]
}
```

---

### 2. Get Evaluation Questions

Retrieve assessment questions.

**Endpoint**: `GET /api/resource/Question`

**Authentication**: Required

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/resource/Question?fields=[\"name\",\"question_text\",\"max_mark\"]&limit_page_length=50" \
  -H "Authorization: token abc123:xyz789"
```

**Response Example**:
```json
{
  "data": [
    {
      "name": "Q001",
      "question_text": "Explain the teaching methodology used",
      "max_mark": 10
    }
  ]
}
```

---

### 3. Submit Evaluation

Submit QA evaluation for a volunteer.

**Endpoint**: `POST /api/method/ifiapp.ifiapp.doctype.evaluation.evaluation.send_evaluation`

**Authentication**: Required

**Request Body**:
```json
{
  "ifi_id": "IFI-123456",
  "evaluator_id": "IFI-789012",
  "evaluation_date": "2024-11-15",
  "evaluation_time": "14:00:00",
  "evaluation_mode": "Online",
  "table_questions": [
    {
      "question": "Q001",
      "mark": 8
    },
    {
      "question": "Q002",
      "mark": 7
    }
  ]
}
```

**Success Response** (200):
```json
{
  "http_status_code": 200,
  "status": "success",
  "message_text": "Evaluation added successfully.",
  "evaluation_id": "EVAL-2024-00001"
}
```

**cURL Example**:
```bash
curl -X POST http://your-site.local:8000/api/method/ifiapp.ifiapp.doctype.evaluation.evaluation.send_evaluation \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "ifi_id": "IFI-123456",
    "evaluator_id": "IFI-789012",
    "evaluation_date": "2024-11-15",
    "evaluation_time": "14:00:00",
    "evaluation_mode": "Online",
    "table_questions": [
      {"question": "Q001", "mark": 8},
      {"question": "Q002", "mark": 7}
    ]
  }'
```

**Notes**:
- Auto-fills volunteer and evaluator details from IFI IDs
- Auto-calculates final_score from question marks
- Creates QuestionTable child records

---

### 4. Get Evaluation History

Retrieve past evaluations.

**Endpoint**: `GET /api/resource/Evaluation`

**Authentication**: Required

**Filters**:
```json
[["evaluator_id","=","IFI-789012"]]
```

**cURL Example**:
```bash
curl -X GET 'http://your-site.local:8000/api/resource/Evaluation?filters=[["evaluator_id","=","IFI-789012"]]&fields=["name","ifi_id","full_name","evaluation_date","final_score"]&order_by=creation desc' \
  -H "Authorization: token abc123:xyz789"
```

---

## District Coordinator APIs

### 1. Add School

Create a new school.

**Endpoint**: `POST /api/resource/School`

**Authentication**: Required

**Request Body**:
```json
{
  "institution_name": "New School",
  "district": "Ernakulam",
  "address": "123 School St",
  "landmark": "Near Temple",
  "contact_number": "9876543210",
  "email": "school@example.com"
}
```

**Success Response** (200):
```json
{
  "data": {
    "name": "New School",
    "institution_name": "New School"
  }
}
```

---

### 2. Add College

Create a new college.

**Endpoint**: `POST /api/resource/College`

**Authentication**: Required

**Request Body**:
```json
{
  "institution_name": "New College",
  "district": "Ernakulam",
  "address": "456 College Rd",
  "landmark": "Near Station",
  "contact_number": "9123456789",
  "email": "college@example.com"
}
```

---

### 3. Map Schools to Volunteers

Assign schools to a volunteer (AppUser).

**Endpoint**: `PUT /api/resource/AppUser/{email}`

**Authentication**: Required

**Request Body**:
```json
{
  "schools": [
    {
      "schools": "School Name 1"
    },
    {
      "schools": "School Name 2"
    }
  ]
}
```

**cURL Example**:
```bash
curl -X PUT http://your-site.local:8000/api/resource/AppUser/volunteer@example.com \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "schools": [
      {"schools": "School Name 1"},
      {"schools": "School Name 2"}
    ]
  }'
```

**Notes**:
- Validates for duplicate school entries
- Schools stored in MappedSchools child table
- Throws error if duplicate found

---

### 4. Get Mapped Schools

View schools assigned to a volunteer.

**Endpoint**: `GET /api/resource/AppUser/{email}`

**Authentication**: Required

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/resource/AppUser/volunteer@example.com?fields=[\"name\",\"full_name\",\"schools\"]" \
  -H "Authorization: token abc123:xyz789"
```

**Response Example**:
```json
{
  "data": {
    "name": "volunteer@example.com",
    "full_name": "John Doe",
    "schools": [
      {
        "schools": "School Name 1"
      }
    ]
  }
}
```

---

## Coordinator APIs

### 1. Get School Details

Retrieve school information with statistics.

**Endpoint**: `GET /api/resource/School/{school_name}`

**Authentication**: Required

**cURL Example**:
```bash
curl -X GET "http://your-site.local:8000/api/resource/School/Example%20School" \
  -H "Authorization: token abc123:xyz789"
```

---

### 2. Get Students by School

Retrieve all students from a specific school.

**Endpoint**: `GET /api/resource/Student`

**Authentication**: Required

**Filters**:
```json
[["school_name","=","Example School"]]
```

**cURL Example**:
```bash
curl -X GET 'http://your-site.local:8000/api/resource/Student?filters=[["school_name","=","Example School"]]&fields=["name","full_name","class_name","grade"]' \
  -H "Authorization: token abc123:xyz789"
```

---

### 3. Get Volunteers by School

Find volunteers assigned to a school.

**Endpoint**: `GET /api/resource/AppUser`

**Authentication**: Required

**Filters with Child Table**:
```json
[["MappedSchools","schools","=","Example School",false]]
```

**cURL Example**:
```bash
curl -X GET 'http://your-site.local:8000/api/resource/AppUser?filters=[["MappedSchools","schools","=","Example School",false]]&fields=["name","full_name","ifi_id"]' \
  -H "Authorization: token abc123:xyz789"
```

**Notes**:
- Uses child table filtering
- Fourth parameter (false) required for child table filters

---

## Standard Frappe REST APIs

### Overview

All DocTypes in IFI App support standard Frappe REST operations:

| Operation | Method | Endpoint | Description |
|-----------|--------|----------|-------------|
| List | GET | `/api/resource/{DocType}` | Get list of documents |
| Get | GET | `/api/resource/{DocType}/{name}` | Get single document |
| Create | POST | `/api/resource/{DocType}` | Create new document |
| Update | PUT | `/api/resource/{DocType}/{name}` | Update document |
| Delete | DELETE | `/api/resource/{DocType}/{name}` | Delete document |

### Available DocTypes

- AppUser
- Student
- Attendance
- ClassSession
- Evaluation
- Reward
- School, College, Corporate
- States, Districts, Class
- IFIModule, Topic, Question
- UserSignups
- ProfileImages

---

### List Documents

**Endpoint**: `GET /api/resource/{DocType}`

**Query Parameters**:
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| fields | JSON | Fields to return | `["name","full_name"]` |
| filters | JSON | Filter conditions | `[["class_name","=","5"]]` |
| limit_page_length | int | Records per page | `20` |
| limit_start | int | Offset for pagination | `0` |
| order_by | string | Sort field and direction | `creation desc` |

**Example**:
```bash
curl -X GET 'http://your-site.local:8000/api/resource/Student?fields=["name","full_name"]&filters=[["class_name","=","5"]]&limit_page_length=10&order_by=creation desc' \
  -H "Authorization: token abc123:xyz789"
```

---

### Get Single Document

**Endpoint**: `GET /api/resource/{DocType}/{name}`

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| fields | JSON | Fields to return (optional) |

**Example**:
```bash
curl -X GET "http://your-site.local:8000/api/resource/Student/STUD-2024-00001" \
  -H "Authorization: token abc123:xyz789"
```

**Response**:
```json
{
  "data": {
    "name": "STUD-2024-00001",
    "full_name": "Alice Smith",
    "school_name": "Example School",
    ...
  }
}
```

---

### Create Document

**Endpoint**: `POST /api/resource/{DocType}`

**Request Body**: JSON object with field values

**Example**:
```bash
curl -X POST http://your-site.local:8000/api/resource/Reward \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "ifi_id": "IFI-123456",
    "reward_type": "Session Completion",
    "points": 10
  }'
```

---

### Update Document

**Endpoint**: `PUT /api/resource/{DocType}/{name}`

**Request Body**: JSON object with fields to update

**Example**:
```bash
curl -X PUT http://your-site.local:8000/api/resource/Student/STUD-2024-00001 \
  -H "Authorization: token abc123:xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "grade": "A+",
    "english_level": "Advanced"
  }'
```

---

### Delete Document

**Endpoint**: `DELETE /api/resource/{DocType}/{name}`

**Example**:
```bash
curl -X DELETE http://your-site.local:8000/api/resource/Attendance/ATT-2024-00001 \
  -H "Authorization: token abc123:xyz789"
```

**Response**:
```json
{
  "message": "ok"
}
```

---

## Bulk Operations

### Comparison of Bulk APIs

| Operation | Endpoint | Create | Update | Notes |
|-----------|----------|--------|--------|-------|
| Attendance | `submit_attendance` | ✓ | ✗ | Errors on duplicates |
| Maths Marks | `bulk_create_or_update_maths_mark_entries` | ✓ | ✓ | Upsert logic |
| English Marks | `bulk_add_or_update_english_marks` | ✓ | ✓ | Upsert logic |

### Best Practices

1. **Attendance**:
   - Submit once per day per student
   - Check for existing records before submission
   - Handle errors gracefully

2. **Marks**:
   - Use -1 for marks not being submitted
   - Submit one test level at a time (initial/intermediate/final)
   - Include total marks in request

3. **Transaction Handling**:
   - All bulk operations use database transactions
   - Failures rollback entire operation
   - Check error logs for details

---

## Advanced Querying

### Filter Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `[["class_name","=","5"]]` |
| `!=` | Not equals | `[["gender","!=","Male"]]` |
| `>` | Greater than | `[["grade",">","B"]]` |
| `<` | Less than | `[["total_attendance","<",50]]` |
| `>=` | Greater than or equal | `[["points_gained",">=",100]]` |
| `<=` | Less than or equal | `[["creation","<=","2024-01-01"]]` |
| `like` | Pattern match | `[["full_name","like","%John%"]]` |
| `in` | In list | `[["class_name","in",["5","6","7"]]]` |
| `not in` | Not in list | `[["district","not in",["District1"]]]` |
| `is` | Is null/empty | `[["email","is","not set"]]` |

### Multiple Filters

Combine filters with AND logic:
```json
[
  ["class_name","=","5"],
  ["school_district","=","Ernakulam"],
  ["total_attendance",">",75]
]
```

### Child Table Filters

Filter by child table fields:
```json
[["ChildTableName","field","=","value",false]]
```

Example - Students with specific skills:
```json
[["Student","visual_spatial","=",1,false]]
```

Example - Volunteers assigned to specific school:
```json
[["MappedSchools","schools","=","School Name",false]]
```

**Note**: The fourth parameter (false) is required for child table filters.

### Field Selection

Return only specific fields:
```json
["name","full_name","email_id","district"]
```

### Pagination

```
limit_page_length=20&limit_start=0
```

- Page 1: `limit_start=0`
- Page 2: `limit_start=20`
- Page 3: `limit_start=40`

### Sorting

```
order_by=creation desc
order_by=full_name asc
order_by=modified desc
```

### Complete Example

```bash
curl -X GET 'http://your-site.local:8000/api/resource/Student?fields=["name","full_name","class_name","total_attendance"]&filters=[["class_name","=","5"],["total_attendance",">",80]]&limit_page_length=10&limit_start=0&order_by=total_attendance desc' \
  -H "Authorization: token abc123:xyz789"
```

---

## Appendix

### A. Skill Fields Reference

Student skills (8 categories):
1. `visual_spatial` - Drawing, Painting, Visual Arts
2. `linguistic_verbal` - Reading, Writing, Debate, Speech
3. `interpersonal` - Communication, Leadership
4. `intrapersonal` - Self Awareness
5. `logical_mathematical` - Problem solving, Analytical thinking
6. `musical` - Singing, Musical instruments
7. `bodily_kinesthetic` - Dance, Sports, Physical coordination
8. `naturalistic` - Nature, Biology interest

### B. DocType Field References

**Student Auto-naming**: `STUD-.YYYY.-` (e.g., STUD-2024-00001)
**AppUser Auto-naming**: By field `user_details` (email)
**IFI ID Format**: `IFI-XXXXXX` (6 random digits)

### C. Workflow States

**UserSignups**:
- Draft
- Approval Pending
- Approved

### D. Date/Time Formats

- **Date**: `YYYY-MM-DD` (e.g., 2024-11-15)
- **DateTime**: `YYYY-MM-DD HH:MM:SS` (e.g., 2024-11-15 14:30:00)
- **Time**: `HH:MM:SS` (e.g., 14:30:00)

### E. Common HTTP Headers

```
Authorization: token {api_key}:{api_secret}
Content-Type: application/json
Accept: application/json
```

### F. Rate Limiting

- No explicit rate limits documented
- Follow reasonable usage patterns
- Implement exponential backoff for retries

### G. Support & Resources

- **Backend Repo**: https://github.com/JinsoRaj/IFIApp
- **Frontend Repo**: https://github.com/anthrapper/insight-app
- **Frappe Docs**: https://frappeframework.com/docs
- **Issue Tracker**: https://github.com/JinsoRaj/IFIApp/issues

---

**Document Version**: 1.0.0  
**Last Updated**: November 2024  
**Maintainer**: JinsoRaj (jinsoraj2000@gmail.com)
