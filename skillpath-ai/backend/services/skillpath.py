from .data_loader import projects_catalog

LEARNING_COURSES = {
    # Data & AI
    "SQL": {
        "action": "Master relational schema design, complex JOINs, aggregate window functions, and indexing.",
        "why": "SQL is the ubiquitous query standard across data analysis, backend engineering, and business intelligence.",
        "course": "Google Data Analytics Professional Certificate / Databases & SQL",
        "provider": "Coursera & Google",
        "degree_bridge": "Accredited verification of data query fluency, accepted by employers in lieu of a formal Computer Science degree."
    },
    "Python": {
        "action": "Write modular, object-oriented Python scripts with virtual environments and package managers.",
        "why": "Python is the primary language for machine learning, data engineering, and automation.",
        "course": "Python for Everybody Specialization (Univ. of Michigan)",
        "provider": "Coursera & edX",
        "degree_bridge": "Demonstrates computational literacy for candidates transitioning from arts, commerce, or non-technical majors."
    },
    "Machine Learning": {
        "action": "Study bias-variance tradeoffs, feature engineering, loss functions, and model validation.",
        "why": "Critical requirement for predicting outcomes, building intelligent services, and automating decisions.",
        "course": "Machine Learning Specialization by Andrew Ng",
        "provider": "DeepLearning.AI & Stanford Online",
        "degree_bridge": "Recognized industry gold-standard credential proving rigorous ML competency."
    },
    "Scikit-learn": {
        "action": "Implement clean train/test evaluation pipelines with cross-validation and hyperparameter tuning.",
        "why": "Translates mathematical machine learning concepts into production-grade Python implementations.",
        "course": "Supervised Machine Learning: Regression and Classification",
        "provider": "Coursera",
        "degree_bridge": "Validates hands-on coding ability over pure theory."
    },
    "Pandas": {
        "action": "Practice tabular ETL routines, handle missing values, reshape data, and perform vectorized math.",
        "why": "Over 80% of data science and analytics time is invested in data wrangling and preparation.",
        "course": "Applied Data Science with Python (Univ. of Michigan)",
        "provider": "Coursera",
        "degree_bridge": "Proves practical analytical capability across real-world business datasets."
    },
    "NumPy": {
        "action": "Practice N-dimensional array manipulations, broadcasting, and numerical matrix algebra.",
        "why": "Forms the high-performance backbone of modern scientific computing and deep learning in Python.",
        "course": "Introduction to Computational Thinking and Data Science",
        "provider": "MIT OpenCourseWare & edX",
        "degree_bridge": "Bridges mathematical and quantitative gaps for self-taught or non-engineering students."
    },
    "Statistics": {
        "action": "Review statistical hypothesis testing, p-values, confidence intervals, and probability distributions.",
        "why": "Prevents false discovery and validates statistical significance in product and business analytics.",
        "course": "Statistics and R Specialization (HarvardX)",
        "provider": "edX & Harvard",
        "degree_bridge": "Validates empirical scientific reasoning across all academic disciplines."
    },
    "Data Visualization": {
        "action": "Design clean executive dashboards that tell clear actionable stories with data.",
        "why": "Senior decision makers rely on visual clarity to approve strategic investments and product pivots.",
        "course": "Data Visualization with Tableau / Power BI Specialization",
        "provider": "Coursera & UC Davis",
        "degree_bridge": "Demonstrates executive business communication skills."
    },
    "Power BI": {
        "action": "Build interactive DAX measures, data models, and automated business KPI dashboards.",
        "why": "Power BI is the enterprise standard for corporate business intelligence across global multinationals.",
        "course": "Microsoft Power BI Data Analyst Professional Certificate (PL-300)",
        "provider": "Microsoft & Coursera",
        "degree_bridge": "Official vendor certification widely accepted for business and finance roles regardless of degree."
    },
    "Excel": {
        "action": "Master dynamic arrays, XLOOKUP, INDEX/MATCH, pivot tables, and financial sensitivity tables.",
        "why": "Excel remains the primary tool for financial analysis, corporate planning, and operational modeling.",
        "course": "Excel Skills for Business: Advanced (Macquarie University)",
        "provider": "Coursera",
        "degree_bridge": "Proves immediate workplace utility in any global business, banking, or corporate position."
    },

    # Finance & Commerce
    "Financial Modeling": {
        "action": "Construct integrated 3-statement financial models, forecast revenues, and model debt schedules.",
        "why": "Core requirement for corporate FP&A, investment banking, private equity, and equity research.",
        "course": "Financial Modeling & Valuation Analyst (FMVA) / Wharton Business Foundations",
        "provider": "CFI / Wharton Online (Coursera)",
        "degree_bridge": "Validates Wall Street & corporate finance readiness for students with any degree (B.Com, B.A., B.Tech)."
    },
    "Accounting": {
        "action": "Study double-entry bookkeeping, revenue recognition principles, and financial statement integrity.",
        "why": "Accounting is the language of business; every investment decision relies on clean books.",
        "course": "Introduction to Financial Accounting (Wharton School)",
        "provider": "Coursera",
        "degree_bridge": "Bridges formal commerce qualification requirements for non-finance graduates."
    },
    "Financial Statement Analysis": {
        "action": "Analyze balance sheets, income statements, and cash flows to evaluate solvency and profitability.",
        "why": "Essential for assessing company fiscal health, creditworthiness, and investment viability.",
        "course": "Financial Statement Analysis & Ratio Mastery",
        "provider": "edX & Columbia Business School",
        "degree_bridge": "Demonstrates rigorous fundamental equity and credit research capability."
    },
    "Valuation": {
        "action": "Perform Discounted Cash Flow (DCF), Comparable Company (Trading Comps), and Precedent Transaction models.",
        "why": "Required for mergers & acquisitions (M&A), capital budgeting, and corporate advisory.",
        "course": "Advanced Valuation and Strategy (Erasmus Univ.)",
        "provider": "Coursera",
        "degree_bridge": "Evidences sophisticated financial acumen for banking and consulting recruiting."
    },
    "DCF Modeling": {
        "action": "Forecast Free Cash Flows (FCFF/FCFE), calculate WACC, and perform terminal value sensitivity tests.",
        "why": "DCF is the cornerstone analytical framework for investment bankers and corporate controllers.",
        "course": "Discounted Cash Flow Modeling & Sensitivity Analysis",
        "provider": "Wall Street Prep / Udemy",
        "degree_bridge": "Demonstrates investment banking analyst readiness."
    },
    "Budgeting": {
        "action": "Formulate departmental operational expenditure (OpEx) and capital expenditure (CapEx) budget forecasts.",
        "why": "Organizations require proactive financial controllership to ensure sustainable burn rates.",
        "course": "Budgeting and Forecasting for Management",
        "provider": "LinkedIn Learning & edX",
        "degree_bridge": "Validates managerial and operational accounting capability."
    },
    "Taxation": {
        "action": "Study corporate tax schedules, deferred tax assets/liabilities, and statutory compliance regulations.",
        "why": "Crucial for financial auditing and risk mitigation across corporate enterprise transactions.",
        "course": "Corporate Tax Law & Compliance Principles",
        "provider": "Coursera",
        "degree_bridge": "Equips candidates with practical compliance know-how."
    },

    # Design & Creative
    "Figma": {
        "action": "Build scalable auto-layout components, interactive prototypes, design tokens, and style guides.",
        "why": "Figma is the world's standard product design and collaborative interface tool.",
        "course": "Google UX Design Professional Certificate / Figma Advanced Mastery",
        "provider": "Google & Coursera",
        "degree_bridge": "Recognized by tech recruiters worldwide as proof of design job-readiness without a formal B.Des degree."
    },
    "User Research": {
        "action": "Conduct qualitative user interviews, usability testing sessions, persona mapping, and journey maps.",
        "why": "Great products solve validated user problems rather than internal assumptions.",
        "course": "User Experience Research and Design Specialization (Univ. of Michigan)",
        "provider": "edX & Coursera",
        "degree_bridge": "Validates human-centered problem solving and research methodology across all backgrounds."
    },
    "Wireframing": {
        "action": "Draft low-fidelity and high-fidelity screen blueprints mapping user journeys and architectural hierarchies.",
        "why": "Establishes structural flow and information hierarchy before aesthetic polish.",
        "course": "Interaction Design Specialization (UC San Diego)",
        "provider": "Coursera",
        "degree_bridge": "Proves structured UI/UX product design thinking."
    },
    "Prototyping": {
        "action": "Build high-fidelity animated micro-interactions and transitions to test with real users.",
        "why": "Validates intuitive workflows and usability before expensive engineering development begins.",
        "course": "High-Fidelity Prototyping with Figma & Framer",
        "provider": "Interaction Design Foundation (IxDF)",
        "degree_bridge": "Provides tangible visual proof of product design execution."
    },
    "Design Systems": {
        "action": "Architect cohesive reusable UI component libraries with accessible typography and color palettes.",
        "why": "Ensures design consistency and rapid cross-functional development across multi-platform apps.",
        "course": "Design Systems for Enterprise Product Teams",
        "provider": "Interaction Design Foundation (IxDF)",
        "degree_bridge": "Signals senior design architecture maturity."
    },

    # Product & Strategy
    "Product Strategy": {
        "action": "Synthesize customer needs, competitive differentiation, and business models into roadmaps.",
        "why": "Product managers define the vision, goals, and measurable success metrics for cross-functional teams.",
        "course": "Digital Product Management: Modern Fundamentals (Univ. of Virginia)",
        "provider": "Coursera",
        "degree_bridge": "Validates strategic leadership and market empathy for career changers."
    },
    "Agile/Scrum": {
        "action": "Facilitate sprint planning, daily standups, backlog refinement, and sprint retrospectives.",
        "why": "Modern product organizations worldwide run on iterative Agile and Scrum frameworks.",
        "course": "Applied Scrum for Agile Project Management / PSM I Preparation",
        "provider": "edX (Univ. of Maryland) & Scrum.org",
        "degree_bridge": "Accredited Agile credentials (e.g. Scrum Master/Product Owner) open doors regardless of major."
    },
    "User Story Mapping": {
        "action": "Deconstruct complex feature epics into clear user stories with explicit acceptance criteria.",
        "why": "Ensures engineering teams build exactly what solves user pain points with zero ambiguity.",
        "course": "Product Ideation, Design, and Story Mapping",
        "provider": "Coursera",
        "degree_bridge": "Demonstrates clear cross-functional technical communication."
    },
    "Business Strategy": {
        "action": "Apply Porter's Five Forces, SWOT, value chain analysis, and unit economics to assess market positions.",
        "why": "Foundational requirement for management consultants and corporate strategy leaders.",
        "course": "Business Strategy Specialization (Univ. of Virginia / Darden)",
        "provider": "Coursera",
        "degree_bridge": "Provides strategic consulting frameworks universally accepted by advisory firms."
    },
    "Hypothesis-Driven Problem Solving": {
        "action": "Structure ambiguous business questions into MECE issue trees and test hypotheses using data.",
        "why": "The trademark analytical approach used by McKinsey, BCG, and Bain consultants.",
        "course": "Strategic Problem Solving & Frameworks",
        "provider": "edX & Harvard Online",
        "degree_bridge": "Demonstrates top-tier executive problem solving capability."
    },

    # Marketing & Communications
    "SEO": {
        "action": "Conduct technical site audits, keyword intent research, backlink analysis, and on-page optimization.",
        "why": "Drives sustainable high-intent organic user acquisition and brand discovery at zero ad cost.",
        "course": "Search Engine Optimization (SEO) Specialization (UC Davis)",
        "provider": "Coursera",
        "degree_bridge": "Signals revenue-generating growth skills across digital commerce."
    },
    "Google Analytics": {
        "action": "Set up GA4 event tracking, analyze user funnel drop-offs, and compute customer lifetime value (LTV).",
        "why": "Allows digital marketers to attribute conversions and optimize return on advertising spend.",
        "course": "Google Analytics 4 (GA4) Certification",
        "provider": "Google Skillshop (Official Free Certification)",
        "degree_bridge": "Recognized global credential validating digital measurement fluency."
    },
    "Content Strategy": {
        "action": "Plan multi-channel editorial calendars, buyer persona messaging, and brand authority narratives.",
        "why": "Builds authentic engagement, trust, and organic lead generation for enterprise and consumer brands.",
        "course": "Content Strategy for Professionals Specialization (Northwestern Univ.)",
        "provider": "Coursera",
        "degree_bridge": "Demonstrates professional communications and marketing leadership."
    },

    # Human Resources & Operations
    "Talent Acquisition": {
        "action": "Source passive talent, structure behavioral interview scorecards, and negotiate offers.",
        "why": "Building world-class teams is the primary competitive advantage for modern organizations.",
        "course": "Recruiting, Onboarding, and Sourcing Strategies",
        "provider": "LinkedIn Learning & Coursera",
        "degree_bridge": "Demonstrates immediate recruiter and human capital capability."
    },
    "HRIS": {
        "action": "Manage employee lifecycle records, benefits workflows, and compliance audits in modern HR systems.",
        "why": "Streamlines organizational operations and protects company compliance records.",
        "course": "Human Resource Management Specialization (Univ. of Minnesota)",
        "provider": "Coursera",
        "degree_bridge": "Signals digital HR systems operational readiness."
    },
    "Inventory Optimization": {
        "action": "Compute economic order quantities (EOQ), reorder points, and safety stock buffers.",
        "why": "Reduces carrying costs and prevents costly stockouts across global supply networks.",
        "course": "Supply Chain Management Specialization (Rutgers University)",
        "provider": "Coursera & MITx",
        "degree_bridge": "Proves quantitative logistics and operations engineering fluency."
    },

    # Cloud & Tech Foundations
    "AWS": {
        "action": "Deploy secure VPC architectures, serverless Lambda functions, and RDS databases on AWS.",
        "why": "AWS powers over a third of global cloud infrastructure.",
        "course": "AWS Certified Cloud Practitioner / Solutions Architect Associate",
        "provider": "AWS Training & Certification / Coursera",
        "degree_bridge": "Industry-accredited cloud certification validating practical enterprise IT fluency."
    },
    "Git": {
        "action": "Manage collaborative Git feature branching, interactive rebasing, and GitHub PR reviews.",
        "why": "The universal version control system used by all software and data teams globally.",
        "course": "Version Control with Git and GitHub (Meta / Coursera)",
        "provider": "Meta & Coursera",
        "degree_bridge": "Proves collaborative developer workflow capability."
    },
    "Data Structures": {
        "action": "Implement arrays, linked lists, trees, hash tables, and graphs with space/time complexity analysis.",
        "why": "Foundational bedrock for writing performant software and passing technical engineering interviews.",
        "course": "CS50: Introduction to Computer Science (Harvard University)",
        "provider": "edX & Harvard Online",
        "degree_bridge": "Harvard's premier CS course; globally respected proof of core software foundations."
    },
    "Algorithms": {
        "action": "Practice recursion, dynamic programming, sorting, and graph traversal algorithms.",
        "why": "Essential for solving complex algorithmic bottlenecks in modern software engineering.",
        "course": "Algorithms, Part I & II (Princeton University)",
        "provider": "Coursera",
        "degree_bridge": "Validates rigorous computational problem-solving capability."
    },
    "React": {
        "action": "Build component state architectures with hooks, memoization, TypeScript, and clean CSS styling.",
        "why": "The dominant frontend library powering modern web applications globally.",
        "course": "Meta Front-End Developer Professional Certificate",
        "provider": "Meta & Coursera",
        "degree_bridge": "Industry certification verifying job-ready web application development."
    },
    "HTML": {
        "action": "Write semantic, accessible HTML5 elements with clean DOM structures and ARIA landmarks.",
        "why": "The structural foundation of every web experience and document.",
        "course": "Responsive Web Design Certification",
        "provider": "freeCodeCamp",
        "degree_bridge": "Proves fundamental web architecture fluency."
    },
    "JavaScript": {
        "action": "Master asynchronous JavaScript (Promises, async/await), ES6+ modules, and DOM APIs.",
        "why": "The universal programming language of the interactive modern web.",
        "course": "JavaScript Algorithms and Data Structures",
        "provider": "freeCodeCamp & edX",
        "degree_bridge": "Demonstrates client-side programming fluency."
    }
}

