import type { ProjectItem } from "@/features/projects/components/projects-carousel";

export const projects: ProjectItem[] = [
    {
        id: 1,
        title: "Smart Recitation Tracker",
        category: "AI / Speech Recognition",
        image: "/projects/smart-recitation-tracker.png",
        description:
            "An intelligent application that uses ASR to convert Quran recitation into text, compare it against reference text, identify errors, and generate review reports.",
        techStack: ["Vosk", "Speech Recognition", "Arabic Speech Processing", "Quranic Text Processing"],
    },
    {
        id: 2,
        title: "Wonderlust",
        category: "AI-powered Travel Platform",
        image: "/projects/wonderlust.png",
        description:
            "An integrated web and mobile travel platform for trip planning, AI-powered recommendations, and secure booking management.",
        techStack: ["React", "Node.js", "MongoDB", "Flask"],
    },
    {
        id: 3,
        title: "KibbleDrop",
        category: "Full-stack SaaS / E-commerce",
        image: "/projects/kibbledrop.png",
        description:
            "A modern platform for managing pet food subscriptions with authentication, payments, and database-driven architecture.",
        techStack: ["Next.js", "Prisma", "PostgreSQL", "Stripe", "Tailwind CSS", "shadcn/ui"],
    },
    {
        id: 4,
        title: "Athar Baqi",
        category: "Full-stack Web Platform",
        image: "/projects/athar-baqi.png",
        description:
            "A digital platform for Quran learning and Islamic content publishing with a modern responsive interface and content management.",
        techStack: ["Next.js", "TypeScript"],
    },
    {
        id: 5,
        title: "PLUAE",
        category: "University Job Platform",
        image: "/projects/pluae.png",
        description:
            "A responsive university job platform connecting students and companies with multi-role dashboards and secure authentication.",
        techStack: ["Next.js", "TypeScript", "Tailwind CSS", "PostgreSQL"],
    },
];
