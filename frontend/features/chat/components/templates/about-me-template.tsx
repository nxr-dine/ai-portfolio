"use client"

import { motion } from "framer-motion"
import { useCallback, useEffect, useState } from "react"
import Image from "next/image"
import { StreamingText } from "./streaming-text"
import { useChatContext } from "@/features/chat/context/chat-context"
import { siteConfig } from "@/lib/config"
import type { Message } from "@/lib/types"

const SECTIONS = [
    {
        html: `Hi there! 👋 I'm **Noureddine Bouderbala**, a **Software Engineer** and **Full-Stack Developer** currently in my third year at **ESTIN** (Higher School of Computer Science and Digital Technologies) in Algeria.`
    },
    {
        html: `I combine software engineering with **AI/ML**, building modern web applications and AI-powered solutions. My hands-on experience spans full-stack freelance development, network & systems internship, ERP internship, and AI/ML training on speech recognition projects.`
    },
    {
        html: `Technically, I work with **Next.js**, **React**, **TypeScript**, **Node.js**, **Python**, **PostgreSQL**, **MongoDB**, and **Prisma** for full-stack development. On the AI side, I've worked with **Whisper fine-tuning**, **Hugging Face**, **PyTorch**, and **LoRA** for Quran recitation speech recognition.`
    },
    {
        html: `I'm interested in **full-stack development**, **AI engineering**, **machine learning**, **SaaS applications**, and **software engineering internships**. I'm always open to collaborative projects and junior developer opportunities.`
    },
    {
        html: `Outside of code, I'm into **submission grappling**, **calisthenics**, and **video editing** — where I've built a personal audience of 50K+ followers and 1.5M+ organic views.`,
        isItalic: true
    }
]

interface AboutMeTemplateProps {
    message?: Message
}

export function AboutMeTemplate({ message }: AboutMeTemplateProps) {
    const { scrollToBottom, setIsComponentStreaming } = useChatContext()
    const [isHistorical] = useState(() =>
        message ? (Date.now() - new Date(message.timestamp).getTime() > 3000) : false
    )

    useEffect(() => {
        if (!isHistorical) {
            setIsComponentStreaming(true);
        }
        return () => setIsComponentStreaming(false);
    }, [isHistorical, setIsComponentStreaming]);

    const [currentSection, setCurrentSection] = useState(() => isHistorical ? SECTIONS.length - 1 : 0)

    const handleSectionComplete = useCallback((index: number) => {
        if (index < SECTIONS.length - 1) {
            setCurrentSection(prev => Math.max(prev, index + 1))
        } else {
            setIsComponentStreaming(false);
        }
    }, [setIsComponentStreaming])

    const handleStream = useCallback(() => {
        if (!isHistorical) scrollToBottom('smooth')
    }, [isHistorical, scrollToBottom])

    return (
        <div className="w-full mb-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
            <div className="flex flex-col md:flex-row gap-6 items-start">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5 }}
                    className="w-full md:w-1/3 shrink-0 self-start px-4 md:px-0"
                >
                    <div className="rounded-xl overflow-hidden border border-white/10 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 p-2 md:p-3 shadow-xl">
                        <div className="aspect-[4/3] md:aspect-[4/5] bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-lg overflow-hidden relative">
                            <Image
                                src="/profile.webp"
                                alt={`${siteConfig.name} - Software Engineer`}
                                fill
                                sizes="(max-width: 768px) 100vw, 33vw"
                                className="object-cover"
                                priority
                            />
                        </div>
                    </div>
                </motion.div>

                <div className="w-full md:w-2/3 text-zinc-200 px-4 md:px-0">
                    <div className="space-y-5 leading-7 tracking-wide font-light">
                        {SECTIONS.map((section, index) => {
                            if (index > currentSection) return null
                            return (
                                <div
                                    key={section.html}
                                    className={`mb-5 last:mb-0 ${section.isItalic ? 'text-zinc-400 italic' : ''}`}
                                >
                                    <StreamingText
                                        text={section.html}
                                        delay={index === 0 ? 500 : 0}
                                        speed={8}
                                        onComplete={() => handleSectionComplete(index)}
                                        onStream={handleStream}
                                        instant={isHistorical}
                                    />
                                </div>
                            )
                        })}
                    </div>
                </div>
            </div>
        </div>
    )
}
