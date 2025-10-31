// ZOE Sleep Assessment Application
class ZOEApp {
    constructor() {
        this.scheduleData = null;
        this.questionsData = null;
        this.currentDay = 1;
        this.currentQuestionIndex = 0;
        this.todayQuestions = [];
        this.userResponses = {};
        this.userData = {};
        this.expansionsTriggered = [];
        this.dayStartTime = null;
        
        this.loadData();
        this.loadProgress();
    }

    async loadData() {
        try {
            // Load schedule
            const scheduleResponse = await fetch('data/14day_schedule.json');
            const scheduleJson = await scheduleResponse.json();
            this.scheduleData = scheduleJson.schedule;
            
            // Load questions
            const questionsResponse = await fetch('data/questions.json');
            this.questionsData = await questionsResponse.json();
            
            console.log('Data loaded successfully');
        } catch (error) {
            console.error('Error loading data:', error);
            alert('Error loading questionnaire data. Please refresh the page.');
        }
    }

    loadProgress() {
        const saved = localStorage.getItem('zoeProgress');
        if (saved) {
            const data = JSON.parse(saved);
            this.currentDay = data.currentDay || 1;
            this.userResponses = data.userResponses || {};
            this.userData = data.userData || {};
            this.expansionsTriggered = data.expansionsTriggered || [];
        }
    }

    saveProgress() {
        const data = {
            currentDay: this.currentDay,
            userResponses: this.userResponses,
            userData: this.userData,
            expansionsTriggered: this.expansionsTriggered,
            lastUpdated: new Date().toISOString()
        };
        localStorage.setItem('zoeProgress', JSON.stringify(data));
    }

    startJourney() {
        const name = document.getElementById('userName').value.trim();
        if (!name) {
            alert('Please enter your name to begin');
            return;
        }

        this.userData.name = name;
        this.userData.email = document.getElementById('userEmail').value.trim();
        this.userData.startedAt = new Date().toISOString();
        
        this.saveProgress();
        this.showDayScreen();
    }

