"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { API_URL } from "@/lib/api";
import { UserPlus, Mail, Lock, ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";

export default function SignUp() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const res = await fetch(`${API_URL}/auth/signup`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || "Failed to create account");
            }

            // Automatically redirect to login after success
            router.push("/auth/signin");
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-purple-50 to-pink-100">
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute -bottom-[20%] -left-[10%] w-[70%] h-[70%] rounded-full bg-blue-200/30 blur-3xl" />
                <div className="absolute top-[10%] -right-[10%] w-[50%] h-[50%] rounded-full bg-purple-200/30 blur-3xl" />
            </div>

            <div className="relative w-full max-w-md bg-white/70 backdrop-blur-xl border border-white/50 rounded-2xl shadow-2xl p-8 transform transition-all hover:scale-[1.01]">
                <div className="flex flex-col items-center mb-8">
                    <div className="p-3 bg-purple-600 rounded-xl shadow-lg mb-4">
                        <UserPlus className="w-8 h-8 text-white" />
                    </div>
                    <h1 className="text-3xl font-bold text-gray-900">Create Account</h1>
                    <p className="text-gray-500 mt-2">Join Evolution of Todo today</p>
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
                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" />
                            <input
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 bg-gray-50/50 border border-gray-200 rounded-xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 outline-none transition-all"
                                placeholder="you@example.com"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-gray-700 ml-1">Password</label>
                        <div className="relative group">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" />
                            <input
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 bg-gray-50/50 border border-gray-200 rounded-xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 outline-none transition-all"
                                placeholder="••••••••"
                                minLength={6}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3.5 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl shadow-lg shadow-purple-500/30 flex items-center justify-center gap-2 transition-all hover:translate-y-[-1px] active:translate-y-[1px] disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        {loading ? (
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                Create Account
                                <ArrowRight className="w-5 h-5" />
                            </>
                        )}
                    </button>
                </form>

                <p className="mt-8 text-center text-sm text-gray-600">
                    Already have an account?{" "}
                    <Link href="/auth/signin" className="font-semibold text-purple-600 hover:text-purple-700 hover:underline">
                        Sign In
                    </Link>
                </p>
            </div>
        </div>
    );
}
