# Deployment Checklist for Scraperrr

## ✅ Step 1: Push to GitHub

Your code is committed locally. Push it to GitHub:

```bash
# If you have SSH set up
git push -u origin main

# Or use GitHub CLI
gh auth login
git push -u origin main

# Or use personal access token
# Go to: GitHub Settings → Developer Settings → Personal Access Tokens
# Create token with 'repo' scope
# Then push with token as password
```

**Repository:** https://github.com/bashmore0207/scraperrr

---

## ✅ Step 2: Deploy Dashboard to Vercel

### 2.1 Create Vercel Account
- Go to [vercel.com](https://vercel.com)
- Sign in with GitHub

### 2.2 Import Repository
1. Click "Add New Project"
2. Import `bashmore0207/scraperrr`
3. **Important:** Set **Root Directory** to `dashboard`
4. Framework: Next.js (auto-detected)

### 2.3 Add Environment Variables

In Vercel project settings, add these:

**Required:**
```
NEXT_PUBLIC_SUPABASE_URL=https://tuuunaprwkqyvudknpaf.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1dXVuYXByd2txeXZ1ZGtucGFmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0MTI4NjQsImV4cCI6MjA4NTk4ODg2NH0.JdUjAz4PAUf61arXGlDf6Ffs5uOh0kVGc0GKMEc46gA
```

**For Automation (add after deployment):**
```
CRON_SECRET=<generate-random-string>
GITHUB_TOKEN=<your-github-personal-access-token>
GITHUB_REPO=bashmore0207/scraperrr
```

### 2.4 Deploy
Click **Deploy** and wait ~2 minutes!

---

## ✅ Step 3: Set Up Automated Scraping

### 3.1 Add GitHub Secrets

Go to: https://github.com/bashmore0207/scraperrr/settings/secrets/actions

Add these secrets:

```
NEXT_PUBLIC_SUPABASE_URL=https://tuuunaprwkqyvudknpaf.supabase.co

SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1dXVuYXByd2txeXZ1ZGtucGFmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDQxMjg2NCwiZXhwIjoyMDg1OTg4ODY0fQ.WniTzZcp_rzDawXFO80NY8miwE9ngAi9opPJODvSOdo

NEWSDATA_API_KEY=pub_7bad64ad479c43dd903a7860958ff611
```

### 3.2 Generate GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "Scraperrr Automation"
4. Scopes: Check `repo` and `workflow`
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### 3.3 Add to Vercel

Go back to Vercel → Settings → Environment Variables:

```
GITHUB_TOKEN=<paste-token-here>
GITHUB_REPO=bashmore0207/scraperrr
CRON_SECRET=<random-string-like-abc123xyz789>
```

---

## ✅ Step 4: Test Everything

### 4.1 Test Dashboard
Visit your Vercel URL (e.g., `scraperrr.vercel.app`)
- ✅ Dashboard loads
- ✅ Articles display
- ✅ Filters work
- ✅ Save button works

### 4.2 Test Scraper API
```bash
# Get your CRON_SECRET from Vercel
curl -X POST https://your-app.vercel.app/api/scrape \
  -H "Authorization: Bearer YOUR_CRON_SECRET"

# Should return:
# {"success":true,"message":"Scraper workflow triggered via GitHub Actions",...}
```

### 4.3 Verify GitHub Actions
1. Go to: https://github.com/bashmore0207/scraperrr/actions
2. You should see a workflow run
3. Check logs to verify scrapers ran successfully
4. Check Supabase for new articles

### 4.4 Verify Cron Job
- Wait 24 hours for automatic trigger
- Or manually trigger via API (step 4.2)
- Check GitHub Actions for new runs

---

## ✅ Quick Reference

**Your URLs:**
- Dashboard: `https://<your-app>.vercel.app`
- GitHub Repo: https://github.com/bashmore0207/scraperrr
- GitHub Actions: https://github.com/bashmore0207/scraperrr/actions
- Supabase: https://supabase.com/dashboard/project/tuuunaprwkqyvudknpaf

**Manual Scraper Run:**
```bash
# Local
python3 tools/run_all_scrapers.py

# Trigger Production
curl -X POST https://your-app.vercel.app/api/scrape \
  -H "Authorization: Bearer YOUR_CRON_SECRET"
```

**Check Data:**
```sql
-- Supabase SQL Editor
SELECT * FROM articles ORDER BY published_at DESC LIMIT 10;
SELECT * FROM scraper_runs ORDER BY started_at DESC LIMIT 5;
```

---

## 🎯 Success Criteria

- [ ] Code pushed to GitHub
- [ ] Dashboard deployed to Vercel
- [ ] Environment variables configured
- [ ] GitHub secrets added
- [ ] Manual API trigger works
- [ ] GitHub Actions workflow runs
- [ ] Articles appear in Supabase
- [ ] Dashboard displays articles
- [ ] Filters work correctly
- [ ] Save functionality works
- [ ] Cron job scheduled

---

## 🆘 Troubleshooting

**Dashboard not loading:**
- Check Vercel build logs
- Verify environment variables are set
- Ensure root directory is `dashboard`

**No articles showing:**
- Run scrapers manually: `python3 tools/run_all_scrapers.py`
- Check Supabase for data
- Verify API keys are valid

**GitHub Actions failing:**
- Check GitHub Secrets are set correctly
- Review workflow logs for errors
- Verify Supabase credentials

**API trigger not working:**
- Verify CRON_SECRET matches in Vercel
- Check Authorization header format
- Review Vercel function logs

---

## 📞 Support

- **README**: [README.md](README.md)
- **Progress**: [progress.md](progress.md)
- **Architecture**: [architecture/](architecture/)

---

Built with 💜 by Claude Sonnet 4.5
