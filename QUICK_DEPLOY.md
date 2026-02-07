# 🚀 Quick Deploy Reference

## Your Configuration (Copy & Paste Ready!)

### 📊 Vercel Environment Variables
Deploy at: https://vercel.com/new

**Repository:** bashmore0207/scraperrr
**Root Directory:** `dashboard` ⚠️ IMPORTANT!

**Copy these 5 variables:**
```
NEXT_PUBLIC_SUPABASE_URL=https://tuuunaprwkqyvudknpaf.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1dXVuYXByd2txeXZ1ZGtucGFmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA0MTI4NjQsImV4cCI6MjA4NTk4ODg2NH0.JdUjAz4PAUf61arXGlDf6Ffs5uOh0kVGc0GKMEc46gA
CRON_SECRET=a1613f5df2897e6803fb7f77168a705d
GITHUB_TOKEN=<YOUR_GITHUB_TOKEN_HERE>
GITHUB_REPO=bashmore0207/scraperrr
```

> **Note:** Use the GitHub token you created with `repo` + `workflow` scopes

---

### 🔐 GitHub Secrets
Add at: https://github.com/bashmore0207/scraperrr/settings/secrets/actions

**Click "New repository secret" for each:**

**Secret 1:**
- Name: `NEXT_PUBLIC_SUPABASE_URL`
- Value: `https://tuuunaprwkqyvudknpaf.supabase.co`

**Secret 2:**
- Name: `SUPABASE_SERVICE_ROLE_KEY`
- Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1dXVuYXByd2txeXZ1ZGtucGFmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDQxMjg2NCwiZXhwIjoyMDg1OTg4ODY0fQ.WniTzZcp_rzDawXFO80NY8miwE9ngAi9opPJODvSOdo`

**Secret 3:**
- Name: `NEWSDATA_API_KEY`
- Value: `pub_7bad64ad479c43dd903a7860958ff611`

---

## ✅ Deployment Checklist

1. **Deploy to Vercel:**
   - [ ] Go to https://vercel.com/new
   - [ ] Import `bashmore0207/scraperrr`
   - [ ] Set root directory: `dashboard`
   - [ ] Paste 5 environment variables (above)
   - [ ] Click Deploy
   - [ ] Wait ~2 minutes
   - [ ] Get your URL: `https://your-app.vercel.app`

2. **Add GitHub Secrets:**
   - [ ] Go to https://github.com/bashmore0207/scraperrr/settings/secrets/actions
   - [ ] Add 3 secrets (above)
   - [ ] Click "New repository secret" for each

3. **Test Everything:**
   - [ ] Visit your Vercel URL
   - [ ] Check dashboard loads
   - [ ] Run scrapers: `python3 tools/run_all_scrapers.py`
   - [ ] Test API: `curl -X POST https://your-app.vercel.app/api/scrape -H "Authorization: Bearer a1613f5df2897e6803fb7f77168a705d"`
   - [ ] Check GitHub Actions: https://github.com/bashmore0207/scraperrr/actions

---

## 🧪 Test Commands

**Test Scraper API:**
```bash
# Replace YOUR_APP_URL with your actual Vercel URL
curl -X POST https://YOUR_APP_URL/api/scrape \
  -H "Authorization: Bearer a1613f5df2897e6803fb7f77168a705d"

# Should return:
# {"success":true,"message":"Scraper workflow triggered..."}
```

**Run Scrapers Locally:**
```bash
python3 tools/run_all_scrapers.py
```

**Check Database:**
```sql
-- In Supabase SQL Editor
SELECT * FROM articles ORDER BY published_at DESC LIMIT 10;
SELECT * FROM scraper_runs ORDER BY started_at DESC LIMIT 5;
```

---

## 📱 Quick Links

- **Repository:** https://github.com/bashmore0207/scraperrr
- **Deploy Vercel:** https://vercel.com/new
- **GitHub Secrets:** https://github.com/bashmore0207/scraperrr/settings/secrets/actions
- **GitHub Actions:** https://github.com/bashmore0207/scraperrr/actions
- **Supabase:** https://supabase.com/dashboard/project/tuuunaprwkqyvudknpaf

---

## 🎯 How Automation Works

```
Vercel Cron (every 24h)
    ↓
/api/scrape endpoint
    ↓
GitHub Actions API (with GITHUB_TOKEN)
    ↓
Workflow runs (.github/workflows/scrape.yml)
    ↓
Python scrapers execute
    ↓
Articles stored in Supabase
    ↓
Dashboard auto-updates
```

---

## 💰 Costs

**Total: $0/month** 🎉

- Vercel: Free (Hobby plan)
- Supabase: Free (500MB database)
- NewsData.io: Free (200 requests/day)
- GitHub Actions: Free (2000 minutes/month)

---

## 🆘 Troubleshooting

**Dashboard not showing articles?**
```bash
# Run scrapers manually first
python3 tools/run_all_scrapers.py
```

**GitHub Actions failing?**
- Check secrets are added correctly
- Verify token has `repo` + `workflow` scopes
- Review logs in Actions tab

**API trigger not working?**
- Verify CRON_SECRET matches in Vercel
- Check Authorization header format
- Review Vercel function logs

---

Built with 💜 by Claude Sonnet 4.5
