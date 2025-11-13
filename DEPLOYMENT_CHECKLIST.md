# 📋 Pre-Deployment Checklist

## ✅ Security Checklist

- [ ] Change all default passwords
- [ ] Generate new SECRET_KEY for production
- [ ] Set strong database password
- [ ] Enable HTTPS/SSL certificates
- [ ] Review and restrict CORS origins
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Review .gitignore (no sensitive files)
- [ ] Set environment variables securely
- [ ] Enable database backups

## ✅ Code Quality

- [ ] All tests passing
- [ ] No console.log in production code
- [ ] No TODO comments unresolved
- [ ] Code reviewed and approved
- [ ] Documentation up to date
- [ ] Error handling implemented
- [ ] Logging configured properly

## ✅ Performance

- [ ] Frontend optimized (build size)
- [ ] Database indexes created
- [ ] API response times acceptable
- [ ] Images optimized
- [ ] Caching configured
- [ ] CDN setup (if needed)

## ✅ Functionality

- [ ] All features tested
- [ ] User authentication working
- [ ] Role-based access working
- [ ] Question submission working
- [ ] Strategy management working
- [ ] Map rendering correctly
- [ ] Mobile responsive
- [ ] Cross-browser tested

## ✅ Documentation

- [ ] README.md complete
- [ ] API documentation updated
- [ ] Deployment guide written
- [ ] User manual created
- [ ] Contributing guidelines clear
- [ ] License file included

## ✅ Infrastructure

- [ ] Domain name configured
- [ ] DNS records set
- [ ] SSL certificate installed
- [ ] Email service configured
- [ ] Monitoring setup
- [ ] Backup strategy in place
- [ ] Disaster recovery plan

## ✅ Legal & Compliance

- [ ] Privacy policy drafted
- [ ] Terms of service drafted
- [ ] Data protection compliance
- [ ] Cookie consent implemented
- [ ] Accessibility standards met

## ✅ Post-Deployment

- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Verify email delivery
- [ ] Test user registration
- [ ] Verify database connections
- [ ] Check all integrations
- [ ] Update status page

## 📝 Production Environment Variables

Create `.env.production` with:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
SECRET_KEY=<generate-strong-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://yourdomain.com

# Email (if configured)
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
```

## 🚀 Deployment Commands

```bash
# Build frontend
cd frontend
npm run build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Initialize database
docker-compose exec backend python init_db.py

# Check logs
docker-compose logs -f
```

---

**Complete this checklist before going live!**
