import json
import random

years = [2023, 2024, 2025]

# Diverse company data with randomly assigned years
companies_base = [
    {"name": "Amazon", "eligibility_cgpa": 7.5, "branches_allowed": ["CSE", "IT", "ECE"], "rounds": "1 OA, 2 Tech, 1 Bar Raiser", "package_range": "30-45 LPA", "number_of_offers": 12},
    {"name": "Microsoft", "eligibility_cgpa": 8.0, "branches_allowed": ["CSE", "IT"], "rounds": "1 OA, 3 Tech, 1 HR", "package_range": "40-50 LPA", "number_of_offers": 8},
    {"name": "Google", "eligibility_cgpa": 8.5, "branches_allowed": ["CSE"], "rounds": "1 Phone, 4 Tech, 1 Googlyness", "package_range": "50-65 LPA", "number_of_offers": 5},
    {"name": "Deloitte", "eligibility_cgpa": 6.5, "branches_allowed": ["CSE", "IT", "ECE", "EEE"], "rounds": "1 Aptitude, 1 Group Discussion, 1 Tech+HR", "package_range": "7-9 LPA", "number_of_offers": 45},
    {"name": "TCS", "eligibility_cgpa": 6.0, "branches_allowed": ["All Branches"], "rounds": "1 NQT, 1 Tech, 1 HR", "package_range": "3.3-7 LPA", "number_of_offers": 150},
    {"name": "Infosys", "eligibility_cgpa": 6.0, "branches_allowed": ["All Branches"], "rounds": "1 Aptitude, 1 Tech, 1 HR", "package_range": "3.6-8 LPA", "number_of_offers": 120},
    {"name": "Wipro", "eligibility_cgpa": 6.0, "branches_allowed": ["All Branches"], "rounds": "1 Aptitude+Coding, 1 Tech+HR", "package_range": "3.5-6.5 LPA", "number_of_offers": 100},
    {"name": "Cisco", "eligibility_cgpa": 7.0, "branches_allowed": ["CSE", "IT", "ECE"], "rounds": "1 OA, 2 Tech, 1 Managerial", "package_range": "15-20 LPA", "number_of_offers": 15},
    {"name": "Goldman Sachs", "eligibility_cgpa": 7.5, "branches_allowed": ["CSE", "IT", "ECE", "EEE"], "rounds": "1 Aptitude+Coding, 2 Tech, 1 HR", "package_range": "20-25 LPA", "number_of_offers": 10},
    {"name": "Atlassian", "eligibility_cgpa": 7.5, "branches_allowed": ["CSE", "IT"], "rounds": "1 OA, 1 Machine Coding, 2 Tech, 1 Values", "package_range": "45-60 LPA", "number_of_offers": 4},
    {"name": "Adobe", "eligibility_cgpa": 7.5, "branches_allowed": ["CSE", "IT"], "rounds": "1 OA, 2 Tech, 1 Director", "package_range": "35-42 LPA", "number_of_offers": 7},
    {"name": "Flipkart", "eligibility_cgpa": 7.0, "branches_allowed": ["CSE", "IT", "ECE"], "rounds": "1 OA, 2 Tech, 1 Hiring Manager", "package_range": "28-32 LPA", "number_of_offers": 14},
    {"name": "Paytm", "eligibility_cgpa": 6.5, "branches_allowed": ["CSE", "IT", "ECE"], "rounds": "1 OA, 2 Tech, 1 HR", "package_range": "12-16 LPA", "number_of_offers": 25},
    {"name": "Zomato", "eligibility_cgpa": 7.0, "branches_allowed": ["CSE", "IT"], "rounds": "1 OA, 2 Tech, 1 Founder", "package_range": "25-30 LPA", "number_of_offers": 8},
    {"name": "Uber", "eligibility_cgpa": 8.0, "branches_allowed": ["CSE"], "rounds": "1 OA, 1 Machine Coding, 2 Tech", "package_range": "40-55 LPA", "number_of_offers": 3},
    {"name": "Salesforce", "eligibility_cgpa": 7.5, "branches_allowed": ["CSE", "IT"], "rounds": "1 HackerRank OA, 2 Tech, 1 HR", "package_range": "28-34 LPA", "number_of_offers": 9},
    {"name": "Oracle", "eligibility_cgpa": 7.0, "branches_allowed": ["CSE", "IT", "ECE"], "rounds": "1 OA, 3 Tech", "package_range": "18-24 LPA", "number_of_offers": 18},
    {"name": "IBM", "eligibility_cgpa": 6.5, "branches_allowed": ["CSE", "IT", "ECE", "EEE"], "rounds": "1 Cognitive Ability, 1 Coding, 1 Tech+HR", "package_range": "8-12 LPA", "number_of_offers": 35},
    {"name": "Samsung", "eligibility_cgpa": 7.0, "branches_allowed": ["CSE", "IT", "ECE"], "rounds": "1 Global Coding Test, 2 Tech, 1 HR", "package_range": "14-22 LPA", "number_of_offers": 20},
    {"name": "Accenture", "eligibility_cgpa": 6.0, "branches_allowed": ["All Branches"], "rounds": "1 Cognitive+Technical, 1 Coding, 1 Communication, 1 Interview", "package_range": "4.5-12 LPA", "number_of_offers": 85}
]

