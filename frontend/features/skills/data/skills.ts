import { Code2, Database, Wrench, Layers, Brain, Palette } from "lucide-react"

export const skills = [
    {
        category: "Programming Languages",
        icon: Code2,
        color: "from-slate-400 to-slate-500",
        items: [
            { name: "JavaScript" },
            { name: "TypeScript" },
            { name: "Python" },
            { name: "C" },
            { name: "C++" },
            { name: "SQL" },
        ],
    },
    {
        category: "Frontend & Web",
        icon: Layers,
        color: "from-zinc-400 to-zinc-500",
        items: [
            { name: "Next.js" },
            { name: "Nuxt.js" },
            { name: "React" },
            { name: "TypeScript" },
            { name: "Tailwind CSS" },
            { name: "EJS" },
        ],
    },
    {
        category: "Backend",
        icon: Wrench,
        color: "from-neutral-400 to-neutral-500",
        items: [
            { name: "Node.js" },
            { name: "Express.js" },
            { name: "REST APIs" },
            { name: "Flask" },
        ],
    },
    {
        category: "Databases",
        icon: Database,
        color: "from-gray-400 to-gray-500",
        items: [
            { name: "PostgreSQL" },
            { name: "MySQL" },
            { name: "MongoDB" },
            { name: "Prisma" },
            { name: "Supabase" },
        ],
    },
    {
        category: "AI & Machine Learning",
        icon: Brain,
        color: "from-indigo-400 to-indigo-500",
        items: [
            { name: "Machine Learning" },
            { name: "OpenAI Whisper" },
            { name: "Hugging Face" },
            { name: "PyTorch" },
            { name: "LoRA" },
            { name: "LangChain" },
            { name: "Vector Databases" },
        ],
    },
    {
        category: "DevOps & Tools",
        icon: Wrench,
        color: "from-stone-400 to-stone-500",
        items: [
            { name: "Docker" },
            { name: "CI/CD" },
            { name: "Git" },
            { name: "GitHub" },
        ],
    },
    {
        category: "Creative & Design",
        icon: Palette,
        color: "from-purple-400 to-purple-500",
        items: [
            { name: "Adobe Premiere Pro" },
            { name: "Adobe After Effects" },
            { name: "DaVinci Resolve" },
            { name: "CapCut" },
            { name: "Figma" },
        ],
    },
]
