import React, { useEffect, useMemo, useState } from 'react'
import {
  Activity,
  ArrowRight,
  Award,
  BrainCircuit,
  BriefcaseBusiness,
  Building,
  Calendar,
  Check,
  CheckCircle2,
  ChevronRight,
  CircleAlert,
  Download,
  Edit3,
  ExternalLink,
  Eye,
  FileText,
  Filter,
  FolderGit2,
  GraduationCap,
  LayoutDashboard,
  LoaderCircle,
  Plus,
  RefreshCw,
  Search,
  Share2,
  ShieldCheck,
  Sparkles,
  Target,
  Trash2,
  Upload,
  Waypoints,
  X,
  Zap
} from 'lucide-react'
import { api } from './api'
import type { Analysis, Profile } from './types'

// Richly articulated demo profile with full punctuation marks and realistic academic accomplishments
const demoProfile: Profile = {
  name: 'Prajwal S. Kumar',
  education: 'Bachelor of Technology (B.Tech.) in Computer Science & Engineering',
  branch: 'Artificial Intelligence & Machine Learning (AI & ML)',
  semester: '7th Semester (Final Year)',
  target_career: 'Machine Learning Intern',
  skills: [
    'Python',
    'NumPy',
    'Pandas',
    'Scikit-learn',
    'SQL (PostgreSQL)',
    'Git & GitHub',
    'FastAPI',
    'REST APIs',
    'Data Visualization',
    'HTML5 & CSS3'
  ],
  projects: [
    'Predictive Healthcare Risk Classifier: Architected an end-to-end Machine Learning pipeline utilizing Python, NumPy, Pandas, and Scikit-learn; achieved 92.4% ROC-AUC on standardized patient records. Integrated a lightweight FastAPI endpoint for real-time risk predictions.',
    'Automated Resume Skill Extraction Engine: Developed a high-precision document parsing tool for PDF and DOCX formats using Python regular expressions and dictionary normalization; processed 200+ academic profiles with 94% entity recognition accuracy.',
    'Cohort Analytics & Performance Dashboard: Designed a responsive interactive data visualization portal with React, Tailwind CSS, and Chart.js; enabled educators to filter and track semester-wise student benchmarks.'
  ],
  experience: [
    'Undergraduate Machine Learning Research Intern at Center for AI Studies (Jan 2024 – May 2024): Preprocessed and normalized 250,000+ tabular records using Pandas and SQL; engineered automated validation routines and co-authored technical benchmark documentation.',
    'Open-Source Contributor & Peer Technical Lead at Campus Developer Club (Aug 2023 – Dec 2023): Reviewed 60+ pull requests via Git & GitHub; mentored 45 junior students on Python data structures, algorithms, and modular software design principles.'
  ],
  certifications: [
    'Machine Learning Specialization — DeepLearning.AI & Stanford Online (Issued via Coursera, 2024)',
    'SQL for Data Analytics & Database Design — DataCamp Verified Credential (ID: DC-829104, 2023)',
    'AWS Certified Cloud Practitioner — Amazon Web Services (Validation ID: AWS-941820, 2024)'
  ],
  resume_text: `Prajwal S. Kumar | Senior Undergraduate, B.Tech. in Computer Science & Engineering (AI & Data Science), 7th Semester.

Professional Summary:
Driven aspiring Machine Learning Engineer with hands-on proficiency in Python, Scikit-learn, Pandas, NumPy, SQL, and Git. Passionate about applying predictive modeling and clean API design to solve complex domain problems.

Technical Skills:
Python, Machine Learning, Scikit-learn, NumPy, Pandas, SQL, PostgreSQL, Git, FastAPI, REST APIs, HTML, CSS, Data Visualization, Statistics.

Projects:
• Predictive Healthcare Risk Classifier: Built an end-to-end classification pipeline in Python using Pandas, NumPy, and Scikit-learn; achieved 92.4% ROC-AUC on patient risk stratification. Integrated an interactive FastAPI endpoint for real-time inference.
• Automated Resume Skill Extraction Engine: Designed a text parsing and alias-matching pipeline for PDF and DOCX files with Python and regex; validated against 150+ sample candidate records.
• Cohort Analytics & Performance Dashboard: Engineered a React and Tailwind CSS data portal with responsive charts and filters to monitor cohort learning metrics.

Work Experience:
• Undergraduate Machine Learning Research Intern at Center for AI Studies (Jan 2024 – May 2024): Collaborated on data preprocessing workflows for 250,000+ tabular records using Pandas and SQL; authored weekly technical benchmarks and documentation.
• Open-Source Contributor & Peer Technical Lead at Campus Developer Club (Aug 2023 – Dec 2023): Maintained Git repositories, reviewed pull requests, and assisted 40+ junior peers with Python data structures and algorithm fundamentals.

Certifications:
• Deep Learning & Machine Learning Specialization — Coursera & DeepLearning.AI (2024)
• SQL for Data Analytics and Relational Database Design — DataCamp (2023)
• AWS Certified Cloud Practitioner — Amazon Web Services (2024)`,
  proficiency: {
    Python: 5,
    NumPy: 4,
    Pandas: 4,
    'Scikit-learn': 4,
    'Machine Learning': 4,
    Git: 4,
    SQL: 4,
    FastAPI: 3
  }
}

// Recommended skills lookup for quick one-click additions
const recommendedSkillsByCareer: Record<string, string[]> = {
  'ml-intern': ['Python', 'SQL', 'Scikit-learn', 'Pandas', 'NumPy', 'Machine Learning', 'Git', 'FastAPI', 'Docker', 'PyTorch'],
  'data-analyst': ['SQL', 'Python', 'Pandas', 'Excel', 'Data Visualization', 'Power BI', 'Statistics', 'Tableau'],
  'data-scientist': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'NumPy', 'Data Visualization', 'Deep Learning'],
  'python-dev': ['Python', 'FastAPI', 'REST APIs', 'Git', 'SQL', 'Docker', 'Testing', 'Debugging'],
  'ai-engineer': ['Python', 'PyTorch', 'Deep Learning', 'Machine Learning', 'REST APIs', 'Git', 'NumPy', 'Hugging Face'],
  'web-dev': ['JavaScript', 'React', 'HTML', 'CSS', 'REST APIs', 'Git', 'TypeScript', 'Tailwind CSS'],
  'software-dev': ['Python', 'Data Structures', 'Algorithms', 'Git', 'SQL', 'Testing', 'System Design']
}

