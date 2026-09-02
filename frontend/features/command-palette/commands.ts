import React from "react";
import { Code2, Briefcase, User, Sparkles, Brain, Target } from "lucide-react"

interface Command {
    value: string
    label: string
    description: string
    icon: React.ComponentType<{ className?: string }>
}

export const COMMANDS: Command[] = [
    {
        value: "Who is Noureddine Bouderbala?",
        label: "Who is Noureddine Bouderbala?",
        description: "Learn about my background and profile",
        icon: User,
    },
    {
        value: "What is Noureddine's tech stack?",
        label: "What is Noureddine's tech stack?",
        description: "Explore my technical skills and tools",
        icon: Briefcase,
    },
    {
        value: "Tell me about his AI and ML experience.",
        label: "Tell me about his AI and ML experience.",
        description: "Discover my AI and machine learning work",
        icon: Brain,
    },
    {
        value: "What projects has Noureddine built?",
        label: "What projects has Noureddine built?",
        description: "Browse my software and AI projects",
        icon: Code2,
    },
    {
        value: "What professional experience does he have?",
        label: "What professional experience does he have?",
        description: "Review my internships and freelance work",
        icon: Sparkles,
    },
    {
        value: "What kind of work is Noureddine looking for?",
        label: "What kind of work is Noureddine looking for?",
        description: "Learn about my career interests and goals",
        icon: Target,
    },
]
