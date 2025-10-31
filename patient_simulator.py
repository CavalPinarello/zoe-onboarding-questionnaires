#!/usr/bin/env python3
"""
ZOE Adaptive Onboarding - Patient Journey Simulator
Simulates user responses and tracks adaptive expansion logic.
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta

class PatientSimulator:
    def __init__(self, schedule_file: str):
        with open(schedule_file, 'r') as f:
            data = json.load(f)
            self.schedule = data['schedule']
        
        self.user_responses = {}
        self.triggered_expansions = []
        self.daily_logs = {}
        
    def simulate_response(self, question: Dict) -> Any:
        """Simulate a realistic response based on question type"""
        
        answer_type = question['answer_type']
        
        if answer_type == 'boolean':
            # 30% chance of triggering expansions (realistic problematic sleep)
            return random.choice(['Yes', 'No']) if random.random() > 0.3 else 'Yes'
        
        elif answer_type == 'scale':
            # Skew toward middle-to-higher scores for sleep issues
            return random.randint(3, 8)
        
        elif answer_type == 'frequency':
            options = question.get('options', ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'])
            # Weight toward middle options
            weights = [10, 20, 40, 20, 10]
            return random.choices(options, weights=weights)[0]
        
        elif answer_type == 'numeric':
            if 'hours' in question['text'].lower():
                return random.uniform(5.5, 8.5)  # Sleep hours
            elif 'neck' in question['text'].lower():
                return random.uniform(14, 17)  # Neck circumference
            elif 'weight' in question['text'].lower():
                return random.randint(120, 200)
            elif 'height' in question['text'].lower():
                return random.randint(60, 75)
            return random.randint(1, 10)
        
        elif answer_type == 'text':
            return "Simulated User"
        
        elif answer_type == 'email':
            return "user@example.com"
        
        elif answer_type == 'date':
            # Random birthdate between 25-65 years old
            years_ago = random.randint(25, 65)
            birthdate = datetime.now() - timedelta(days=years_ago * 365)
            return birthdate.strftime('%Y-%m-%d')
        
        elif answer_type == 'single_choice':
            options = question.get('options', ['Option 1', 'Option 2', 'Option 3'])
            return random.choice(options) if options else 'Other'
        
        return "Simulated response"
    
    def check_expansion_trigger(self, question: Dict, response: Any, expansion_info: Dict) -> bool:
        """Check if a response triggers an expansion"""
        
        condition = expansion_info['condition'].upper()
        
        # Parse trigger conditions
        if 'YES' in condition:
            return response == 'Yes'
        
        elif 'OFTEN' in condition or 'ALWAYS' in condition:
            return response in ['Often', 'Always']
        
        elif 'ANY YES' in condition:
            return response == 'Yes'
        
        elif '>' in condition:
            # Numeric threshold
            try:
                threshold = float(condition.split('>')[1].strip().replace('in', ''))
                return float(response) > threshold
            except:
                return False
        
        return False
    
    def simulate_day(self, day_num: int, persona: str = 'balanced') -> Dict:
        """
        Simulate a single day's responses
        Personas: 'healthy', 'balanced', 'problematic'
        """
        
        day_schedule = self.schedule[str(day_num)]
        day_log = {
            'day': day_num,
            'date_simulated': datetime.now().isoformat(),
            'title': day_schedule['title'],
            'description': day_schedule['description'],
            'core_questions_completed': [],
            'expansions_triggered': [],
            'total_questions_answered': 0,
            'total_time_minutes': day_schedule['estimated_minutes']
        }
        
        # Answer core questions
        for question in day_schedule['core_questions']:
            response = self.simulate_response(question)
            
            self.user_responses[question['id']] = {
                'question_id': question['id'],
                'question_text': question['text'],
                'response': response,
                'day': day_num,
                'timestamp': datetime.now().isoformat()
            }
            
            day_log['core_questions_completed'].append({
                'id': question['id'],
                'text': question['text'][:60] + '...' if len(question['text']) > 60 else question['text'],
                'response': str(response)
            })
            day_log['total_questions_answered'] += 1
        
        # Check for triggered expansions
        for expansion in day_schedule.get('possible_expansions', []):
            trigger_q = expansion['trigger_question']
            
            if trigger_q['id'] in self.user_responses:
                response = self.user_responses[trigger_q['id']]['response']
                
                if self.check_expansion_trigger(trigger_q, response, expansion):
                    # Expansion triggered!
                    expansion_triggered = {
                        'trigger_question_id': trigger_q['id'],
                        'trigger_response': str(response),
                        'modules': [],
                        'additional_questions': 0
                    }
                    
                    for module_info in expansion['expansion_modules']:
                        module_name = module_info['module']
                        questions = module_info['questions']
                        
                        expansion_triggered['modules'].append(module_name)
                        expansion_triggered['additional_questions'] += len(questions)
                        
                        # Simulate responses to expansion questions
                        for exp_q in questions:
                            exp_response = self.simulate_response(exp_q)
                            self.user_responses[exp_q['id']] = {
                                'question_id': exp_q['id'],
                                'question_text': exp_q['text'],
                                'response': exp_response,
                                'day': day_num,
                                'module': module_name,
                                'expansion': True,
                                'timestamp': datetime.now().isoformat()
                            }
                            day_log['total_questions_answered'] += 1
                    
                    day_log['expansions_triggered'].append(expansion_triggered)
                    day_log['total_time_minutes'] += expansion['estimated_additional_minutes']
                    
                    self.triggered_expansions.append({
                        'day': day_num,
                        'modules': expansion_triggered['modules'],
                        'question_count': expansion_triggered['additional_questions']
                    })
        
        self.daily_logs[day_num] = day_log
        return day_log
    
    def simulate_full_journey(self, persona: str = 'balanced') -> Dict:
        """Simulate complete 14-day patient journey"""
        
        print(f"\n🎭 Simulating Patient Journey (Persona: {persona})")
        print("=" * 80)
        
        for day in range(1, 15):
            day_log = self.simulate_day(day, persona)
            
            expansion_note = ""
            if day_log['expansions_triggered']:
                exp_count = sum(e['additional_questions'] for e in day_log['expansions_triggered'])
                modules = [m for e in day_log['expansions_triggered'] for m in e['modules']]
                expansion_note = f" → Expanded: +{exp_count}q ({', '.join(modules)})"
            
            print(f"Day {day:2d} | {day_log['title']:20s} | "
                  f"{day_log['total_questions_answered']:3d} questions | "
                  f"~{day_log['total_time_minutes']:2d}min{expansion_note}")
        
        # Generate journey report
        total_questions = sum(log['total_questions_answered'] for log in self.daily_logs.values())
        total_time = sum(log['total_time_minutes'] for log in self.daily_logs.values())
        total_expansions = len(self.triggered_expansions)
        
        report = {
            'persona': persona,
            'simulation_date': datetime.now().isoformat(),
            'total_days': 14,
            'total_questions_answered': total_questions,
            'total_time_minutes': total_time,
            'expansions_triggered_count': total_expansions,
            'expansions_triggered': self.triggered_expansions,
            'daily_logs': self.daily_logs,
            'user_responses': self.user_responses
        }
        
        print("\n" + "=" * 80)
        print(f"📊 Journey Summary:")
        print(f"   Total Questions: {total_questions}")
        print(f"   Total Time: {total_time} minutes (~{total_time / 60:.1f} hours over 14 days)")
        print(f"   Expansions Triggered: {total_expansions}")
        print(f"   Average per Day: {total_questions / 14:.1f} questions, {total_time / 14:.1f} minutes")
        
        if self.triggered_expansions:
            print(f"\n🔄 Triggered Expansion Modules:")
            for expansion in self.triggered_expansions:
                print(f"   Day {expansion['day']}: {', '.join(expansion['modules'])} "
                      f"(+{expansion['question_count']} questions)")
        
        return report
    
    def save_journey_report(self, output_file: str, persona: str = 'balanced'):
        """Generate and save journey simulation report"""
        report = self.simulate_full_journey(persona)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Journey report saved to {output_file}")
        return report


if __name__ == '__main__':
    schedule_file = '/Users/martinkawalski/ZOE/data/14day_schedule.json'
    
    # Run simulations with different personas
    personas = ['balanced', 'healthy', 'problematic']
    
    for persona in personas:
        output_file = f'/Users/martinkawalski/ZOE/data/journey_simulation_{persona}.json'
        simulator = PatientSimulator(schedule_file)
        simulator.save_journey_report(output_file, persona)
        print("\n")