export default function App() {
  const [profile, setProfile] = useState<Profile>(demoProfile)
  const [careers, setCareers] = useState<{ id: string; name: string }[]>([])
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [resumeText, setResumeText] = useState(demoProfile.resume_text)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [active, setActive] = useState('Overview')
  const [profileTab, setProfileTab] = useState<'basics' | 'skills' | 'projects' | 'experience' | 'certifications'>('skills')

  // Resume Parsing details
  const [resumeInfo, setResumeInfo] = useState<{
    skills: string[]
    confidence: number
    method: string
    projects?: string[]
    experience?: string[]
  } | null>(null)

  // Modals & Popovers
  const [selectedOpp, setSelectedOpp] = useState<string | null>(null)
  const [oppFilter, setOppFilter] = useState<'ALL' | 'APPLY NOW' | 'PREPARE & APPLY' | 'NOT YET'>('ALL')
  const [oppSearch, setOppSearch] = useState('')
  const [showReportModal, setShowReportModal] = useState(false)
  const [skillInput, setSkillInput] = useState('')
  const [skillSearch, setSkillSearch] = useState('')
  const [completedActions, setCompletedActions] = useState<Record<string, boolean>>({})

  // Item form states
  const [newProject, setNewProject] = useState({ title: '', techStack: '', link: '', description: '' })
  const [newExperience, setNewExperience] = useState({ role: '', company: '', duration: '', description: '' })
  const [newCert, setNewCert] = useState({ name: '', issuer: '', yearOrId: '', link: '' })
  const [showAddProject, setShowAddProject] = useState(false)
  const [showAddExp, setShowAddExp] = useState(false)
  const [showAddCert, setShowAddCert] = useState(false)

  // Fetch career list and compute initial live analysis on start
  useEffect(() => {
    api.careers()
      .then(careersList => {
        setCareers(careersList)
        api.analyze(demoProfile)
          .then(setAnalysis)
          .catch(() => {})
      })
      .catch(e => setError(e.message))
  }, [])

  const updateProfile = (key: keyof Profile, value: any) => {
    setProfile(p => ({ ...p, [key]: value }))
  }

  // Profile completeness calculation
  const profileCompleteness = useMemo(() => {
    let score = 0
    if (profile.name.trim()) score += 10
    if (profile.education.trim()) score += 10
    if (profile.branch.trim()) score += 10
    if (profile.target_career.trim()) score += 15
    if (profile.skills.length >= 3) score += 20
    if (profile.projects.length >= 1) score += 15
    if (profile.experience.length >= 1) score += 10
    if (profile.certifications.length >= 1) score += 10
    return Math.min(100, score)
  }, [profile])

  // Run backend career analysis
  const runAnalysis = async () => {
    setBusy(true)
    setError('')
    setNotice('')
    try {
      const clean = { ...profile, resume_text: resumeText }
      await api.saveProfile(clean)
      const result = await api.analyze(clean)
      setAnalysis(result)
      setProfile(clean)
      setActive('Overview')
      setNotice(`Analysis successfully updated for ${clean.target_career}! Review your score and recommendations.`)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Analysis failed to complete.')
    } finally {
      setBusy(false)
    }
  }

  // Resume analysis
  const doResumeAnalysis = async (file?: File) => {
    setBusy(true)
    setError('')
    setNotice('')
    try {
      const result = file ? await api.analyzeResumeFile(file) : await api.analyzeResume(resumeText)
      setResumeInfo({
        skills: result.skills,
        confidence: result.confidence,
        method: result.method,
        projects: result.projects,
        experience: result.experience
      })
      // Sync discovered items into current profile
      const mergedSkills = Array.from(new Set([...profile.skills, ...result.skills]))
      const mergedProjects = result.projects?.length
        ? Array.from(new Set([...profile.projects, ...result.projects]))
        : profile.projects

      setProfile(p => ({
        ...p,
        skills: mergedSkills,
        projects: mergedProjects,
        ...(result.education.qualification ? { education: result.education.qualification } : {})
      }))
      setNotice(`Resume analyzed with ${Math.round(result.confidence * 100)}% confidence! Detected ${result.skills.length} skills.`)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Resume analysis failed.')
    } finally {
      setBusy(false)
    }
  }

  // Load clean demo profile
  const loadDemo = () => {
    setProfile(demoProfile)
    setResumeText(demoProfile.resume_text)
    setAnalysis(null)
    setResumeInfo(null)
    setError('')
    setNotice('Demo profile loaded. Click "Analyze career" to compute your live readiness score and matches.')
  }

  // Quick Skill Helpers
  const addSkill = (skill: string) => {
    const trimmed = skill.trim()
    if (!trimmed) return
    if (!profile.skills.some(s => s.toLowerCase() === trimmed.toLowerCase())) {
      setProfile(p => ({ ...p, skills: [...p.skills, trimmed] }))
    }
    setSkillInput('')
  }

  const removeSkill = (skillToRemove: string) => {
    setProfile(p => ({
      ...p,
      skills: p.skills.filter(s => s !== skillToRemove)
    }))
  }

  // Project item handlers
  const handleAddProject = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newProject.title.trim()) return
    const formatted = `${newProject.title.trim()}${
      newProject.techStack.trim() ? ` [${newProject.techStack.trim()}]` : ''
    }: ${newProject.description.trim()}${
      newProject.link.trim() ? ` (Link: ${newProject.link.trim()})` : ''
    }`
    setProfile(p => ({ ...p, projects: [...p.projects, formatted] }))
    setNewProject({ title: '', techStack: '', link: '', description: '' })
    setShowAddProject(false)
  }

  const removeProject = (index: number) => {
    setProfile(p => ({
      ...p,
      projects: p.projects.filter((_, i) => i !== index)
    }))
  }

  // Experience item handlers
  const handleAddExperience = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newExperience.role.trim()) return
    const formatted = `${newExperience.role.trim()} at ${newExperience.company.trim() || 'Organization'} (${
      newExperience.duration.trim() || 'Recent'
    }): ${newExperience.description.trim()}`
    setProfile(p => ({ ...p, experience: [...p.experience, formatted] }))
    setNewExperience({ role: '', company: '', duration: '', description: '' })
    setShowAddExp(false)
  }

  const removeExperience = (index: number) => {
    setProfile(p => ({
      ...p,
      experience: p.experience.filter((_, i) => i !== index)
    }))
  }

  // Certification item handlers
  const handleAddCert = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newCert.name.trim()) return
    const formatted = `${newCert.name.trim()} — ${newCert.issuer.trim() || 'Issuer'}${
      newCert.yearOrId.trim() ? ` (${newCert.yearOrId.trim()})` : ''
    }${newCert.link.trim() ? ` [${newCert.link.trim()}]` : ''}`
    setProfile(p => ({ ...p, certifications: [...p.certifications, formatted] }))
    setNewCert({ name: '', issuer: '', yearOrId: '', link: '' })
    setShowAddCert(false)
  }

  const removeCert = (index: number) => {
    setProfile(p => ({
      ...p,
      certifications: p.certifications.filter((_, i) => i !== index)
    }))
  }

  // Filtered opportunities
  const filteredOpportunities = useMemo(() => {
    if (!analysis) return []
    return analysis.opportunities.filter(opp => {
      const matchesFilter = oppFilter === 'ALL' || opp.classification === oppFilter
      const query = oppSearch.toLowerCase().trim()
      const matchesSearch =
        !query ||
        opp.role.toLowerCase().includes(query) ||
        opp.company.toLowerCase().includes(query) ||
        opp.matched_skills.some(s => s.toLowerCase().includes(query)) ||
        opp.missing_skills.some(s => s.toLowerCase().includes(query))
      return matchesFilter && matchesSearch
    })
  }, [analysis, oppFilter, oppSearch])

  // Suggested skills for current career
  const currentCareerId = useMemo(() => {
    const found = careers.find(c => c.name.toLowerCase() === profile.target_career.toLowerCase())
    return found ? found.id : 'ml-intern'
  }, [careers, profile.target_career])

  const suggestedSkills = useMemo(() => {
    const list = recommendedSkillsByCareer[currentCareerId] || recommendedSkillsByCareer['ml-intern']
    return list.filter(s => !profile.skills.some(userSkill => userSkill.toLowerCase() === s.toLowerCase()))
  }, [currentCareerId, profile.skills])

  const score = analysis?.readiness.overall_score ?? 0

  const pageTitle = useMemo(
    () =>
      ({
        Overview: 'Executive Overview',
        Profile: 'Profile & Skills Architecture',
        Resume: 'Intelligent Resume Parser',
        SkillPath: 'SkillPath Action Roadmap',
        Opportunities: 'Opportunity Matching Intelligence'
      }[active] || active),
    [active]
  )

  return (
    <div className="app-shell">
      {/* Sleek Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Waypoints size={22} strokeWidth={2.4} />
          </div>
          <div className="brand-text">
            <strong>
              SkillPath<span> AI</span>
            </strong>
            <small>CAREER INTELLIGENCE</small>
          </div>
        </div>

        <div className="workspace-label">ENTERPRISE PLATFORM</div>
        <nav>
          {[
            ['Overview', LayoutDashboard],
            ['Profile', GraduationCap],
            ['Resume', FileText],
            ['SkillPath', BrainCircuit],
            ['Opportunities', BriefcaseBusiness]
          ].map(([label, Icon]) => (
            <button
              key={label as string}
              className={`nav-item ${active === label ? 'active' : ''}`}
              onClick={() => setActive(label as string)}
            >
              <Icon size={18} strokeWidth={active === label ? 2.2 : 1.8} />
              <span>{label as string}</span>
              {active === label && <ChevronRight size={15} className="nav-chevron" />}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sdg-mark">8</div>
          <div>
            <strong>Decent Work & Growth</strong>
            <small>UN SDG 8 · Academic MVP</small>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main">
        {/* Sticky Topbar */}
        <header className="topbar">
          <div className="breadcrumb">
            SkillPath AI <span>/</span> <strong>{pageTitle}</strong>
          </div>
          <div className="top-actions">
            <div className="live-pill">
              <span className="live-dot" />
              <span>FastAPI Connected</span>
            </div>

            <button
              className="btn btn-secondary btn-sm"
              title="View full report"
              onClick={() => setShowReportModal(true)}
            >
              <Download size={14} /> Export Report
            </button>

            <button
              className="btn btn-secondary btn-sm"
              title="Reset with clean demo data"
              onClick={loadDemo}
            >
              <RefreshCw size={14} /> Load Demo
            </button>

            <div className="avatar" title={profile.name || 'Student'}>
              {(profile.name || 'P').slice(0, 1).toUpperCase()}
            </div>
          </div>
        </header>

        {/* Dynamic Page Views */}
        <div className="content">
          {/* Header Banner */}
          <section className="welcome-row">
            <div>
              <div className="eyebrow">
                <Sparkles size={14} /> CAREER READINESS & BENCHMARKING
              </div>
              <h1>
                {active === 'Overview' && 'Career Readiness & Strategic Blueprint.'}
                {active === 'Profile' && 'Comprehensive Student Profile & Portfolio.'}
                {active === 'Resume' && 'AI-Powered Resume Analysis & Extraction.'}
                {active === 'SkillPath' && 'Personalized Learning & Project Roadmap.'}
                {active === 'Opportunities' && 'Curated Opportunities & Readiness Matches.'}
              </h1>
              <p className="subhead">
                {active === 'Overview' &&
                  `Real-time weighted skill gap assessment and transparent opportunity scoring for ${
                    profile.target_career || 'your chosen career'
                  }.`}
                {active === 'Profile' &&
                  'Document your complete technical skills, hands-on projects, work experience, and verified credentials.'}
                {active === 'Resume' &&
                  'Extract verified skills and academic credentials with high precision from text, PDF, or DOCX files.'}
                {active === 'SkillPath' &&
                  'Targeted high-priority actions and concrete project blueprints designed to close critical gaps.'}
                {active === 'Opportunities' &&
                  'Rule-based evaluation matching your profile against illustrative local industry internship profiles.'}
              </p>
            </div>

            <div className="header-cta-group">
              <button className="btn btn-secondary" onClick={loadDemo}>
                Load Demo Profile
              </button>
              <button
                className="btn btn-accent"
                disabled={busy}
                onClick={runAnalysis}
              >
                {busy ? <LoaderCircle className="spin" size={16} /> : <Zap size={16} />}
                Run Live Analysis
              </button>
            </div>
          </section>

          {/* Feedback Alerts */}
          {error && (
            <div className="alert error">
              <CircleAlert size={18} />
              <span>{error}</span>
              <button onClick={() => setError('')}>Dismiss</button>
            </div>
          )}
          {notice && (
            <div className="alert success">
              <CheckCircle2 size={18} />
              <span>{notice}</span>
              <button onClick={() => setNotice('')}>Dismiss</button>
            </div>
          )}

          {/* ======================================================== */}
          {/* PAGE 1: OVERVIEW DASHBOARD */}
          {/* ======================================================== */}
          {active === 'Overview' && (
            <>
              {/* Hero Readiness Panel */}
              <div className="hero-grid">
                <div className="score-panel">
                  <div className="score-panel-bg-glow" />
                  <div className="score-header">
                    <div>
                      <span className="score-badge">
                        <ShieldCheck size={13} /> TRANSPARENT READINESS SCORE
                      </span>
                      <h2 style={{ fontSize: 22, margin: '10px 0 0', fontWeight: 800 }}>
                        {analysis ? analysis.readiness.classification : 'Benchmark Pending'}
                      </h2>
                    </div>
                  </div>

                  <div className="score-main-row">
                    <div className="score-display-number">
                      {analysis ? score : '—'}
                      <span>/ 100</span>
                    </div>

                    <div className="score-ring-svg">
                      <svg width="96" height="96" viewBox="0 0 100 100">
                        <circle
                          cx="50"
                          cy="50"
                          r="42"
                          stroke="rgba(255, 255, 255, 0.15)"
                          strokeWidth="8"
                          fill="none"
                        />
                        <circle
                          cx="50"
                          cy="50"
                          r="42"
                          stroke={score >= 75 ? '#34d399' : score >= 50 ? '#fbbf24' : '#f87171'}
                          strokeWidth="8"
                          fill="none"
                          strokeDasharray="263.89"
                          strokeDashoffset={263.89 - (263.89 * score) / 100}
                          strokeLinecap="round"
                          transform="rotate(-90 50 50)"
                          style={{ transition: 'stroke-dashoffset 0.8s ease' }}
                        />
                      </svg>
                      <div className="score-circle-inner">
                        <strong>{analysis ? `${score}%` : '0%'}</strong>
                        <small>{analysis ? 'Indexed' : 'Pending'}</small>
                      </div>
                    </div>
                  </div>

                  <p className="note">
                    {analysis
                      ? analysis.readiness.note
                      : 'Complete your profile credentials and trigger career analysis to calculate your readiness score.'}
                  </p>

                  <div style={{ marginTop: 'auto', position: 'relative', zIndex: 2 }}>
                    <button
                      className="btn btn-accent"
                      onClick={() => (analysis ? setActive('SkillPath') : setActive('Profile'))}
                    >
                      {analysis ? 'Explore Custom SkillPath' : 'Complete Profile First'}{' '}
                      <ArrowRight size={15} />
                    </button>
                  </div>
                </div>

                {/* Target Career Blueprint */}
                <div className="target-panel">
                  <div className="panel-heading" style={{ marginBottom: 12 }}>
                    <div>
                      <span className="eyebrow" style={{ color: '#059669', marginBottom: 4 }}>
                        TARGET ROLE SPECIFICATION
                      </span>
                      <h2>{profile.target_career}</h2>
                    </div>
                    <div className="target-icon">
                      <BriefcaseBusiness size={22} />
                    </div>
                  </div>
                  <p className="desc">
                    Comprehensive skill expectations evaluated against your academic degree, verified
                    coursework, portfolio projects, and technical proficiencies.
                  </p>

                  <div className="target-stats">
                    <div>
                      <strong>{analysis?.target_career.required_skills.length ?? '—'}</strong>
                      <span>Mandatory Skills</span>
                    </div>
                    <div>
                      <strong style={{ color: '#059669' }}>
                        {analysis?.skill_gap.strong.length ?? '—'}
                      </strong>
                      <span>Strong Matches</span>
                    </div>
                    <div>
                      <strong style={{ color: '#e11d48' }}>
                        {analysis?.skill_gap.missing.length ?? '—'}
                      </strong>
                      <span>Gaps to Bridge</span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: 10, marginTop: 'auto' }}>
                    <button className="btn btn-secondary btn-sm" onClick={() => setActive('Profile')}>
                      Modify Target Role <ArrowRight size={14} />
                    </button>
                  </div>
                </div>
              </div>

              {/* 5 Scoring Pillars */}
              {analysis && (
                <>
                  <div className="panel-heading" style={{ marginBottom: 16 }}>
                    <div>
                      <h2>
                        <Activity size={18} style={{ color: '#10b981' }} />
                        Weighted Readiness Dimension Breakdown
                      </h2>
                      <p>
                        Transparent academic weighting methodology: Technical (30%), Projects (20%),
                        Industry Alignment (20%), Internship (15%), Portfolio Strength (15%).
                      </p>
                    </div>
                  </div>

                  <div className="pillars-grid">
                    {[
                      {
                        title: 'Technical Skills',
                        weight: '30%',
                        score: analysis.readiness.technical_skills
                      },
                      {
                        title: 'Project Evidence',
                        weight: '20%',
                        score: analysis.readiness.project_experience
                      },
                      {
                        title: 'Industry Alignment',
                        weight: '20%',
                        score: analysis.readiness.industry_alignment
                      },
                      {
                        title: 'Internship Fit',
                        weight: '15%',
                        score: analysis.readiness.internship_readiness
                      },
                      {
                        title: 'Portfolio Breadth',
                        weight: '15%',
                        score: analysis.readiness.portfolio_strength
                      }
                    ].map(p => (
                      <div className="pillar-card" key={p.title}>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                          <strong>{p.title}</strong>
                          <small>{p.weight}</small>
                        </div>
                        <div className="pillar-score-row">
                          <span className="score">{p.score}</span>
                          <span style={{ fontSize: 11, color: '#64748b' }}>/ 100</span>
                        </div>
                        <div className="pillar-track">
                          <div className="pillar-fill" style={{ width: `${p.score}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}

              {/* Skill Gap Matrix */}
              <div className="panel-heading" style={{ marginTop: 24, marginBottom: 16 }}>
                <div>
                  <h2>
                    <BrainCircuit size={18} style={{ color: '#6366f1' }} />
                    Skill Gap Matrix Snapshot
                  </h2>
                  <p>
                    Categorized comparison between your current proficiencies and career requirements.
                  </p>
                </div>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => (analysis ? setActive('SkillPath') : runAnalysis())}
                >
                  {analysis ? 'View Full Action Plan' : 'Run Live Analysis'} <ArrowRight size={14} />
                </button>
              </div>

              <div className="three-grid">
                <div className="skill-card green">
                  <div className="skill-card-top">
                    <div>
                      <h3 style={{ color: '#065f46' }}>Strong & Verified</h3>
                      <p>Full match with career requirements</p>
                    </div>
                    <span className="skill-count-bubble">
                      {analysis?.skill_gap.strong.length ?? 0}
                    </span>
                  </div>
                  <div className="skill-items">
                    {(analysis?.skill_gap.strong || []).length > 0 ? (
                      analysis!.skill_gap.strong.map(s => (
                        <span className="skill-pill-tag" key={s}>
                          <CheckCircle2 size={13} /> {s}
                        </span>
                      ))
                    ) : (
                      <p style={{ fontSize: 12, color: '#94a3b8' }}>
                        Run analysis to identify verified matches.
                      </p>
                    )}
                  </div>
                </div>

                <div className="skill-card amber">
                  <div className="skill-card-top">
                    <div>
                      <h3 style={{ color: '#92400e' }}>Developing & Adjacent</h3>
                      <p>Related or partially demonstrated skills</p>
                    </div>
                    <span className="skill-count-bubble">
                      {analysis?.skill_gap.developing.length ?? 0}
                    </span>
                  </div>
                  <div className="skill-items">
                    {(analysis?.skill_gap.developing || []).length > 0 ? (
                      analysis!.skill_gap.developing.map(s => (
                        <span className="skill-pill-tag" key={s}>
                          <Activity size={13} /> {s}
                        </span>
                      ))
                    ) : (
                      <p style={{ fontSize: 12, color: '#94a3b8' }}>
                        Run analysis to see developing capabilities.
                      </p>
                    )}
                  </div>
                </div>

                <div className="skill-card rose">
                  <div className="skill-card-top">
                    <div>
                      <h3 style={{ color: '#9f1239' }}>Missing Gaps</h3>
                      <p>Critical skills requiring targeted learning</p>
                    </div>
                    <span className="skill-count-bubble">
                      {analysis?.skill_gap.missing.length ?? 0}
                    </span>
                  </div>
                  <div className="skill-items">
                    {(analysis?.skill_gap.missing || []).length > 0 ? (
                      analysis!.skill_gap.missing.map(s => (
                        <span className="skill-pill-tag" key={s}>
                          <CircleAlert size={13} /> {s}
                        </span>
                      ))
                    ) : (
                      <p style={{ fontSize: 12, color: '#94a3b8' }}>
                        Run analysis to reveal learning priorities.
                      </p>
                    )}
                  </div>
                </div>
              </div>

              {/* Lower Grid: Next Best Action & Opportunities Outlook */}
              <div className="lower-grid">
                <section className="panel" style={{ margin: 0 }}>
                  <div className="panel-heading" style={{ marginBottom: 12 }}>
                    <div>
                      <h2>
                        <Sparkles size={18} style={{ color: '#10b981' }} />
                        Recommended Next Action
                      </h2>
                      <p>The single highest-leverage milestone to address right now.</p>
                    </div>
                  </div>

                  {analysis?.skillpath.actions[0] ? (
                    <>
                      <div className="next-action-card">
                        <div className="action-step-num">01</div>
                        <div className="action-body">
                          <strong>{analysis.skillpath.actions[0].title}</strong>
                          <p>{analysis.skillpath.actions[0].action}</p>
                          <small>Why: {analysis.skillpath.actions[0].why}</small>
                        </div>
                      </div>
                      <button className="btn btn-primary" onClick={() => setActive('SkillPath')}>
                        Open Full SkillPath Roadmap <ArrowRight size={15} />
                      </button>
                    </>
                  ) : (
                    <div style={{ padding: '24px 0', textAlign: 'center', color: '#64748b' }}>
                      <BrainCircuit size={32} style={{ margin: '0 auto 10px', color: '#10b981' }} />
                      <p style={{ fontSize: 13 }}>Trigger career analysis to generate actionable guidance.</p>
                      <button className="btn btn-accent" onClick={runAnalysis} disabled={busy}>
                        {busy ? 'Computing...' : 'Analyze Career Now'}
                      </button>
                    </div>
                  )}
                </section>

                <section className="panel" style={{ margin: 0 }}>
                  <div className="panel-heading" style={{ marginBottom: 12 }}>
                    <div>
                      <h2>
                        <BriefcaseBusiness size={18} style={{ color: '#6366f1' }} />
                        Opportunity Readiness Outlook
                      </h2>
                      <p>Matched against illustrative benchmark records.</p>
                    </div>
                  </div>

                  {analysis ? (
                    <>
                      <div className="opp-counts-row">
                        <div className="opp-count-box">
                          <strong style={{ color: '#059669' }}>
                            {analysis.opportunity_summary.apply_now}
                          </strong>
                          <span>APPLY NOW</span>
                        </div>
                        <div className="opp-count-box">
                          <strong style={{ color: '#d97706' }}>
                            {analysis.opportunity_summary.prepare_and_apply}
                          </strong>
                          <span>PREPARE & APPLY</span>
                        </div>
                        <div className="opp-count-box">
                          <strong style={{ color: '#e11d48' }}>
                            {analysis.opportunity_summary.not_yet}
                          </strong>
                          <span>NOT YET</span>
                        </div>
                      </div>
                      <button
                        className="btn btn-secondary"
                        style={{ width: '100%' }}
                        onClick={() => setActive('Opportunities')}
                      >
                        Explore Matched Roles ({analysis.opportunities.length}){' '}
                        <ArrowRight size={15} />
                      </button>
                    </>
                  ) : (
                    <div style={{ padding: '24px 0', textAlign: 'center', color: '#64748b' }}>
                      <BriefcaseBusiness size={32} style={{ margin: '0 auto 10px', color: '#6366f1' }} />
                      <p style={{ fontSize: 13 }}>
                        Run analysis to rank your profile against benchmark opportunities.
                      </p>
                    </div>
                  )}
                </section>
              </div>
            </>
          )}

          {/* ======================================================== */}
          {/* PAGE 2: PROFILE & SKILLS ARCHITECTURE (SPACIOUS) */}
          {/* ======================================================== */}
          {active === 'Profile' && (
            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h2>
                    <GraduationCap size={20} style={{ color: '#10b981' }} />
                    Student Profile, Technical Stack & Evidence
                  </h2>
                  <p>
                    Type in your technical skills, hands-on projects, internships, and verified
                    credentials with full punctuation marks and detailed descriptions.
                  </p>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: 11, fontWeight: 700, color: '#059669' }}>
                    PROFILE COMPLETENESS
                  </span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 4 }}>
                    <div style={{ width: 110, height: 7, borderRadius: 9999, background: '#e2e8f0', overflow: 'hidden' }}>
                      <div
                        style={{
                          height: '100%',
                          width: `${profileCompleteness}%`,
                          background: 'linear-gradient(90deg, #10b981, #34d399)'
                        }}
                      />
                    </div>
                    <strong style={{ fontSize: 13, fontFamily: 'var(--font-heading)' }}>
                      {profileCompleteness}%
                    </strong>
                  </div>
                </div>
              </div>

              {/* Profile Subtabs */}
              <div className="profile-subtabs">
                {[
                  ['basics', '1. Academic & Career Target', GraduationCap],
                  ['skills', `2. Skills Hub (${profile.skills.length})`, Zap],
                  ['projects', `3. Projects Portfolio (${profile.projects.length})`, FolderGit2],
                  ['experience', `4. Experience (${profile.experience.length})`, BriefcaseBusiness],
                  ['certifications', `5. Certifications (${profile.certifications.length})`, Award]
                ].map(([tabKey, label, Icon]) => (
                  <button
                    key={tabKey as string}
                    className={`subtab-btn ${profileTab === tabKey ? 'active' : ''}`}
                    onClick={() => setProfileTab(tabKey as any)}
                  >
                    <Icon size={15} />
                    <span>{label as string}</span>
                  </button>
                ))}
              </div>

              {/* Subtab 1: Basics */}
              {profileTab === 'basics' && (
                <div className="form-grid">
                  <div className="field">
                    <label>
                      <span>Full Student Name</span>
                      <span className="hint">Required for official transcripts</span>
                    </label>
                    <input
                      value={profile.name}
                      onChange={e => updateProfile('name', e.target.value)}
                      placeholder="e.g. Prajwal S. Kumar"
                    />
                  </div>

                  <div className="field">
                    <label>
                      <span>Degree Program / Qualification</span>
                      <span className="hint">e.g. B.Tech., B.C.A., M.C.A., B.Sc.</span>
                    </label>
                    <input
                      value={profile.education}
                      onChange={e => updateProfile('education', e.target.value)}
                      placeholder="e.g. Bachelor of Technology (B.Tech.) in Computer Science"
                    />
                  </div>

                  <div className="field">
                    <label>
                      <span>Department / Specialization</span>
                      <span className="hint">Academic branch</span>
                    </label>
                    <input
                      value={profile.branch}
                      onChange={e => updateProfile('branch', e.target.value)}
                      placeholder="e.g. Artificial Intelligence & Data Science"
                    />
                  </div>

                  <div className="field">
                    <label>
                      <span>Current Academic Semester / Year</span>
                      <span className="hint">Cohort stage</span>
                    </label>
                    <input
                      value={profile.semester}
                      onChange={e => updateProfile('semester', e.target.value)}
                      placeholder="e.g. 7th Semester (Final Year)"
                    />
                  </div>

                  <div className="field" style={{ gridColumn: 'span 2' }}>
                    <label>
                      <span>Target Career Benchmark</span>
                      <span className="hint">Select the role you wish to be evaluated against</span>
                    </label>
                    <select
                      value={profile.target_career}
                      onChange={e => updateProfile('target_career', e.target.value)}
                    >
                      {careers.map(c => (
                        <option key={c.id} value={c.name}>
                          {c.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              )}

              {/* Subtab 2: Skills Hub */}
              {profileTab === 'skills' && (
                <div>
                  <div style={{ marginBottom: 16 }}>
                    <h3 style={{ fontSize: 15, fontWeight: 700, margin: '0 0 6px' }}>
                      Add or Remove Technical Skills & Tools
                    </h3>
                    <p style={{ fontSize: 13, color: '#64748b', margin: 0 }}>
                      Type a skill name and press Enter or comma. Supports compound tags, punctuation marks,
                      and framework names like <code>SQL (PostgreSQL)</code>, <code>C++</code>,{' '}
                      <code>Node.js</code>, and <code>Git & GitHub</code>.
                    </p>
                  </div>

                  <div className="skills-input-bar">
                    <input
                      value={skillInput}
                      onChange={e => setSkillInput(e.target.value)}
                      onKeyDown={e => {
                        if (e.key === 'Enter' || e.key === ',') {
                          e.preventDefault()
                          addSkill(skillInput)
                        }
                      }}
                      placeholder="Type a skill (e.g. Scikit-learn, FastAPI, SQL, PyTorch, Docker) and press Enter..."
                    />
                    <button className="btn btn-primary" onClick={() => addSkill(skillInput)}>
                      <Plus size={15} /> Add Skill
                    </button>
                  </div>

                  {/* Interactive Tag Cloud */}
                  <div className="interactive-tag-cloud">
                    {profile.skills.length > 0 ? (
                      profile.skills.map(s => (
                        <span className="interactive-chip" key={s}>
                          <span>{s}</span>
                          <button
                            className="remove"
                            title={`Remove ${s}`}
                            onClick={() => removeSkill(s)}
                          >
                            <X size={14} />
                          </button>
                        </span>
                      ))
                    ) : (
                      <div style={{ width: '100%', textAlign: 'center', color: '#94a3b8', padding: '20px 0' }}>
                        No skills added yet. Type a skill above or click from suggested recommendations below.
                      </div>
                    )}
                  </div>

                  {/* Quick-add Recommended Skills */}
                  {suggestedSkills.length > 0 && (
                    <div className="suggested-chips-row">
                      <span className="label">Recommended for {profile.target_career}:</span>
                      {suggestedSkills.map(s => (
                        <button
                          key={s}
                          type="button"
                          className="suggested-chip"
                          onClick={() => addSkill(s)}
                        >
                          + {s}
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Raw Multi-line Editor for high space / bulk pasting */}
                  <details style={{ marginTop: 24, padding: '14px 18px', background: '#f8fafc', borderRadius: 12, border: '1px solid #e2e8f0' }}>
                    <summary style={{ cursor: 'pointer', fontWeight: 700, fontSize: 13, color: '#334155' }}>
                      Need to bulk paste or type with unlimited space? Open Raw Text Editor
                    </summary>
                    <div style={{ marginTop: 12 }}>
                      <textarea
                        style={{ width: '100%', minHeight: 110, padding: 12, borderRadius: 8, border: '1px solid #cbd5e1', fontSize: 13 }}
                        value={profile.skills.join(', ')}
                        onChange={e =>
                          updateProfile(
                            'skills',
                            e.target.value
                              .split(/[,;\n]/)
                              .map(s => s.trim())
                              .filter(Boolean)
                          )
                        }
                        placeholder="Paste comma-separated skills here..."
                      />
                      <small style={{ color: '#64748b' }}>
                        Changes here immediately sync with your skills cloud above.
                      </small>
                    </div>
                  </details>
                </div>
              )}

              {/* Subtab 3: Projects */}
              {profileTab === 'projects' && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                    <div>
                      <h3 style={{ fontSize: 15, fontWeight: 700, margin: '0 0 4px' }}>
                        Documented Projects Portfolio ({profile.projects.length})
                      </h3>
                      <p style={{ fontSize: 13, color: '#64748b', margin: 0 }}>
                        Provide detailed multi-sentence project descriptions with proper punctuation marks,
                        technologies used, and impact metrics.
                      </p>
                    </div>

                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => setShowAddProject(!showAddProject)}
                    >
                      {showAddProject ? <X size={14} /> : <Plus size={14} />}
                      {showAddProject ? 'Cancel' : 'Add New Project'}
                    </button>
                  </div>

                  {/* Add Project Form Drawer */}
                  {showAddProject && (
                    <form
                      onSubmit={handleAddProject}
                      style={{
                        padding: 20,
                        background: '#f8fafc',
                        border: '1px solid #cbd5e1',
                        borderRadius: 14,
                        marginBottom: 20
                      }}
                    >
                      <h4 style={{ margin: '0 0 14px', fontSize: 14, fontWeight: 800 }}>
                        Add Project Details
                      </h4>
                      <div className="form-grid" style={{ marginBottom: 12 }}>
                        <div className="field">
                          <label>Project Title / Identifier</label>
                          <input
                            required
                            value={newProject.title}
                            onChange={e => setNewProject(p => ({ ...p, title: e.target.value }))}
                            placeholder="e.g. Real-Time Fraud Detection Pipeline"
                          />
                        </div>
                        <div className="field">
                          <label>Tech Stack & Tools</label>
                          <input
                            value={newProject.techStack}
                            onChange={e => setNewProject(p => ({ ...p, techStack: e.target.value }))}
                            placeholder="e.g. Python, Scikit-learn, FastAPI, PostgreSQL"
                          />
                        </div>
                        <div className="field" style={{ gridColumn: 'span 2' }}>
                          <label>Repository or Live Demo Link (Optional)</label>
                          <input
                            value={newProject.link}
                            onChange={e => setNewProject(p => ({ ...p, link: e.target.value }))}
                            placeholder="e.g. https://github.com/username/fraud-detector"
                          />
                        </div>
                        <div className="field" style={{ gridColumn: 'span 2' }}>
                          <label>
                            Detailed Project Description & Results
                            <span className="hint">
                              Use complete sentences with periods, semicolons, and commas.
                            </span>
                          </label>
                          <textarea
                            required
                            style={{ minHeight: 90 }}
                            value={newProject.description}
                            onChange={e => setNewProject(p => ({ ...p, description: e.target.value }))}
                            placeholder="Describe architecture, datasets used, methodology, and quantifiable results achieved..."
                          />
                        </div>
                      </div>
                      <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
                        <button
                          type="button"
                          className="btn btn-secondary btn-sm"
                          onClick={() => setShowAddProject(false)}
                        >
                          Cancel
                        </button>
                        <button type="submit" className="btn btn-accent btn-sm">
                          Save Project
                        </button>
                      </div>
                    </form>
                  )}

                  {/* Project Cards List */}
                  <div className="items-list-container">
                    {profile.projects.length > 0 ? (
                      profile.projects.map((projStr, idx) => (
                        <div className="item-entry-card" key={idx}>
                          <div className="item-entry-top">
                            <div>
                              <h4 className="item-entry-title">
                                Project #{idx + 1}: {projStr.split(':')[0]}
                              </h4>
                            </div>
                            <div className="item-entry-actions">
                              <button
                                className="icon-action-btn delete"
                                title="Remove project"
                                onClick={() => removeProject(idx)}
                              >
                                <Trash2 size={15} />
                              </button>
                            </div>
                          </div>
                          <p className="item-entry-desc">
                            {projStr.includes(':') ? projStr.split(':').slice(1).join(':').trim() : projStr}
                          </p>
                        </div>
                      ))
                    ) : (
                      <div style={{ padding: 30, textAlign: 'center', background: '#f8fafc', borderRadius: 12, border: '1px dashed #cbd5e1' }}>
                        <FolderGit2 size={32} style={{ margin: '0 auto 8px', color: '#94a3b8' }} />
                        <p style={{ color: '#64748b', fontSize: 13, margin: 0 }}>
                          No projects recorded yet. Click "Add New Project" to document your work.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Subtab 4: Experience */}
              {profileTab === 'experience' && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                    <div>
                      <h3 style={{ fontSize: 15, fontWeight: 700, margin: '0 0 4px' }}>
                        Internships & Practical Work Experience ({profile.experience.length})
                      </h3>
                      <p style={{ fontSize: 13, color: '#64748b', margin: 0 }}>
                        Include research assistantships, industrial internships, open-source roles, or
                        academic lab experience.
                      </p>
                    </div>

                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => setShowAddExp(!showAddExp)}
                    >
                      {showAddExp ? <X size={14} /> : <Plus size={14} />}
                      {showAddExp ? 'Cancel' : 'Add Experience'}
                    </button>
                  </div>

                  {/* Add Experience Form */}
                  {showAddExp && (
                    <form
                      onSubmit={handleAddExperience}
                      style={{
                        padding: 20,
                        background: '#f8fafc',
                        border: '1px solid #cbd5e1',
                        borderRadius: 14,
                        marginBottom: 20
                      }}
                    >
                      <h4 style={{ margin: '0 0 14px', fontSize: 14, fontWeight: 800 }}>
                        Add Experience Record
                      </h4>
                      <div className="form-grid" style={{ marginBottom: 12 }}>
                        <div className="field">
                          <label>Job Title / Role</label>
                          <input
                            required
                            value={newExperience.role}
                            onChange={e => setNewExperience(x => ({ ...x, role: e.target.value }))}
                            placeholder="e.g. Machine Learning Engineering Intern"
                          />
                        </div>
                        <div className="field">
                          <label>Company / Organization</label>
                          <input
                            required
                            value={newExperience.company}
                            onChange={e => setNewExperience(x => ({ ...x, company: e.target.value }))}
                            placeholder="e.g. Center for AI Studies"
                          />
                        </div>
                        <div className="field" style={{ gridColumn: 'span 2' }}>
                          <label>Duration / Dates</label>
                          <input
                            value={newExperience.duration}
                            onChange={e => setNewExperience(x => ({ ...x, duration: e.target.value }))}
                            placeholder="e.g. Jan 2024 – May 2024"
                          />
                        </div>
                        <div className="field" style={{ gridColumn: 'span 2' }}>
                          <label>Key Responsibilities & Highlights (Full sentences)</label>
                          <textarea
                            required
                            style={{ minHeight: 90 }}
                            value={newExperience.description}
                            onChange={e => setNewExperience(x => ({ ...x, description: e.target.value }))}
                            placeholder="Preprocessed 250,000+ tabular records using Pandas and SQL; engineered automated validation routines..."
                          />
                        </div>
                      </div>
                      <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
                        <button
                          type="button"
                          className="btn btn-secondary btn-sm"
                          onClick={() => setShowAddExp(false)}
                        >
                          Cancel
                        </button>
                        <button type="submit" className="btn btn-accent btn-sm">
                          Save Experience
                        </button>
                      </div>
                    </form>
                  )}

                  {/* Experience Cards */}
                  <div className="items-list-container">
                    {profile.experience.length > 0 ? (
                      profile.experience.map((expStr, idx) => (
                        <div className="item-entry-card" key={idx}>
                          <div className="item-entry-top">
                            <div>
                              <h4 className="item-entry-title">
                                {expStr.split(':')[0]}
                              </h4>
                            </div>
                            <div className="item-entry-actions">
                              <button
                                className="icon-action-btn delete"
                                title="Remove experience"
                                onClick={() => removeExperience(idx)}
                              >
                                <Trash2 size={15} />
                              </button>
                            </div>
                          </div>
                          <p className="item-entry-desc">
                            {expStr.includes(':') ? expStr.split(':').slice(1).join(':').trim() : expStr}
                          </p>
                        </div>
                      ))
                    ) : (
                      <div style={{ padding: 30, textAlign: 'center', background: '#f8fafc', borderRadius: 12, border: '1px dashed #cbd5e1' }}>
                        <BriefcaseBusiness size={32} style={{ margin: '0 auto 8px', color: '#94a3b8' }} />
                        <p style={{ color: '#64748b', fontSize: 13, margin: 0 }}>
                          No work or internship experience documented yet.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Subtab 5: Certifications */}
              {profileTab === 'certifications' && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                    <div>
                      <h3 style={{ fontSize: 15, fontWeight: 700, margin: '0 0 4px' }}>
                        Verified Certifications & Accreditations ({profile.certifications.length})
                      </h3>
                      <p style={{ fontSize: 13, color: '#64748b', margin: 0 }}>
                        Add industry certifications, verified online courses, and external accreditations.
                      </p>
                    </div>

                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => setShowAddCert(!showAddCert)}
                    >
                      {showAddCert ? <X size={14} /> : <Plus size={14} />}
                      {showAddCert ? 'Cancel' : 'Add Certification'}
                    </button>
                  </div>

                  {/* Add Cert Form */}
                  {showAddCert && (
                    <form
                      onSubmit={handleAddCert}
                      style={{
                        padding: 20,
                        background: '#f8fafc',
                        border: '1px solid #cbd5e1',
                        borderRadius: 14,
                        marginBottom: 20
                      }}
                    >
                      <h4 style={{ margin: '0 0 14px', fontSize: 14, fontWeight: 800 }}>
                        Add Certification Record
                      </h4>
                      <div className="form-grid" style={{ marginBottom: 12 }}>
                        <div className="field">
                          <label>Certification Name</label>
                          <input
                            required
                            value={newCert.name}
                            onChange={e => setNewCert(c => ({ ...c, name: e.target.value }))}
                            placeholder="e.g. Deep Learning Specialization"
                          />
                        </div>
                        <div className="field">
                          <label>Issuing Institution</label>
                          <input
                            required
                            value={newCert.issuer}
                            onChange={e => setNewCert(c => ({ ...c, issuer: e.target.value }))}
                            placeholder="e.g. Coursera / DeepLearning.AI"
                          />
                        </div>
                        <div className="field">
                          <label>Issue Year or Credential ID</label>
                          <input
                            value={newCert.yearOrId}
                            onChange={e => setNewCert(c => ({ ...c, yearOrId: e.target.value }))}
                            placeholder="e.g. 2024 or ID: DL-89240"
                          />
                        </div>
                        <div className="field">
                          <label>Verification URL (Optional)</label>
                          <input
                            value={newCert.link}
                            onChange={e => setNewCert(c => ({ ...c, link: e.target.value }))}
                            placeholder="e.g. https://coursera.org/verify/..."
                          />
                        </div>
                      </div>
                      <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
                        <button
                          type="button"
                          className="btn btn-secondary btn-sm"
                          onClick={() => setShowAddCert(false)}
                        >
                          Cancel
                        </button>
                        <button type="submit" className="btn btn-accent btn-sm">
                          Save Certification
                        </button>
                      </div>
                    </form>
                  )}

                  {/* Certifications Cards */}
                  <div className="items-list-container">
                    {profile.certifications.length > 0 ? (
                      profile.certifications.map((certStr, idx) => (
                        <div className="item-entry-card" key={idx}>
                          <div className="item-entry-top">
                            <div>
                              <h4 className="item-entry-title">
                                <Award size={16} style={{ display: 'inline', color: '#f59e0b', marginRight: 6 }} />
                                {certStr}
                              </h4>
                            </div>
                            <div className="item-entry-actions">
                              <button
                                className="icon-action-btn delete"
                                title="Remove certification"
                                onClick={() => removeCert(idx)}
                              >
                                <Trash2 size={15} />
                              </button>
                            </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div style={{ padding: 30, textAlign: 'center', background: '#f8fafc', borderRadius: 12, border: '1px dashed #cbd5e1' }}>
                        <Award size={32} style={{ margin: '0 auto 8px', color: '#94a3b8' }} />
                        <p style={{ color: '#64748b', fontSize: 13, margin: 0 }}>
                          No certifications recorded yet.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Panel Footer Action */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  borderTop: '1px solid #e2e8f0',
                  paddingTop: 20,
                  marginTop: 28
                }}
              >
                <span style={{ fontSize: 12.5, color: '#64748b' }}>
                  All updates are evaluated by FastAPI using transparent, deterministic rules.
                </span>
                <button className="btn btn-accent" disabled={busy} onClick={runAnalysis}>
                  {busy ? <LoaderCircle className="spin" size={16} /> : <ArrowRight size={16} />}
                  Save & Analyze Career Now
                </button>
              </div>
            </section>
          )}

          {/* ======================================================== */}
          {/* PAGE 3: RESUME ANALYSIS (SPACIOUS) */}
          {/* ======================================================== */}
          {active === 'Resume' && (
            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h2>
                    <FileText size={20} style={{ color: '#10b981' }} />
                    Automated Resume Parsing & Skill Ingestion
                  </h2>
                  <p>
                    Upload a PDF, DOCX, or text file, or paste your complete multi-page resume text below.
                  </p>
                </div>
              </div>

              {/* File Dropzone */}
              <label className="upload-dropzone">
                <Upload size={32} />
                <strong>Choose or drag-and-drop your resume file</strong>
                <span>Supports PDF, DOCX, or TXT · Maximum 5 MB</span>
                <input
                  type="file"
                  style={{ display: 'none' }}
                  accept=".pdf,.docx,.txt"
                  onChange={e => e.target.files?.[0] && doResumeAnalysis(e.target.files[0])}
                />
              </label>

              <div className="or-divider">OR PASTE COMPREHENSIVE RESUME TEXT BELOW</div>

              <textarea
                className="resume-textarea"
                value={resumeText}
                onChange={e => setResumeText(e.target.value)}
                placeholder="Paste your full resume here including Technical Skills, Academic Projects, Work Experience, and Certifications..."
              />

              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginTop: 18
                }}
              >
                <span style={{ fontSize: 12, color: '#64748b' }}>
                  Word count: {resumeText.trim().split(/\s+/).filter(Boolean).length} words
                </span>
                <button
                  className="btn btn-accent"
                  disabled={busy}
                  onClick={() => doResumeAnalysis()}
                >
                  {busy ? <LoaderCircle className="spin" size={16} /> : <Sparkles size={16} />}
                  Extract Skills & Entities
                </button>
              </div>

              {/* Detected Resume Entities Box */}
              {resumeInfo && (
                <div className="resume-detected-box">
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: 12
                    }}
                  >
                    <h3 style={{ fontSize: 15, fontWeight: 800, margin: 0 }}>
                      Extracted Resume Intelligence
                    </h3>
                    <span
                      style={{
                        fontSize: 12,
                        fontWeight: 700,
                        color: '#059669',
                        background: '#ecfdf5',
                        padding: '4px 10px',
                        borderRadius: 6
                      }}
                    >
                      Extraction Confidence: {Math.round(resumeInfo.confidence * 100)}%
                    </span>
                  </div>

                  <p style={{ fontSize: 12.5, color: '#64748b', margin: '0 0 12px' }}>
                    Methodology: {resumeInfo.method}
                  </p>

                  <div style={{ marginBottom: 16 }}>
                    <small
                      style={{
                        display: 'block',
                        fontSize: 11,
                        fontWeight: 700,
                        textTransform: 'uppercase',
                        color: '#64748b',
                        marginBottom: 8
                      }}
                    >
                      Detected Skills ({resumeInfo.skills.length})
                    </small>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                      {resumeInfo.skills.map(s => (
                        <span className="skill-pill-tag green" key={s}>
                          <Check size={12} /> {s}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: 10, marginTop: 16 }}>
                    <button className="btn btn-primary btn-sm" onClick={() => setActive('Profile')}>
                      Review in Profile Portfolio <ArrowRight size={14} />
                    </button>
                    <button className="btn btn-accent btn-sm" onClick={runAnalysis}>
                      Run Career Analysis Now <Zap size={14} />
                    </button>
                  </div>
                </div>
              )}
            </section>
          )}

          {/* ======================================================== */}
          {/* PAGE 4: SKILLPATH ROADMAP */}
          {/* ======================================================== */}
          {active === 'SkillPath' && (
            <div>
              <div className="panel-heading" style={{ marginBottom: 20 }}>
                <div>
                  <h2>
                    <BrainCircuit size={20} style={{ color: '#10b981' }} />
                    Personalized SkillPath Learning & Project Roadmap
                  </h2>
                  <p>
                    Rule-based sequence synthesized from identified skill gaps, critical requirements,
                    and opportunity overlap.
                  </p>
                </div>
                {analysis && (
                  <span className="live-pill" style={{ background: '#f0fdf4', color: '#166534', border: '1px solid #bbf7d0' }}>
                    <Activity size={13} /> {analysis.skillpath.actions.length} Milestones Computed
                  </span>
                )}
              </div>

              {analysis ? (
                <div className="roadmap-container">
                  {analysis.skillpath.actions.map((act, i) => {
                    const isDone = !!completedActions[act.title]
                    return (
                      <div
                        className="roadmap-step-card"
                        key={`${act.title}-${i}`}
                        style={{ opacity: isDone ? 0.75 : 1 }}
                      >
                        <div
                          className="step-indicator"
                          style={{
                            background: isDone ? '#10b981' : '#0f172a',
                            color: '#ffffff'
                          }}
                        >
                          {isDone ? <Check size={20} /> : String(i + 1).padStart(2, '0')}
                        </div>

                        <div className="step-content">
                          <div className="step-header">
                            <span
                              className={`priority-badge ${
                                act.priority.toLowerCase() === 'high' ? 'high' : 'medium'
                              }`}
                            >
                              {act.priority} Priority
                            </span>
                            <span style={{ fontSize: 12, fontWeight: 700, color: '#64748b' }}>
                              Focus Skill: {act.skill}
                            </span>
                          </div>

                          <h3 style={{ textDecoration: isDone ? 'line-through' : 'none' }}>
                            {act.title}
                          </h3>

                          <p className="action-text">{act.action}</p>

                          <div className="why-callout">
                            <Sparkles size={16} style={{ flexShrink: 0, marginTop: 1 }} />
                            <span>
                              <b>Strategic Rationale:</b> {act.why}
                            </span>
                          </div>
                        </div>

                        <button
                          type="button"
                          className={`btn btn-sm ${isDone ? 'btn-secondary' : 'btn-primary'}`}
                          onClick={() =>
                            setCompletedActions(prev => ({
                              ...prev,
                              [act.title]: !prev[act.title]
                            }))
                          }
                        >
                          {isDone ? (
                            <>
                              <CheckCircle2 size={14} style={{ color: '#10b981' }} /> Done
                            </>
                          ) : (
                            'Mark Done'
                          )}
                        </button>
                      </div>
                    )
                  })}

                  <div
                    style={{
                      background: '#f1f5f9',
                      borderRadius: 12,
                      padding: '14px 18px',
                      fontSize: 12.5,
                      color: '#475569',
                      marginTop: 8
                    }}
                  >
                    💡 <b>Pro Tip:</b> Work through the high-priority milestones first. As you complete
                    projects or gain certifications, update your profile and rerun analysis to track your
                    improved score.
                  </div>
                </div>
              ) : (
                <div style={{ padding: 60, textAlign: 'center', background: '#ffffff', borderRadius: 16, border: '1px solid #e2e8f0' }}>
                  <BrainCircuit size={48} style={{ color: '#10b981', margin: '0 auto 12px' }} />
                  <h3 style={{ fontSize: 18, fontWeight: 800, margin: '0 0 8px' }}>
                    Action Plan Pending Analysis
                  </h3>
                  <p style={{ color: '#64748b', fontSize: 14, maxWidth: 440, margin: '0 auto 18px' }}>
                    Run career analysis on your profile to generate a customized step-by-step SkillPath.
                  </p>
                  <button className="btn btn-accent" onClick={runAnalysis}>
                    Run Analysis Now <ArrowRight size={15} />
                  </button>
                </div>
              )}
            </div>
          )}

          {/* ======================================================== */}
          {/* PAGE 5: OPPORTUNITIES EXPLORER */}
          {/* ======================================================== */}
          {active === 'Opportunities' && (
            <div>
              <div className="panel-heading" style={{ marginBottom: 20 }}>
                <div>
                  <h2>
                    <BriefcaseBusiness size={20} style={{ color: '#10b981' }} />
                    Opportunities Matching Engine
                  </h2>
                  <p>
                    Ranked against your student profile using mandatory skills, preferred skills, project
                    evidence, and degree qualifications.
                  </p>
                </div>
              </div>

              {/* Filter and Search Bar */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: 16,
                  marginBottom: 20,
                  flexWrap: 'wrap'
                }}
              >
                {/* Status Filter Tabs */}
                <div style={{ display: 'flex', gap: 6 }}>
                  {(['ALL', 'APPLY NOW', 'PREPARE & APPLY', 'NOT YET'] as const).map(tab => (
                    <button
                      key={tab}
                      className={`btn btn-sm ${oppFilter === tab ? 'btn-primary' : 'btn-secondary'}`}
                      onClick={() => setOppFilter(tab)}
                    >
                      {tab}
                    </button>
                  ))}
                </div>

                {/* Search Input */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, maxWidth: 320, width: '100%' }}>
                  <div style={{ position: 'relative', width: '100%' }}>
                    <Search
                      size={15}
                      style={{ position: 'absolute', left: 12, top: 12, color: '#94a3b8' }}
                    />
                    <input
                      style={{
                        width: '100%',
                        padding: '9px 12px 9px 34px',
                        borderRadius: 8,
                        border: '1px solid #cbd5e1',
                        fontSize: 13
                      }}
                      value={oppSearch}
                      onChange={e => setOppSearch(e.target.value)}
                      placeholder="Search company, role, skill..."
                    />
                  </div>
                </div>
              </div>

              {/* Opportunity Cards */}
              {analysis ? (
                <div className="opportunity-grid">
                  {filteredOpportunities.length > 0 ? (
                    filteredOpportunities.map(o => (
                      <article className="opp-card" key={o.id}>
                        <div className="opp-top-row">
                          <div className="opp-company-badge">
                            <Building size={24} />
                          </div>
                          <div className="opp-info-block">
                            <h3>{o.role}</h3>
                            <p className="company">{o.company}</p>
                            <span style={{ fontSize: 13, color: '#475569', lineHeight: 1.5 }}>
                              {o.description}
                            </span>
                          </div>

                          <div className="opp-score-badge">
                            <strong>{o.match_score}%</strong>
                            <span>MATCH INDEX</span>
                          </div>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                          <span
                            className={`classification-tag ${
                              o.classification === 'APPLY NOW'
                                ? 'apply'
                                : o.classification === 'PREPARE & APPLY'
                                ? 'prepare'
                                : 'notyet'
                            }`}
                          >
                            {o.classification}
                          </span>
                          <span style={{ fontSize: 12, color: '#64748b' }}>
                            {o.matched_skills.length} core requirements matched
                          </span>
                        </div>

                        {/* Side by side skills comparison */}
                        <div className="opp-skills-comparison">
                          <div>
                            <small>Matched Capabilities</small>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                              {o.matched_skills.length > 0 ? (
                                o.matched_skills.map(s => (
                                  <span className="skill-pill-tag green" key={s}>
                                    <Check size={12} /> {s}
                                  </span>
                                ))
                              ) : (
                                <span style={{ fontSize: 12, color: '#94a3b8' }}>None matched</span>
                              )}
                            </div>
                          </div>

                          <div>
                            <small>Missing Requirements</small>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                              {o.missing_skills.length > 0 ? (
                                o.missing_skills.map(s => (
                                  <span className="skill-pill-tag rose" key={s}>
                                    <X size={12} /> {s}
                                  </span>
                                ))
                              ) : (
                                <span style={{ fontSize: 12, color: '#059669' }}>All requirements met!</span>
                              )}
                            </div>
                          </div>
                        </div>

                        <p
                          style={{
                            fontSize: 12.5,
                            color: '#334155',
                            background: '#f8fafc',
                            padding: '10px 14px',
                            borderRadius: 8,
                            margin: 0,
                            lineHeight: 1.5
                          }}
                        >
                          {o.explanation}
                        </p>

                        <div
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            borderTop: '1px solid #e2e8f0',
                            paddingTop: 12
                          }}
                        >
                          <button
                            type="button"
                            className="btn btn-secondary btn-sm"
                            onClick={() => setSelectedOpp(selectedOpp === o.id ? null : o.id)}
                          >
                            <Eye size={14} />
                            {selectedOpp === o.id ? 'Hide Match Intelligence' : 'Match Intelligence'}
                          </button>

                          <a
                            className="btn btn-primary btn-sm"
                            href={o.application_url || '#'}
                            target="_blank"
                            rel="noreferrer"
                            onClick={e => {
                              if (!o.application_url) e.preventDefault()
                            }}
                          >
                            Apply / Review Role <ExternalLink size={13} />
                          </a>
                        </div>

                        {/* Detailed Reasoning drawer */}
                        {selectedOpp === o.id && (
                          <div
                            style={{
                              background: '#f0fdf4',
                              border: '1px solid #bbf7d0',
                              borderRadius: 10,
                              padding: 16,
                              fontSize: 12.5,
                              color: '#166534',
                              lineHeight: 1.6
                            }}
                          >
                            <h4 style={{ margin: '0 0 6px', fontSize: 13, fontWeight: 800 }}>
                              Decision Breakdown & Rationale:
                            </h4>
                            <p style={{ margin: '0 0 8px' }}>{o.explanation}</p>
                            {o.critical_missing_skills.length > 0 && (
                              <p style={{ margin: 0, color: '#991b1b' }}>
                                <b>Critical Gap Threshold:</b>{' '}
                                {o.critical_missing_skills.join(', ')} — Mandatory before recommendation
                                upgrades to "APPLY NOW".
                              </p>
                            )}
                          </div>
                        )}
                      </article>
                    ))
                  ) : (
                    <div style={{ padding: 40, textAlign: 'center', color: '#64748b' }}>
                      No opportunities match the selected filter criteria.
                    </div>
                  )}
                </div>
              ) : (
                <div style={{ padding: 60, textAlign: 'center', background: '#ffffff', borderRadius: 16, border: '1px solid #e2e8f0' }}>
                  <BriefcaseBusiness size={48} style={{ color: '#10b981', margin: '0 auto 12px' }} />
                  <h3 style={{ fontSize: 18, fontWeight: 800, margin: '0 0 8px' }}>
                    Opportunities Awaiting Profile Analysis
                  </h3>
                  <p style={{ color: '#64748b', fontSize: 14, maxWidth: 440, margin: '0 auto 18px' }}>
                    Run career analysis to evaluate your profile against all 8 demo opportunities.
                  </p>
                  <button className="btn btn-accent" onClick={runAnalysis}>
                    Run Analysis Now <ArrowRight size={15} />
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Footer */}
          <footer
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderTop: '1px solid #e2e8f0',
              marginTop: 40,
              paddingTop: 20,
              color: '#94a3b8',
              fontSize: 12
            }}
          >
            <span>SkillPath AI · AI-Powered Skill Gap Analysis & Career Readiness Navigator</span>
            <span>Final Academic MVP · Connected to FastAPI Backend</span>
          </footer>
        </div>
      </main>

      {/* Global Export Report Modal */}
      {showReportModal && (
        <div className="modal-overlay" onClick={() => setShowReportModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Career Readiness Assessment Summary Report</h2>
              <button
                className="icon-action-btn"
                onClick={() => setShowReportModal(false)}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ fontSize: 13.5, lineHeight: 1.6, color: '#334155' }}>
              <div style={{ padding: '16px 20px', background: '#f8fafc', borderRadius: 12, marginBottom: 16 }}>
                <strong>Candidate:</strong> {profile.name} ({profile.education}, {profile.semester})<br />
                <strong>Target Role:</strong> {profile.target_career}<br />
                <strong>Overall Readiness Index:</strong>{' '}
                <span style={{ color: '#059669', fontWeight: 800 }}>
                  {analysis ? `${score}/100 (${analysis.readiness.classification})` : 'Pending Analysis'}
                </span>
              </div>

              <h4 style={{ margin: '14px 0 6px', fontWeight: 800 }}>Verified Skills:</h4>
              <p style={{ margin: 0 }}>{profile.skills.join(', ')}</p>

              <h4 style={{ margin: '14px 0 6px', fontWeight: 800 }}>Documented Projects:</h4>
              <ul style={{ margin: 0, paddingLeft: 20 }}>
                {profile.projects.map((p, idx) => (
                  <li key={idx}>{p}</li>
                ))}
              </ul>

              {analysis && (
                <>
                  <h4 style={{ margin: '14px 0 6px', fontWeight: 800 }}>Strategic Gaps to Address:</h4>
                  <p style={{ margin: 0, color: '#e11d48' }}>
                    {analysis.skill_gap.missing.join(', ') || 'None identified!'}
                  </p>
                </>
              )}
            </div>

            <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end', marginTop: 16 }}>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => {
                  window.print()
                }}
              >
                <Download size={14} /> Print / Save PDF
              </button>
              <button
                className="btn btn-primary btn-sm"
                onClick={() => {
                  navigator.clipboard.writeText(
                    `SkillPath AI Career Readiness Report\nCandidate: ${profile.name}\nTarget: ${profile.target_career}\nScore: ${score}/100\nSkills: ${profile.skills.join(', ')}`
                  )
                  setNotice('Report summary copied to clipboard!')
                  setShowReportModal(false)
                }}
              >
                <Share2 size={14} /> Copy to Clipboard
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Busy Processing Indicator */}
      {busy && (
        <div className="busy-pill">
          <LoaderCircle className="spin" size={17} />
          <span>Processing Profile & Computing Intelligence...</span>
        </div>
      )}
    </div>
  )
}
