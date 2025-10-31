# 🧪 ZOE Sleep Assessment - Testing Guide

**Live App:** https://cavalpinarello.github.io/zoe-onboarding-questionnaires/app.html

---

## 📋 Quick Start for Testers

### 1. Access the App
Click the live app link above - it works on any device (desktop, tablet, mobile)

### 2. Start Your Journey
- Enter your name (required)
- Optionally add email
- Click "Start Your Journey"

### 3. Answer Questions
You'll go through a 14-day assessment journey:
- **Days 1-3:** Basic demographics and initial screening
- **Days 4-6:** Gateway questions that may trigger expansions
- **Days 7-14:** Lifestyle, environment, and health questions

### 4. Experience Adaptive Logic
Try answering "Yes" to these gateway questions to trigger expansions:

**Day 4 - Sleep Difficulties:**
- Question: "Do you have trouble falling asleep, staying asleep, or waking too early?"
- Answer: **Yes**
- Result: System adds 16 more questions about insomnia (DBAS-16 scale)

**Day 5 - Daytime Function:**
- Question: "Do you feel excessively tired or sleepy during the day?"
- Answer: **Often** or **Always**
- Result: System adds 19 questions about fatigue and functioning

---

## 🎯 Testing Scenarios

### Scenario 1: Healthy Sleeper (Minimal Expansions)
Answer most gateway questions with "No" or "Rarely"
- **Expected:** 30-35 questions total
- **Expected Time:** ~40 minutes over 14 days
- **Expected Expansions:** 0-1

### Scenario 2: Moderate Sleep Issues (Some Expansions)
Answer some gateway questions positively
- **Expected:** 45-60 questions total
- **Expected Time:** ~50-70 minutes over 14 days
- **Expected Expansions:** 2-3

### Scenario 3: Multiple Sleep Problems (Many Expansions)
Answer most gateway questions positively
- **Expected:** 65-90 questions total
- **Expected Time:** ~75-110 minutes over 14 days
- **Expected Expansions:** 4-6

---

## 🔄 Testing Multiple Patients

You can test multiple patient journeys simultaneously:

### Method 1: Different Browser Sessions
1. **Regular browser window** = Patient 1
2. **Incognito/Private window** = Patient 2
3. **Different browser** (Chrome vs Firefox) = Patient 3

### Method 2: Different Devices
- Your laptop = Patient 1
- Your phone = Patient 2
- Tablet = Patient 3

Each maintains separate progress via browser local storage!

---

## 💾 Progress Persistence

The app automatically saves your progress:
- Close the browser and reopen = Resume exactly where you left off
- Answer a few questions, come back tomorrow = Your progress is saved
- Data stored locally in your browser (not sent to any server)

To **reset and start fresh:**
1. Open browser developer tools (F12)
2. Go to Application > Local Storage
3. Find `zoeProgress` and delete it
4. Refresh the page

---

## 📤 Exporting Responses

After completing any day:
1. Click **"View My Responses"** button
2. Downloads a JSON file with all your answers
3. File format: `zoe-assessment-[YourName]-day[X].json`

This JSON contains:
- Your demographic info
- All question responses
- Timestamps
- Triggered expansions
- Progress metadata

---

## 🐛 What to Test & Report

### Functionality Testing
- [ ] Can start the journey with name input
- [ ] Questions display correctly for each day
- [ ] All answer types work (Yes/No, scales, text input)
- [ ] Can navigate Previous/Next between questions
- [ ] Progress saves and resumes correctly
- [ ] Expansions trigger on correct responses
- [ ] Day completion summary shows accurate data
- [ ] Export function downloads valid JSON
- [ ] Progress bar updates correctly

### UX Testing
- [ ] Instructions are clear
- [ ] Question text is readable
- [ ] Answer options are intuitive
- [ ] Time estimates feel accurate
- [ ] Expansion alerts are not overwhelming
- [ ] Mobile experience is smooth
- [ ] Load times are acceptable

