# Quick Reference: Project Alignment & SDD Governance

## What Was Aligned?

Your three projects (`backend`, `memory`, `my-ai-book`) were aligned to follow the **Spec-Driven Development (SDD)** model from AI-Native-Development.

## Key Changes Per Project

### Backend
- ✅ Added `.specify/` with governance framework
- ✅ Added `.gemini/commands/` with 11 Spec-Kit commands
- ✅ Created `GEMINI.md` with backend-specific agent rules
- ✅ Created `history/prompts/` for PHR tracking
- ✅ Created `specs/001-rag-backend/` structure
- ✅ Created project constitution for API development
- ✅ Added reusable templates (spec, plan, checklist, phr)

### Memory
- ✅ Added `.specify/` with governance framework
- ✅ Added `.gemini/commands/` with 11 Spec-Kit commands
- ✅ Created `GEMINI.md` with knowledge-management rules
- ✅ Created `history/prompts/` for PHR tracking
- ✅ Created `specs/002-rag-system/` structure
- ✅ Created project constitution for knowledge management
- ✅ Added reusable templates

### My-AI-Book
- ✅ Added `.specify/` with governance framework
- ✅ Added `.gemini/commands/` with 11 Spec-Kit commands
- ✅ Created `GEMINI.md` with documentation-specific rules
- ✅ Created `history/prompts/` including ai-native-docs-chapter/
- ✅ Created `specs/001-ai-native-docs-chapter/` structure
- ✅ Created project constitution for documentation
- ✅ Added reusable templates

## File Structure Template (All Projects)

```
project/
├── .specify/                      # Governance Framework
│   ├── memory/
│   │   └── constitution.md        # Project Principles
│   ├── scripts/powershell/        # Automation Scripts
│   └── templates/                 # Reusable Templates
│       ├── spec-template.md
│       ├── plan-template.md
│       ├── checklist-template.md
│       └── phr-template.prompt.md
│
├── .gemini/commands/              # Spec-Kit Commands (11 files)
│   ├── sp.adr.toml
│   ├── sp.analyze.toml
│   ├── sp.checklist.toml
│   ├── sp.clarify.toml
│   ├── sp.constitution.toml
│   ├── sp.git.commit_pr.toml
│   ├── sp.implement.toml
│   ├── sp.phr.toml
│   ├── sp.plan.toml
│   ├── sp.specify.toml
│   └── sp.tasks.toml
│
├── history/                       # Work History & Decisions
│   └── prompts/
│       ├── constitution/          # Constitutional PHRs
│       ├── general/               # General work PHRs
│       └── [feature-name]/        # Feature-specific PHRs
│
├── specs/                         # Feature Specifications
│   └── [feature-id]/
│       ├── spec.md                # Detailed requirements
│       ├── plan.md                # Implementation plan
│       ├── research.md            # Research findings
│       └── checklists/
│
├── GEMINI.md                      # Agent Development Rules
└── [project-specific files]       # Existing project files
```

## How to Use This Structure

### For Creating a New Feature:

1. **Create Specification**
   ```
   specs/[FEATURE_ID]/spec.md  ← Use spec-template.md
   ```

2. **Create Implementation Plan**
   ```
   specs/[FEATURE_ID]/plan.md  ← Use plan-template.md
   ```

3. **Create Checklist**
   ```
   specs/[FEATURE_ID]/checklists/requirements.md  ← Use checklist-template.md
   ```

4. **Do the Work** (following GEMINI.md rules)

5. **Record History**
   ```
   history/prompts/[FEATURE_NAME]/[ID]-description.md  ← Use phr-template.prompt.md
   ```

### For Making a Decision:

1. **Detect Decision**: Is this architecturally significant?
2. **Create ADR**: Suggest "📋 Architectural decision detected: [brief]. Document? Run `/sp.adr [title]`"
3. **Record PHR**: Document in `history/prompts/general/` or `constitution/`

## Constitution Rules by Project

### Backend Constitution
- API Compliance and Standardization
- Vector Database Integration (Qdrant)
- AI Model Compatibility (Gemini via OpenAI)
- Environment Security (.env)
- Code Quality and Testing
- Documentation and Traceability

### Memory Constitution
- Single Source of Truth
- Specification-First Development
- Decision Tracking (ADRs)
- Prompt History Recording (PHRs)
- Knowledge Organization
- Accessibility and Clarity

### My-AI-Book Constitution
- Clarity, Structure, and Correctness
- Docusaurus Best Practices
- Minimal Technical Jargon
- High-Quality Final Product
- Portability and Integration
- AI-Native Development Focus

## Command Reference (All Projects)

All projects have 11 standardized commands:

| Command | Purpose | When to Use |
|---------|---------|-----------|
| `sp.adr` | Create Architecture Decision Record | After major architectural decision |
| `sp.analyze` | Analyze code/knowledge structure | When exploring codebase |
| `sp.checklist` | Create requirements checklist | Before starting feature work |
| `sp.clarify` | Clarify requirements | When requirements unclear |
| `sp.constitution` | Define project principles | At project start |
| `sp.git.commit_pr` | Create commits/PRs | After completing work |
| `sp.implement` | Implement from specifications | During active development |
| `sp.phr` | Create Prompt History Record | After completing any work |
| `sp.plan` | Create implementation plan | After specification |
| `sp.specify` | Create detailed specification | At start of feature |
| `sp.tasks` | Create task breakdown | After planning |

## PHR Storage Structure

### All Projects

```
history/prompts/
├── constitution/                  # PHRs about project principles
│   └── [ID]-[slug].constitution.prompt.md
├── general/                       # General work PHRs
│   └── [ID]-[slug].general.prompt.md
└── [feature-name]/               # Feature-specific PHRs
    └── [ID]-[slug].[stage].prompt.md
```

Where `stage` = spec | plan | tasks | red | green | refactor | explainer | misc

### My-AI-Book Special Case
Also has: `history/prompts/ai-native-docs-chapter/` for documentation work

## Strict Adherence Requirements

✅ **MUST Follow:**
1. Constitution principles for each project
2. File structure with correct directory hierarchy
3. Template usage for all specifications and documents
4. PHR creation for all significant work
5. GEMINI.md rules for agent behavior
6. Spec-first development approach

✅ **MUST NOT:**
1. Hardcode secrets (use `.env`)
2. Skip specifications for implementation
3. Create untracked work (always create PHRs)
4. Ignore constitution violations
5. Mix feature and general prompts in same PHR folder

## Benefits of This Alignment

1. **Consistency**: All projects follow same governance
2. **Traceability**: Complete audit trail through PHRs
3. **Scalability**: Templates ensure quality at scale
4. **Clarity**: Constitution rules prevent misalignment
5. **Reusability**: Templates and tools available for all projects
6. **Governance**: Clear decision-making framework

## Support & Documentation

- **AI-Native Reference**: `AI-Native-Development-001-ai-native-docs-chapter/GEMINI.md`
- **Alignment Details**: `ALIGNMENT_SUMMARY.md` (root)
- **This Reference**: `QUICK_REFERENCE.md` (root)
- **Project Templates**: `.specify/templates/` in each project
- **Constitution**: `.specify/memory/constitution.md` in each project

---

**All projects are now strictly aligned to the SDD governance model.**