    showScreen(screenId) {
        document.querySelectorAll('.welcome-screen, .day-screen, .question-screen, .complete-screen').forEach(el => {
            el.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }

    showDayScreen() {
        const dayData = this.scheduleData[this.currentDay.toString()];
        if (!dayData) {
            this.showComplete();
            return;
        }

        // Show progress bar
        document.getElementById('progressContainer').style.display = 'block';
        this.updateProgress();

        // Prepare today's questions
        this.todayQuestions = [...dayData.core_questions];
        
        // Check for expansions from previous responses
        if (dayData.possible_expansions && dayData.possible_expansions.length > 0) {
            dayData.possible_expansions.forEach(expansion => {
                const triggerQ = expansion.trigger_question;
                const response = this.userResponses[triggerQ.id];
                
                if (response && this.checkTrigger(response.response, expansion.condition)) {
                    // Add expansion questions
                    expansion.expansion_modules.forEach(module => {
                        this.todayQuestions.push(...module.questions);
                    });
                    
                    // Show expansion alert
                    this.showExpansionAlert(expansion);
                    
                    // Track expansion
                    this.expansionsTriggered.push({
                        day: this.currentDay,
                        modules: expansion.expansion_modules.map(m => m.module),
                        questionCount: expansion.total_additional_questions
                    });
                }
            });
        }

        // Update UI
        document.getElementById('dayNumber').textContent = `Day ${dayData.day}`;
        document.getElementById('dayTitle').textContent = dayData.title;
        document.getElementById('dayDescription').textContent = dayData.description;
        document.getElementById('todayQuestions').textContent = this.todayQuestions.length;
        document.getElementById('todayMinutes').textContent = Math.ceil(this.todayQuestions.length / 2);

        this.showScreen('dayScreen');
        this.currentQuestionIndex = 0;
        this.dayStartTime = new Date();
    }

    showExpansionAlert(expansion) {
        const alertHtml = `
            <div class="expansion-alert">
                <h3>📋 Additional Assessment Recommended</h3>
                <p>Based on your previous responses, we'd like to dive deeper into this area.</p>
                <p><strong>Additional questions:</strong> ${expansion.total_additional_questions}</p>
                <p><strong>Estimated time:</strong> ${expansion.estimated_additional_minutes} more minutes</p>
                <p>This helps us provide better personalized insights for your sleep health.</p>
            </div>
        `;
        document.getElementById('expansionAlert').innerHTML = alertHtml;
    }

    checkTrigger(response, condition) {
        const cond = condition.toUpperCase();
        const resp = String(response).toUpperCase();
        
        if (cond.includes('YES')) {
            return resp === 'YES';
        } else if (cond.includes('OFTEN') || cond.includes('ALWAYS')) {
            return resp === 'OFTEN' || resp === 'ALWAYS';
        } else if (cond.includes('ANY YES')) {
            return resp === 'YES';
        } else if (cond.includes('>')) {
            const threshold = parseFloat(cond.split('>')[1]);
            return parseFloat(response) > threshold;
        }
        return false;
    }

    startDayQuestions() {
        this.showQuestionScreen();
    }

    showQuestionScreen() {
        if (this.currentQuestionIndex >= this.todayQuestions.length) {
            this.completeDayscreen();
            return;
        }

        const question = this.todayQuestions[this.currentQuestionIndex];
        
        // Update question display
        document.getElementById('questionNumber').textContent = 
            `Question ${this.currentQuestionIndex + 1} of ${this.todayQuestions.length}`;
        document.getElementById('questionText').textContent = question.text;

        // Create answer input based on question type
        const answerContainer = document.getElementById('answerContainer');
        answerContainer.innerHTML = this.createAnswerInput(question);

        // Show/hide previous button
        document.getElementById('prevBtn').style.display = 
            this.currentQuestionIndex > 0 ? 'inline-block' : 'none';

        // Update next button text
        document.getElementById('nextBtn').textContent = 
            this.currentQuestionIndex === this.todayQuestions.length - 1 ? 'Complete Day' : 'Next';

        // Pre-fill if already answered
        const savedResponse = this.userResponses[question.id];
        if (savedResponse) {
            this.prefillAnswer(question, savedResponse.response);
        }

        this.showScreen('questionScreen');
        this.updateProgress();
    }

    createAnswerInput(question) {
        const answerType = question.answer_type;
        
        if (answerType === 'boolean' && question.options.length > 0) {
            return this.createRadioOptions(question.options);
        } else if (answerType === 'frequency' && question.options.length > 0) {
            return this.createRadioOptions(question.options);
        } else if (answerType === 'single_choice' && question.options.length > 0) {
            return this.createRadioOptions(question.options);
        } else if (answerType === 'scale') {
            return this.createScaleInput(question);
        } else if (answerType === 'numeric') {
            return `<input type="number" class="answer-input" id="answerInput" placeholder="Enter your answer">`;
        } else if (answerType === 'email') {
            return `<input type="email" class="answer-input" id="answerInput" placeholder="your@email.com">`;
        } else if (answerType === 'date') {
            return `<input type="date" class="answer-input" id="answerInput">`;
        } else {
            return `<input type="text" class="answer-input" id="answerInput" placeholder="Type your answer">`;
        }
    }

    createRadioOptions(options) {
        return `
            <div class="answer-options">
                ${options.map((opt, idx) => `
                    <div class="answer-option" onclick="app.selectOption(${idx})">
                        <input type="radio" name="answer" value="${opt}" id="opt${idx}">
                        <label for="opt${idx}" style="cursor: pointer; flex: 1;">${opt}</label>
                    </div>
                `).join('')}
            </div>
        `;
    }

    createScaleInput(question) {
        // Determine scale range from question text or options
        let min = 0, max = 10;
        const text = question.text.toLowerCase();
        
        if (text.includes('1-10') || text.includes('1 to 10')) {
            min = 1;
            max = 10;
        }

        const values = [];
        for (let i = min; i <= max; i++) {
            values.push(i);
        }

        return `
            <div class="scale-input">
                <div class="scale-values">
                    ${values.map(val => `
                        <div class="scale-value" onclick="app.selectScale(${val})" data-value="${val}">
                            ${val}
                        </div>
                    `).join('')}
                </div>
                <div class="scale-labels">
                    <span>${text.includes('disagree') ? 'Strongly Disagree' : 'Not at all'}</span>
                    <span>${text.includes('agree') ? 'Strongly Agree' : 'Very much'}</span>
                </div>
            </div>
        `;
    }

    selectOption(index) {
        // Remove previous selections
        document.querySelectorAll('.answer-option').forEach(el => el.classList.remove('selected'));
        
        // Select current
        document.querySelectorAll('.answer-option')[index].classList.add('selected');
        document.getElementById(`opt${index}`).checked = true;
    }

    selectScale(value) {
        // Remove previous selections
        document.querySelectorAll('.scale-value').forEach(el => el.classList.remove('selected'));
        
        // Select current
        event.target.classList.add('selected');
        event.target.setAttribute('data-selected', value);
    }

    prefillAnswer(question, response) {
        if (question.answer_type === 'scale') {
            const scaleValue = document.querySelector(`.scale-value[data-value="${response}"]`);
            if (scaleValue) {
                scaleValue.classList.add('selected');
                scaleValue.setAttribute('data-selected', response);
            }
        } else if (question.options && question.options.length > 0) {
            const optIndex = question.options.indexOf(response);
            if (optIndex >= 0) {
                this.selectOption(optIndex);
            }
        } else {
            const input = document.getElementById('answerInput');
            if (input) {
                input.value = response;
            }
        }
    }

    getCurrentAnswer() {
        const question = this.todayQuestions[this.currentQuestionIndex];
        
        if (question.answer_type === 'scale') {
            const selected = document.querySelector('.scale-value.selected');
            return selected ? selected.getAttribute('data-value') : null;
        } else if (question.options && question.options.length > 0) {
            const selected = document.querySelector('input[name="answer"]:checked');
            return selected ? selected.value : null;
        } else {
            const input = document.getElementById('answerInput');
            return input ? input.value : null;
        }
    }

    nextQuestion() {
        const answer = this.getCurrentAnswer();
        
        if (!answer || answer.trim() === '') {
            alert('Please answer the question before continuing');
            return;
        }

        // Save response
        const question = this.todayQuestions[this.currentQuestionIndex];
        this.userResponses[question.id] = {
            question_id: question.id,
            question_text: question.text,
            response: answer,
            day: this.currentDay,
            timestamp: new Date().toISOString()
        };

        this.saveProgress();

        // Move to next question
        this.currentQuestionIndex++;
        this.showQuestionScreen();
    }

    previousQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            this.showQuestionScreen();
        }
    }

