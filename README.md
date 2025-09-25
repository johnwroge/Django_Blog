# Django Blog Project

[![Django CI](https://github.com/johnwroge/Django_Blog/actions/workflows/django.yml/badge.svg)](https://github.com/johnwroge/Django_Blog/actions/workflows/django.yml)

A personal blog built with Django featuring user authentication, post management, and commenting system.

## Features

- **User Roles**:
  - Superuser: Full CRUD access, Django admin access
  - Blog Authors: Can create, edit, and delete their own posts
  - Visitors: Can view posts and leave comments

- **Blog Management**:
  - Create, edit, and delete blog posts
  - Rich text content with line break formatting
  - Published/draft status for posts
  - Pagination for post listings

- **User Authentication**:
  - User registration and login
  - Group-based permissions
  - Session management

- **Commenting System**:
  - Authenticated users can comment on posts
  - Comments display with timestamps and author info

## Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone and setup**:
   ```bash
   git clone https://github.com/johnwroge/Django_Blog.git
   cd Django_Blog
   python -m venv blog_env
   source blog_env/bin/activate  # On Windows: blog_env\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install django python-dotenv django-widget-tweaks
   ```

3. **Environment setup**:
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY='your-secret-key-here'
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

4. **Database setup**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to view the blog.

## Creating Blog Posts

### As a Superuser
1. Login at `/accounts/login/`
2. Click "New Post" in the navigation
3. Fill out the title, content, and set published status
4. Save to create the post

### Setting Up Blog Authors
1. Access Django admin at `/admin/`
2. Create a group called "Blog Authors"
3. Create new users and add them to this group
4. Blog authors can then create their own posts

## User Management

### Create Blog Authors via Admin
1. Go to `/admin/`
2. Click "Groups" → "Add Group"
3. Name: "Blog Authors"
4. Save the group
5. Create users and assign them to this group

### User Registration
- Visitors can register at `/register/`
- New users can comment but cannot create posts
- Manually add them to "Blog Authors" group via admin if needed

## Key URLs

- `/` - Home page (blog post list)
- `/post/<id>/` - Individual blog post
- `/post/new/` - Create new post (authors/superusers only)
- `/post/<id>/edit/` - Edit post (authors/superusers only)
- `/accounts/login/` - Login page
- `/register/` - User registration
- `/admin/` - Django admin (superusers only)

## File Structure

```
blog_project/
├── blog/                  # Main blog app
│   ├── models.py         # BlogPost and Comment models
│   ├── views.py          # Blog views and logic
│   ├── forms.py          # Blog and comment forms
│   ├── urls.py           # App URL patterns
│   └── admin.py          # Admin configuration
├── blog_project/         # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── templates/            # HTML templates
│   ├── blog/            # Blog-specific templates
│   └── registration/    # Auth templates
├── static/              # Static files (CSS, JS, images)
├── manage.py           # Django management script
└── .env               # Environment variables (not in git)
```

## Environment Variables

Store sensitive data in `.env` file:

```env
SECRET_KEY='your-django-secret-key'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Never commit the `.env` file to version control.

## Security Notes

- Secret key is stored in environment variables
- User authentication required for posting/commenting
- CSRF protection enabled
- Group-based permission system

## Development

### Running Tests Locally
```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run security checks
python manage.py check --deploy
```

### Continuous Integration
This project uses GitHub Actions for automated testing. Every push to `main` or `develop` branches will:
- Run the full test suite on Python 3.11
- Perform Django system checks
- Run database migrations
- Execute security checks

Tests must pass before merging pull requests.

### Adding New Features
1. Create new models in `blog/models.py`
2. Run `python manage.py makemigrations blog`
3. Run `python manage.py migrate`
4. Update views, forms, and templates as needed
5. Write tests for new functionality
6. Ensure all tests pass locally before pushing

### Testing User Roles
1. Create superuser account
2. Create regular user accounts
3. Test different permission levels
4. Verify group-based access control

## Deployment

For production deployment:
1. Set `DEBUG=False` in environment
2. Configure proper `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up static file serving
5. Use a proper WSGI server (Gunicorn, uWSGI)

## Troubleshooting

**Login not working**: Check credentials and ensure user exists
**New posts not appearing**: Verify user is in "Blog Authors" group
**Template errors**: Ensure all templates are in correct directories
**Static files not loading**: Check `STATICFILES_DIRS` setting