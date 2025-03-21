# Cline Setup

Reference: https://docs.cline.bot/getting-started/getting-started-new-coders/our-favorite-tech-stack#getting-started

1. For a better view, use "Cline: Open In New Tab"
2. Setup Memory bank
    - Add [custom instructions template](https://docs.cline.bot/improving-your-prompting-skills/custom-instructions-library/cline-memory-bank#custom-instructions-copy-this)
    - Update custom instructions
        -   Enforcing Coding Style and Best Practices: Ensure Cline always adheres to your team's coding conventions, naming conventions, and best practices.
        -   Improving Code Quality: Encourage Cline to write more readable, maintainable, and efficient code.
        -   Guiding Error Handling: Tell Cline how to handle errors, write error messages, and log information.

    - Create `cline_docs` folder in root
    - Update `cline_docs/projectBrief.md` template
    - Create `memory-bank` folder in root
    - Tell Cline to "initialize memory bank"
3. Add `.clinerules` file which contains project specific instructions. Custom instructions are global (applying across all projects).
    For more sophisticated rule organization, cline can read clinerules folder structure:
    ```
    your-project/
    ├── .clinerules/              # Folder containing active rules
    │   ├── 01-coding.md          # Core coding standards
    │   ├── 02-documentation.md   # Documentation requirements
    │   └── current-sprint.md     # Rules specific to current work
    ├── src/
    └── ...
    ```
4. Remember Key Commands
    - "follow your custom instructions" - starting a task, this will instruct Cline to read the context files and continue where he left off
    - "initialize memory bank" - Start fresh
    - "update memory bank" - Full documentation review
    - Toggle Plan/Act modes as needed
5. Use Deepseek R1 for planning, Sonnet for coding. Check Model Selection guide for reference.
6. **IMPORTANT**: Review Prompt Examples: https://docs.cline.bot/improving-your-prompting-skills/prompting#prompt-examples
7. (Optional) Setup `.clineignore` file to tell cline to ignore files and directories. [Example](https://docs.cline.bot/improving-your-prompting-skills/prompting#example-.clineignore-file)


## Documentation Flow
- projectbrief.md is your foundation
- activeContext.md changes most often
- progress.md tracks milestones
- .clinerules captures learning

## .clinerules Template

```
# Project Configuration

## Tech Stack
- Next.js 14+ with App Router
- Tailwind CSS for styling
- Supabase for backend
- Vercel for deployment
- GitHub for version control

## Project Structure
/src
  /app         # Next.js App Router pages
  /components  # React components
  /lib         # Utility functions
  /types       # TypeScript types
/supabase
  /migrations  # SQL migration files
  /seed        # Seed data files
/public        # Static assets

## Database Migrations
SQL files in /supabase/migrations should:
- Use sequential numbering: 001, 002, etc.
- Include descriptive names
- Be reviewed by Cline before execution
Example: 001_create_users_table.sql

## Development Workflow
- Cline helps write and review code changes
- Vercel automatically deploys from main branch
- Database migrations reviewed by Cline before execution

## Security
DO NOT read or modify:
- .env files
- **/config/secrets.*
- Any file containing API keys or credentials
```

## [Model Selection](https://docs.cline.bot/getting-started/model-selection-guide)

| Model             | Input Cost (per 1M tokens) | Output Cost (per 1M tokens) | Best For                       | Best Mode |
|-------------------|----------------------------|-----------------------------|--------------------------------|-----------|
| Claude 3.5 Sonnet | $3.00                      | $15.00                      | Production apps, complex tasks | Acting (coding) |
| DeepSeek R1       | $1.00                      | $3.00                       | Budget-conscious production    | Planning        |

## Let Cline install everything

`Hello Cline! I need help setting up my Mac for software development. Could you please help me install the essential development tools like Homebrew, Node.js, Git, Python, and any other utilities that are commonly needed for coding? I'd like you to guide me through the process step-by-step, explaining what each tool does and making sure everything is installed correctly.`

## Task-specific context (alternative to Memory bank)
- Created for specific implementation tasks
- Document requirements, constraints, and decisions
- Example:
```
# auth-system-implementation.md

## Requirements
- OAuth2 implementation
- Support for Google and GitHub
- Rate limiting on auth endpoints

## Technical Decisions
- Using Passport.js for provider integration
- JWT for session management
- Redis for rate limiting
```

## Using a rule bank

```
your-project/
├── .clinerules/              # Active rules - automatically applied
│   ├── 01-coding.md
│   └── client-a.md
│
├── clinerules-bank/          # Repository of available but inactive rules
│   ├── clients/              # Client-specific rule sets
│   │   ├── client-a.md
│   │   └── client-b.md
│   ├── frameworks/           # Framework-specific rules
│   │   ├── react.md
│   │   └── vue.md
│   └── project-types/        # Project type standards
│       ├── api-service.md
│       └── frontend-app.md
└── ...
```


## MCP
- memory-server
- filesystem?