    completeDayScreen() {
        const dayData = this.scheduleData[this.currentDay.toString()];
        const timeSpent = Math.round((new Date() - this.dayStartTime) / 60000); // minutes

        // Update completion screen
        document.getElementById('completeMessage').textContent = 
            `Great work today! You've completed Day ${this.currentDay}.`;
        document.getElementById('summaryQuestions').textContent = this.todayQuestions.length;
        document.getElementById('summaryTime').textContent = timeSpent;

        // Show expansion summary if any
        const todayExpansions = this.expansionsTriggered.filter(e => e.day === this.currentDay);
        if (todayExpansions.length > 0) {
            const modules = todayExpansions.flatMap(e => e.modules);
            document.getElementById('expansionSummary').innerHTML = 
                `<p><strong>Expanded modules:</strong> ${modules.join(', ')}</p>`;
        } else {
            document.getElementById('expansionSummary').innerHTML = '';
        }

        // Generate day summary badges
        this.generateDaySummary();

        // Update next day button
        const nextDayBtn = document.getElementById('nextDayBtn');
        if (this.currentDay >= 14) {
            nextDayBtn.textContent = 'View Final Results';
        } else {
            nextDayBtn.textContent = 'Continue to Next Day';
        }

        this.showScreen('completeScreen');
    }

    generateDaySummary() {
        const container = document.getElementById('daySummary');
        let html = '';
        
        for (let day = 1; day <= 14; day++) {
            let className = 'day-badge';
            if (day < this.currentDay) {
                className += ' completed';
            } else if (day === this.currentDay) {
                className += ' current';
            }
            html += `<div class="${className}">${day}</div>`;
        }
        
        container.innerHTML = html;
    }

    continueToNextDay() {
        if (this.currentDay >= 14) {
            this.showFinalResults();
            return;
        }

        this.currentDay++;
        this.saveProgress();
        this.showDayScreen();
    }

    viewResults() {
        // Export responses as JSON
        const exportData = {
            userData: this.userData,
            currentDay: this.currentDay,
            responses: this.userResponses,
            expansionsTriggered: this.expansionsTriggered,
            completedAt: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `zoe-assessment-${this.userData.name}-day${this.currentDay}.json`;
        a.click();
    }

    showFinalResults() {
        alert('Congratulations! You\'ve completed the 14-day ZOE Sleep Assessment. Your responses have been saved.');
        this.viewResults();
    }

    updateProgress() {
        const totalDays = 14;
        const progress = ((this.currentDay - 1) / totalDays) * 100;
        
        document.getElementById('progressFill').style.width = `${progress}%`;
        document.getElementById('progressText').textContent = `Day ${this.currentDay} of ${totalDays}`;
        document.getElementById('completionText').textContent = `${Math.round(progress)}% complete`;
    }

    resetJourney() {
        if (confirm('Are you sure you want to reset your journey? All progress will be lost.')) {
            localStorage.removeItem('zoeProgress');
            location.reload();
        }
    }
}

// Initialize app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new ZOEApp();
    
    // Check if user has existing progress
    const saved = localStorage.getItem('zoeProgress');
    if (saved) {
        const data = JSON.parse(saved);
        if (data.userData && data.userData.name) {
            // Resume journey
            if (confirm(`Welcome back, ${data.userData.name}! Continue from Day ${data.currentDay}?`)) {
                app.showDayScreen();
            } else {
                document.getElementById('welcomeScreen').classList.add('active');
            }
        }
    }
});
