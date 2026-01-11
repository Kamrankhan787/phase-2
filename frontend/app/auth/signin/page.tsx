"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { API_URL } from "@/lib/api";
import { LogIn, Mail, Lock, ArrowRight, AlertCircle } from "lucide-react";

export default function SignIn() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const formData = new URLSearchParams();
            formData.append("username", email);
            formData.append("password", password);

            const fetchUrl = `${API_URL}/auth/signin`;
            console.log("Attempting sign-in fetch to:", fetchUrl);

            const res = await fetch(fetchUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: formData,
            });

            const data = await res.json();

            if (!res.ok) {
                setError(`Server Error (${res.status}): ${data.detail || "Incorrect email or password"}`);
                return;
            }

            login(data.access_token, email);
        } catch (err: any) {
            console.error("Sign-in error details:", err);
            if (err.message === "Failed to fetch") {
                setError(`Network Error: Cannot connect to the backend at ${API_URL}. Please ensure the server is running on port 8000.`);
            } else {
                setError(err.message || "An unexpected error occurred.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-blue-50 to-indigo-100">
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute -top-[30%] -left-[10%] w-[70%] h-[70%] rounded-full bg-purple-200/30 blur-3xl" />
                <div className="absolute top-[40%] -right-[10%] w-[60%] h-[60%] rounded-full bg-blue-200/30 blur-3xl" />
            </div>

            <div className="relative w-full max-w-md bg-white/70 backdrop-blur-xl border border-white/50 rounded-2xl shadow-2xl p-8 transform transition-all hover:scale-[1.01]">
                <div className="flex flex-col items-center mb-8">
                    <div className="p-3 bg-blue-600 rounded-xl shadow-lg mb-4">
                        <LogIn className="w-8 h-8 text-white" />
                    </div>
                    <h1 className="text-3xl font-bold text-gray-900">Welcome Back</h1>
                    <p className="text-gray-500 mt-2">Sign in to continue your journey</p>
                    <span className="text-[10px] text-gray-400 mt-1 opacity-50">Build: 2026-01-11-REV4</span>
                </div>

                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-100 rounded-xl flex items-center gap-3 text-red-600 animate-pulse">
                        <AlertCircle className="w-5 h-5 flex-shrink-0" />
                        <span className="text-sm font-medium">{error}</span>
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-gray-700 ml-1">Email</label>
                        <div className="relative group">
                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                            <input
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 bg-gray-50/50 border border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
                                placeholder="you@example.com"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-gray-700 ml-1">Password</label>
                        <div className="relative group">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                            <input
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 bg-gray-50/50 border border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
                                placeholder="••••••••"
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg shadow-blue-500/30 flex items-center justify-center gap-2 transition-all hover:translate-y-[-1px] active:translate-y-[1px] disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        {loading ? (
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                Sign In
                                <ArrowRight className="w-5 h-5" />
                            </>
                        )}
                    </button>
                </form>

                <p className="mt-8 text-center text-sm text-gray-600">
                    Don't have an account?{" "}
                    <Link href="/auth/signup" className="font-semibold text-blue-600 hover:text-blue-700 hover:underline">
                        Create Account
                    </Link>
                </p>
            </div>
        </div>
    );
}