companies = []
for c in companies_base:
    year = random.choice(years)
    month = random.randint(8, 11)
    day = random.randint(1, 28)
    c["visit_date"] = f"{year}-{month:02d}-{day:02d}"
    companies.append(c)

senior_first_names = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Neha", "Rohit", "Anjali", "Karan", "Pooja", "Arjun", "Kavya", "Varun", "Riya", "Aditya", "Shruti", "Siddharth", "Aisha", "Dev", "Tanya", "Akash", "Ishita", "Yash", "Tanvi", "Pranav", "Rashi", "Karthik", "Roshni", "Aman", "Megha"]
senior_last_names = ["Sharma", "Singh", "Patel", "Kumar", "Gupta", "Verma", "Reddy", "Nair", "Joshi", "Chawla", "Yadav", "Iyer", "Rao", "Das", "Menon", "Malhotra", "Mehta", "Bose", "Saxena", "Kapoor"]

# 30 unique tips to guarantee diversity in vector space
tips = [
    "Focus heavily on Dynamic Programming and Graphs. Do at least 200 medium level LeetCode questions.",
    "Communication is key. If you are stuck, think out loud. Interviewers care more about your approach than the final code.",
    "Make sure your resume doesn't have fake projects. They grilled me on every single technology I mentioned.",
    "System Design basics are crucial. Read 'Designing Data-Intensive Applications' or watch standard YouTube crash courses.",
    "Practice mock interviews with your friends. Answering behavioral questions smoothly using the STAR method makes a huge difference.",
    "Speed matters in the online assessment. Don't spend too much time optimizing early on; get a working brute force solution first.",
    "Brush up on core CS subjects: OS, DBMS, and Computer Networks. They asked me very specific SQL indexing questions.",
    "Stay calm during the Bar Raiser round. They will push you to your limits to see how you handle pressure and ambiguity.",
    "Don't ignore Object-Oriented Programming (OOP) concepts. I was asked to design a parking lot system from scratch.",
    "Maintain a good CGPA (above 8 ideally). It acts as a tie-breaker when many students solve the OA questions.",
    "Contribute to open source! Mentioning my merged PRs in popular repos completely drove the technical interview.",
    "For front-end roles, know JavaScript under the hood. Closures, event loop, and promises are guaranteed questions.",
    "Have a solid grasp of REST API principles. I was asked to architect an API for a chat application on the whiteboard.",
    "Always clarify the question before jumping into the code. Asking edge-case questions shows maturity.",
    "Know your database transactions. I had a 20-minute discussion just on ACID properties and isolation levels.",
    "If you mention AWS or Cloud on your resume, be ready to explain how load balancers and auto-scaling work.",
    "Don't just memorize LeetCode solutions. Understand the underlying patterns like sliding window and two pointers.",
    "Read up on the company's core values before the HR round. Align your personal stories with their mission statement.",
    "During the machine coding round, focus on modularity and clean code. Hardcoded values will lead to rejection.",
    "Be honest if you don't know an answer. Saying 'I don't know, but here is how I would approach it' is highly respected.",
    "Have 2-3 strong questions prepared for the interviewer at the end. It shows you are genuinely interested in the role.",
    "Master Git commands. Being able to explain branching strategies and merge conflict resolution impressed my interviewer.",
    "For product companies, think about edge cases in the user experience, not just the technical edge cases.",
    "If you're interviewing for a backend role, make sure you know the difference between monolithic and microservice architectures.",
    "Participate in competitive programming. The speed you gain there will make online assessments feel very easy.",
    "Keep your GitHub profile active and clean. Interviewers sometimes look at your code quality before the interview.",
    "Know how to test your own code. Writing unit tests during the interview sets you apart from 90% of candidates.",
    "Understand web security basics. Cross-Site Scripting (XSS) and SQL injection were major discussion points in my tech round.",
    "Don't neglect your soft skills. Being likable and easy to work with is just as important as your technical abilities.",
    "Finally, don't burn out. Take breaks during preparation. A fresh mind performs much better in interviews than an exhausted one."
]

