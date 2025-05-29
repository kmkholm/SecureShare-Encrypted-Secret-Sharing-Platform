# Simplified Share Secret Platform Plan

## Core Features
1. User Authentication
   - Login
   - Registration
   - Session management

2. Secret Creation
   - Text-only secrets
   - Password protection
   - Unique ID generation

3. QR Code Generation
   - Pure Python implementation (segno)
   - Basic QR code for sharing

4. Content Viewing
   - Password-protected access
   - Blurred content until password entered

## Technical Specifications
- Flask for web framework
- SQLite for database
- Pure Python dependencies only
- Minimal JavaScript for frontend
- No image processing libraries

## Project Structure
```
/share_secret_simple/
├── app.py                 # Main application file
├── requirements.txt       # Dependencies
├── schema.py              # Database models
├── static/                # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript
│   └── qrcodes/           # Generated QR codes
└── templates/             # HTML templates
    ├── index.html         # Landing page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── dashboard.html     # User dashboard
    ├── create.html        # Create secret page
    └── view.html          # View secret page
```

## Dependencies
- Flask
- Flask-SQLAlchemy
- Werkzeug
- segno (for QR codes)
- python-dotenv

## Implementation Plan
1. Set up basic project structure
2. Implement database models
3. Create authentication system
4. Implement secret creation
5. Add QR code generation
6. Create content viewing with password protection
7. Test locally
8. Deploy permanently
