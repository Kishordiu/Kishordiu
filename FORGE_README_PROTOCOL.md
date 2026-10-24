# The F.O.R.G.E. README Protocol

*A material-first, proof-led way to document software projects.*

A repository README is often the first interface a visitor experiences. It should make the project feel distinctive, explain how it works, and give a reader enough evidence to decide whether to explore the source. The F.O.R.G.E. Protocol is a documentation method developed for the DIU Foundry project portfolio to keep those goals together without turning every repository into the same template.

## F — Form

Give the project its own visual language before asking the reader to scan paragraphs.

- Use a project-specific hero image or a carefully designed SVG, with meaningful alt text.
- Choose a material, shape language, and motif that belongs to the domain: machined metal and network geometry for connected systems, route contours for mobility, optical forms for image tools, or softer materials for human-centred products.
- Keep the shared studio signature subtle. A consistent family should not mean identical artwork.
- Prefer committed, repository-relative assets over fragile third-party banner generators.

## O — Objective

State the product's job in one direct sentence. Describe the problem the project is trying to solve, who the interface serves, and what makes the approach useful. Avoid adjective stacks that could describe any application.

## R — Route

Make the mechanism visible. A short data-flow diagram, workflow, or repository map should show how a user input moves through the UI, state layer, API, database, model, or external service. Only include layers that exist or clearly label planned parts.

## G — Ground truth

Write the difference between implementation and aspiration into the document.

- **Implemented:** point to a source path, configured service, or reproducible command when it matters.
- **Simulated:** label seeded data, scripted outcomes, and placeholder analysis as demonstrations.
- **Planned:** describe the intended future without phrasing it as a working feature.
- **Boundary:** state the most important limitations, safety considerations, external dependencies, and validation still required.

The goal is not to make prototypes sound smaller. It is to make their actual work credible and reviewable. A polished concept can be ambitious while remaining honest about what has and has not been validated.

## E — Execute

Give the reader a reliable next action.

- Name the required runtime and package manager.
- Use commands that exist in `package.json` or the project's documented toolchain.
- Explain the necessary environment variables without exposing secret values.
- Separate build/lint/test commands and do not claim checks passed unless they were actually run.
- State when a backend, provider, hardware device, or browser permission is required.

## Quality gate

Before publishing a README, check:

- [ ] The hero image path resolves from the repository root.
- [ ] The project name and purpose are obvious in the first screen.
- [ ] The diagram follows the real code path rather than an imagined architecture.
- [ ] External providers, live data, security properties, performance figures, and clinical/legal claims have evidence or are labelled as aspirations.
- [ ] The setup steps match the actual package scripts and directory structure.
- [ ] Images have useful alt text and the content remains readable without decorative badges.
- [ ] The README is specific to this project; removing the project name should not make it interchangeable with another repository.

## The principle

**Make the craft visible. Make the mechanism legible. Make the claims earn their place.**

F.O.R.G.E. is a working standard for these repositories, not a claim that README styling proves software quality. The code, tests, deployment, security posture, and real-world validation remain separate things that must be checked on their own.