questions = [
    "Reverse a linked list in groups of K, Word Ladder problem, SQL queries on Joins.",
    "Design a URL shortener, Find the median in a stream of integers, differences between TCP and UDP.",
    "Detect cycle in a directed graph, LRU Cache implementation, questions on React hooks.",
    "Merge K sorted lists, Binary Tree Maximum Path Sum, Explain ACID properties in DBMS.",
    "Find the longest palindromic substring, Implement a Trie, explain multithreading concepts in Java.",
    "Design an elevator system (LLD), Valid Parentheses, Page replacement algorithms in OS.",
    "Trapping Rain Water, Next Greater Element, normalization forms in databases.",
    "Alien Dictionary, Clone a graph, write an SQL query to find the second highest salary.",
    "Longest Increasing Subsequence, Edit Distance, explain the event loop in JavaScript.",
    "Two Sum, Best Time to Buy and Sell Stock, how does a hash map work internally."
]

roles = ["SDE-1", "Software Engineer", "Frontend Developer", "Backend Engineer", "Full Stack Developer", "Data Analyst", "Systems Engineer", "MTS", "Cloud Engineer", "Analyst"]
tech_stacks = ["MERN", "Java/Spring Boot", "Python/Django", "C++/SQL", "Go/Kubernetes", "React/Node.js", "Vue/Laravel", "Ruby on Rails", "Angular/Express", ".NET/Azure"]

seniors = []
for i in range(30):
    first_name = senior_first_names[i]
    last_name = random.choice(senior_last_names)
    company = random.choice(companies)
    
    senior = {
        "name": f"{first_name} {last_name}",
        "batch": str(random.choice(years)),
        "company": company["name"],
        "role": random.choice(roles),
        "selected": random.random() > 0.3,
        "rounds_detail": company["rounds"],
        "questions_asked": random.choice(questions),
        "tech_stack": random.choice(tech_stacks),
        "tips": tips[i],  # 30 unique tips assigned
        "consent": random.random() > 0.2,
        "linkedin_url": f"https://linkedin.com/in/{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}"
    }
    seniors.append(senior)

import os
target_dir = r"c:\Desktop\E2E\backend\data\sample"
os.makedirs(target_dir, exist_ok=True)

with open(os.path.join(target_dir, "sample_companies.json"), "w") as f:
    json.dump(companies, f, indent=4)
    
with open(os.path.join(target_dir, "sample_seniors.json"), "w") as f:
    json.dump(seniors, f, indent=4)

print("Mock data generated successfully with years 2023, 2024, and 2025!")