def generate_skillpath(skill_gap: dict, matched_opportunities: list[dict] | None = None) -> dict:
    missing = skill_gap.get("missing", [])
    developing = skill_gap.get("developing", [])
    
    # Prioritize skills that unlock the most matched opportunities
    shared = {}
    for opp in (matched_opportunities or []):
        for s in opp.get("missing_skills", []):
            shared[s] = shared.get(s, 0) + 1
            
    ordered = sorted(missing, key=lambda s: (-shared.get(s, 0), s)) + sorted(developing, key=lambda s: (-shared.get(s, 0), s))
    actions = []
    seen = set()
    
    for skill in ordered:
        if skill in seen:
            continue
        seen.add(skill)
        
        # Look up detailed learning recommendations or synthesize intelligent default
        info = LEARNING_COURSES.get(skill)
        if not info:
            # Fallback search by case-insensitive key
            for k, v in LEARNING_COURSES.items():
                if _norm(k) == _norm(skill):
                    info = v
                    break
                    
        if info:
            actions.append({
                "title": f"Master {skill}",
                "skill": skill,
                "action": info["action"],
                "why": info["why"],
                "course": info["course"],
                "provider": info["provider"],
                "degree_bridge": info["degree_bridge"],
                "priority": "High" if skill in missing else "Medium"
            })
        else:
            actions.append({
                "title": f"Build {skill} Competency",
                "skill": skill,
                "action": f"Complete a hands-on project and accredited certified course in {skill}.",
                "why": f"{skill} is a critical requirement across your target career role.",
                "course": f"{skill} Foundations & Practical Application",
                "provider": "Coursera / edX / LinkedIn Learning",
                "degree_bridge": f"Validates verified skill equivalency in {skill} to bridge formal degree requirements.",
                "priority": "High" if skill in missing else "Medium"
            })
            
        if len(actions) >= 5:
            break
            
    if skill_gap.get("missing") or skill_gap.get("developing"):
        catalog = projects_catalog()
        gaps = {_norm(s) for s in missing + developing}
        ranked = sorted(catalog, key=lambda p: sum(_norm(s) in gaps for s in p.get("skills", [])), reverse=True)
        if ranked and sum(_norm(s) in gaps for s in ranked[0].get("skills", [])):
            actions.append({
                "title": ranked[0]["title"],
                "skill": "Portfolio Project",
                "action": "Build a documented end-to-end project and publish the code with a comprehensive README.",
                "why": ranked[0]["reason"],
                "course": "Project-Based Applied Learning",
                "provider": "GitHub & Portfolio Evidence",
                "degree_bridge": "Tangible real-world project deliverables serve as the strongest substitute for a specialized academic degree.",
                "priority": "High"
            })
            
    if not actions:
        actions.append({
            "title": "Strengthen Portfolio Evidence",
            "skill": "Portfolio",
            "action": "Document a full case-study project with methodology, quantifiable results, and architecture.",
            "why": "Tangible proof of applied skills helps recruiters and managers assess your job readiness.",
            "course": "Career Portfolio Architecture",
            "provider": "Industry Best Practice",
            "degree_bridge": "Public portfolio evidence bridges traditional degree boundaries across all industries.",
            "priority": "Medium"
        })
        
    return {
        "actions": actions,
        "next_best_action": actions[0]["title"],
        "method": "Opportunity-weighted skill prioritization with accredited course and degree-bridge mappings."
    }

def _norm(x):
    return " ".join(str(x).lower().replace("-", " ").split())
