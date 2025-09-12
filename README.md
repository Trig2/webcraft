# WebBuilder - Professional Website Development

WebBuilder is a Django-based web application for a website development company that specializes in creating websites for organizations such as schools, hospitals, e-commerce businesses, and marketing agencies.

## Features

- **Service Showcase**: Display various web development services offered
- **Portfolio Management**: Showcase completed projects
- **Service Packages**: Offer bundled services at discounted rates
- **Contact Form**: Allow potential clients to get in touch
- **Content Management**: Easily manage pages, team members, FAQs, and testimonials

## Technology Stack

- **Backend**: Django
- **Frontend**: Tailwind CSS
- **Database**: SQLite (default, can be configured for production)

## Project Structure

The project consists of the following Django apps:

- **core**: Contains base functionality, including home page, about page, contact form, and FAQs
- **services**: Manages services and service packages
- **projects**: Handles the portfolio of completed projects
- **theme**: Contains Tailwind CSS configuration

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js and npm (for Tailwind CSS)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd webbuilder
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install Tailwind CSS dependencies:
   ```
   python manage.py tailwind install
   ```

5. Apply database migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

8. In a separate terminal, start the Tailwind CSS watcher:
   ```
   python manage.py tailwind start
   ```

9. Access the site at http://127.0.0.1:8000/

## Usage

### Admin Interface

Access the admin interface at http://127.0.0.1:8000/admin/ to:

- Add/edit services and service packages
- Manage projects in your portfolio
- Update team member information
- Create and edit static pages
- Manage FAQs and testimonials
- View and respond to contact messages

### Content Management

1. **Services**: Add services with descriptions, pricing, and features
2. **Service Packages**: Create bundles of services at discounted rates
3. **Projects**: Showcase completed projects with details and images
4. **Team Members**: Add information about your team
5. **Testimonials**: Display client feedback
6. **FAQs**: Add frequently asked questions and answers
7. **Pages**: Create custom static pages

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving with a web server (Nginx, Apache)
4. Use a WSGI server like Gunicorn
5. Set up HTTPS with a valid SSL certificate

## License

This project is licensed under the MIT License - see the LICENSE file for details.# webcraft