### Adaptive Logic Testing
- [ ] Day 4: Insomnia gateway triggers DBAS-16
- [ ] Day 5: Daytime sleepiness triggers ESS/FOSQ/FSS
- [ ] Day 6: Snoring triggers STOP-BANG
- [ ] Expansion questions appear in same day
- [ ] Question count matches expansion alert

---

## 📝 Reporting Issues

When you find a bug or have feedback, please note:

1. **What happened** (the issue/bug)
2. **What you expected** (correct behavior)
3. **Steps to reproduce** (how to trigger it)
4. **Your environment** (browser, device, OS)
5. **Screenshots** (if visual issue)

**Report to:** Martin Caval or create GitHub issue

---

## 💡 Testing Tips

### Tip 1: Use Realistic Responses
Try to answer as you genuinely would - this tests the real user flow

### Tip 2: Test Edge Cases
- Very long text answers
- Skipping optional fields
- Rapid clicking
- Browser back button behavior

### Tip 3: Test on Different Devices
Mobile vs desktop can reveal responsive design issues

### Tip 4: Check Console for Errors
Open developer tools (F12) and watch the Console tab for any red errors

### Tip 5: Test the Full 14-Day Journey
At least one tester should complete all 14 days to validate the complete flow

---

## 🎨 Question Types You'll Encounter

| Type | Example | How to Answer |
|------|---------|---------------|
| **Boolean** | "Do you snore?" | Click Yes/No |
| **Frequency** | "How often do you feel tired?" | Click Never/Rarely/Sometimes/Often/Always |
| **Scale (0-10)** | "Rate your sleep quality" | Click number 0-10 |
| **Text Input** | "What's your name?" | Type in text box |
| **Number Input** | "What's your height?" | Type number |
| **Date Input** | "Date of birth" | Pick from calendar |
| **Email Input** | "Your email" | Type email address |

---

## 📊 Expected Day Breakdown

| Day | Theme | Core Questions | Potential Expansions |
|-----|-------|----------------|---------------------|
| 1 | Welcome | 3 | None |
| 2 | Basic Profile | 4 | None |
| 3 | Sleep Quality | 2 | None |
| 4 | Sleep Difficulties | 1 | +16 (DBAS-16) |
| 5 | Daytime Energy | 1 | +19 (ESS, FOSQ, FSS) |
| 6 | Breathing & Sleep | 3 | +18 (STOP-BANG, Berlin) |
| 7-14 | Various Topics | 2-3 each | Module-specific |

---

## ✅ Testing Checklist

### Before Starting
- [ ] App loads without errors
- [ ] Welcome screen displays correctly
- [ ] Can enter name and email

### During Journey
- [ ] Each day's questions load
- [ ] All answer types work
- [ ] Progress saves between sessions
- [ ] Expansions trigger correctly
- [ ] Time estimates are reasonable

### After Completion
- [ ] Day summary is accurate
- [ ] Can export responses
- [ ] JSON file is valid
- [ ] Can continue to next day

### Cross-Browser Testing
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Mobile browsers

---

## 🚀 Advanced Testing

### Performance Testing
- Load app on slow connection (throttle network)
- Try with 100+ questions (trigger all expansions)
- Test on older devices/browsers

### Data Integrity Testing
- Export JSON after each day
- Verify all responses are captured
- Check timestamp accuracy
- Confirm expansion tracking

### Accessibility Testing
- Try keyboard-only navigation (Tab, Enter)
- Test with screen reader (if available)
- Check color contrast
- Verify font sizes are readable

---

## 📞 Support & Questions

**Project Owner:** Martin Caval  
**Email:** caval.apps@gmail.com  
**Linear Project:** [ZOE Onboarding Questionnaires](https://linear.app/sleepos/project/zoe-onboarding-questionnaires-1c7dc3bd90f7)  
**GitHub Repo:** [zoe-onboarding-questionnaires](https://github.com/CavalPinarello/zoe-onboarding-questionnaires)

---

## 🎉 Thank You for Testing!

Your feedback helps us build a better sleep health assessment tool. Every bug you find, every suggestion you make, makes ZOE better for our users.

**Happy Testing! 💤**
