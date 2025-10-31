#!/usr/bin/env python3
"""
ZOE Adaptive Onboarding - 14-Day Question Distribution Algorithm
Distributes questions intelligently across 14 days with adaptive expansion logic.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

class QuestionDistributor:
    def __init__(self, questions_file: str, rules_file: str):
        with open(questions_file, 'r') as f:
            self.questions = json.load(f)
        
        with open(rules_file, 'r') as f:
            self.conditional_rules = json.load(f)
        
        self.core_questions = [q for q in self.questions if q['module'] == 'CORE']
        self.expansion_questions_by_module = defaultdict(list)
        
        for q in self.questions:
            if q['module'] != 'CORE':
                self.expansion_questions_by_module[q['module']].append(q)
    
    def distribute_14_days(self) -> Dict[int, Any]:
        """
        Distribute core questions across 14 days with intelligent pacing.
        Strategy:
        - Days 1-3: Demographics + Initial screening (gateway questions)
        - Days 4-7: Sleep quality and quantity assessment
        - Days 8-10: Circadian rhythm and chronotype
        - Days 11-14: Lifestyle, environment, and wrap-up
        - Target: 2-4 core questions per day
        """
        
        daily_schedule = {}
        
        # Group questions by section/theme
        demographics = [q for q in self.core_questions if q['section'] and 'DEMO' in q['section'].upper()]
        sleep_quality = [q for q in self.core_questions if q['section'] and 'SLEEP QUALITY' in q['section'].upper()]
        insomnia_screen = [q for q in self.core_questions if q['section'] and 'INSOMNIA' in q['section'].upper()]
        daytime_function = [q for q in self.core_questions if q['section'] and 'DAYTIME' in q['section'].upper()]
        apnea_screen = [q for q in self.core_questions if q['section'] and 'APNEA' in q['section'].upper()]
        
        # Unclassified core questions
        other_core = [q for q in self.core_questions 
                     if q not in demographics + sleep_quality + insomnia_screen + daytime_function + apnea_screen]
        
        # Day 1-2: Welcome + Demographics
        daily_schedule[1] = {
            'day': 1,
            'title': 'Welcome to ZOE',
            'description': 'Let\'s start with some basic information about you.',
            'core_questions': demographics[:3],
            'estimated_minutes': 2,
            'can_trigger_expansion': False
        }
        
        daily_schedule[2] = {
            'day': 2,
            'title': 'Basic Profile',
            'description': 'A few more details to personalize your assessment.',
            'core_questions': demographics[3:] + sleep_quality[:1],
            'estimated_minutes': 2,
            'can_trigger_expansion': False
        }
        
        # Day 3: Initial Sleep Quality Screening
        daily_schedule[3] = {
            'day': 3,
            'title': 'Sleep Quality Check',
            'description': 'How has your sleep been lately?',
            'core_questions': sleep_quality[1:],
            'estimated_minutes': 2,
            'can_trigger_expansion': False
        }
        
        # Day 4: Insomnia Gateway (CRITICAL)
        daily_schedule[4] = {
            'day': 4,
            'title': 'Sleep Difficulties',
            'description': 'Understanding your sleep patterns.',
            'core_questions': insomnia_screen,
            'estimated_minutes': 3,
            'can_trigger_expansion': True,
            'trigger_note': 'If you report sleep difficulties, we\'ll ask some additional questions to better understand your situation.'
        }
        
        # Day 5: Daytime Function Gateway
        daily_schedule[5] = {
            'day': 5,
            'title': 'Daytime Energy',
            'description': 'How do you feel during the day?',
            'core_questions': daytime_function,
            'estimated_minutes': 3,
            'can_trigger_expansion': True,
            'trigger_note': 'Excessive daytime sleepiness may require deeper assessment.'
        }
        
        # Day 6: Sleep Apnea Gateway
        daily_schedule[6] = {
            'day': 6,
            'title': 'Breathing & Sleep',
            'description': 'Checking for breathing-related sleep issues.',
            'core_questions': apnea_screen,
            'estimated_minutes': 3,
            'can_trigger_expansion': True,
            'trigger_note': 'Snoring or breathing pauses during sleep are important indicators.'
        }
        
        # Days 7-14: Distribute remaining core questions
        remaining_questions = other_core
        questions_per_day = max(2, len(remaining_questions) // 8)
        
        day_num = 7
        themes = [
            ('Circadian Rhythm', 'Understanding your natural sleep-wake cycle.'),
            ('Sleep Environment', 'How your bedroom affects your sleep.'),
            ('Lifestyle Factors', 'Daily habits that impact sleep.'),
            ('Mental Health', 'Stress, mood, and sleep connection.'),
            ('Physical Health', 'Your overall health and sleep.'),
            ('Social Factors', 'Relationships and sleep patterns.'),
            ('Technology Use', 'Screen time and sleep.'),
            ('Final Questions', 'Completing your sleep profile.')
        ]
        
        for i in range(0, len(remaining_questions), questions_per_day):
            if day_num > 14:
                break
            
            theme_idx = min(day_num - 7, len(themes) - 1)
            theme, desc = themes[theme_idx]
            
            day_questions = remaining_questions[i:i + questions_per_day]
            
            daily_schedule[day_num] = {
                'day': day_num,
                'title': theme,
                'description': desc,
                'core_questions': day_questions,
                'estimated_minutes': 2 + len(day_questions) // 2,
                'can_trigger_expansion': False
            }
            
            day_num += 1
        
        return daily_schedule
    
    def add_expansion_logic(self, daily_schedule: Dict[int, Any]) -> Dict[int, Any]:
        """
        Add expansion module information to schedule based on conditional rules.
        """
        
        # Map trigger questions to expansion modules
        trigger_map = {}
        for rule in self.conditional_rules:
            trigger_q_id = rule['trigger_question_id']
            modules = rule['expanded_modules']
            
            trigger_map[trigger_q_id] = {
                'condition': rule['condition'],
                'modules': modules,
                'rule_text': rule['rule_text']
            }
        
        # Add expansion info to each day
        for day_num, day_info in daily_schedule.items():
            day_info['possible_expansions'] = []
            
            for question in day_info['core_questions']:
                if question['id'] in trigger_map:
                    trigger_info = trigger_map[question['id']]
                    
                    # Calculate expansion question count
                    expansion_count = 0
                    expansion_details = []
                    
                    for module_name in trigger_info['modules']:
                        if module_name in self.expansion_questions_by_module:
                            module_questions = self.expansion_questions_by_module[module_name]
                            expansion_count += len(module_questions)
                            expansion_details.append({
                                'module': module_name,
                                'question_count': len(module_questions),
                                'questions': module_questions
                            })
                    
                    day_info['possible_expansions'].append({
                        'trigger_question': question,
                        'condition': trigger_info['condition'],
                        'expansion_modules': expansion_details,
                        'total_additional_questions': expansion_count,
                        'estimated_additional_minutes': expansion_count // 2
                    })
            
            # Update estimated time range if expansions possible
            if day_info['possible_expansions']:
                max_additional = sum(exp['total_additional_questions'] 
                                    for exp in day_info['possible_expansions'])
                max_additional_minutes = max_additional // 2
                
                day_info['estimated_minutes_range'] = {
                    'min': day_info['estimated_minutes'],
                    'max': day_info['estimated_minutes'] + max_additional_minutes
                }
        
        return daily_schedule
    
    def generate_schedule(self, output_file: str = None):
        """Generate complete 14-day schedule with expansion logic"""
        
        print("🗓️  Generating 14-day distribution schedule...")
        
        schedule = self.distribute_14_days()
        schedule = self.add_expansion_logic(schedule)
        
        # Calculate statistics
        total_core = sum(len(day['core_questions']) for day in schedule.values())
        days_with_expansions = sum(1 for day in schedule.values() if day['can_trigger_expansion'])
        
        stats = {
            'total_days': 14,
            'total_core_questions': total_core,
            'days_with_potential_expansions': days_with_expansions,
            'average_questions_per_day': total_core / 14,
            'schedule': schedule
        }
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved 14-day schedule to {output_file}")
        
        # Print summary
        print(f"\n📊 Schedule Summary:")
        print(f"   Total Core Questions: {total_core}")
        print(f"   Average per Day: {total_core / 14:.1f}")
        print(f"   Days with Potential Expansions: {days_with_expansions}")
        
        print(f"\n📅 Daily Breakdown:")
        for day_num in sorted(schedule.keys()):
            day = schedule[day_num]
            q_count = len(day['core_questions'])
            time = day['estimated_minutes']
            expansion = " 🔄" if day['can_trigger_expansion'] else ""
            
            print(f"   Day {day_num:2d}: {q_count} questions (~{time}min) - {day['title']}{expansion}")
            
            if day['possible_expansions']:
                for exp in day['possible_expansions']:
                    print(f"           ↳ May expand: +{exp['total_additional_questions']} questions "
                          f"(+{exp['estimated_additional_minutes']}min)")
        
        return stats


if __name__ == '__main__':
    questions_file = '/Users/martinkawalski/ZOE/data/questions.json'
    rules_file = '/Users/martinkawalski/ZOE/data/conditional_rules.json'
    output_file = '/Users/martinkawalski/ZOE/data/14day_schedule.json'
    
    distributor = QuestionDistributor(questions_file, rules_file)
    distributor.generate_schedule(output_file)
