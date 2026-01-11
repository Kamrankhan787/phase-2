"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { LogOut, Home } from "lucide-react";

export function Navbar() {
    const { user, logout } = useAuth();

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-gray-200 dark:border-white/5 shadow-sm transition-all duration-300">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <div className="flex items-center">
                        <Link href="/" className="flex items-center gap-2 group">
                            <div className="p-2 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
                                <Home className="w-5 h-5 text-blue-600" />
                            </div>
                            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                                Evolution of Todo
                            </span>
                        </Link>
                    </div>

                    <div className="flex items-center gap-4">
                        {user && (
                            <div className="hidden md:flex flex-col items-end">
                                <span className="text-xs text-gray-400 font-medium uppercase tracking-wider">Signed in as</span>
                                <span className="text-sm font-semibold text-gray-700">{user.email}</span>
                            </div>
                        )}

                        {user ? (
                            <button
                                onClick={logout}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-50 text-gray-700 font-medium hover:bg-red-50 hover:text-red-600 transition-all border border-gray-200 hover:border-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-200"
                            >
                                <LogOut className="w-4 h-4" />
                                <span>Sign Out</span>
                            </button>
                        ) : (
                            <div className="flex items-center gap-3">
                                <Link
                                    href="/auth/signin"
                                    className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors"
                                >
                                    Sign In
                                </Link>
                                <Link
                                    href="/auth/signup"
                                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-all shadow-md hover:shadow-lg shadow-blue-500/20"
                                >
                                    Get Started
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}
