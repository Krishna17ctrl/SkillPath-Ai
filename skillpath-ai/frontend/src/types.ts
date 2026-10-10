export type Profile = {
  name: string
  education: string
  branch: string
  semester: string
  skills: string[]
  projects: string[]
  experience: string[]
  certifications: string[]
  target_career: string
  resume_text: string
  proficiency?: Record<string, number>
}

export type SkillGap = {
  strong: string[]
  developing: string[]
  missing: string[]
  required_count: number
  coverage_score: number
}

export type Action = {
  title: string
  skill: string
  action: string
  why: string
  priority: string
  course?: string
  provider?: string
  course_url?: string
  degree_bridge?: string
}

export type Opportunity = {
  id: string
  role: string
  company: string
  match_score: number
  matched_skills: string[]
  developing_skills: string[]
  missing_skills: string[]
  critical_missing_skills: string[]
  classification: string
  explanation: string
  application_url?: string
  description?: string
}

export type Analysis = {
  target_career: {
    id: string
    name: string
    required_skills: string[]
    critical_skills: string[]
    related_skills?: Record<string, string[]>
  }
  skill_gap: SkillGap
  readiness: {
    overall_score: number
    technical_skills: number
    project_experience: number
    industry_alignment: number
    internship_readiness: number
    portfolio_strength: number
    classification: string
    note: string
    weights?: Record<string, number>
  }
  skillpath: {
    actions: Action[]
    next_best_action: string
    method: string
  }
  opportunities: Opportunity[]
  opportunity_summary: {
    apply_now: number
    prepare_and_apply: number
    not_yet: number
  }
}

export type StructuredProject = {
  id: string
  title: string
  techStack: string
  link: string
  description: string
}

export type StructuredExperience = {
  id: string
  role: string
  company: string
  duration: string
  description: string
}

export type StructuredCertification = {
  id: string
  name: string
  issuer: string
  yearOrId: string
  link: string
}
