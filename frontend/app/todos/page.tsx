"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { API_URL } from "@/lib/api";
import { Navbar } from "@/components/Navbar";
import { Plus, Trash2, CheckCircle, Circle, Calendar, Layout, Loader2 } from "lucide-react";

interface Todo {
    id: string;
    title: string;
    completed: boolean;
    created_at: string;
}

export default function TodosPage() {
    const { user, token, isLoading } = useAuth();
    const router = useRouter();
    const [todos, setTodos] = useState<Todo[]>([]);
    const [newTodo, setNewTodo] = useState("");
    const [loading, setLoading] = useState(true);
    const [adding, setAdding] = useState(false);

    useEffect(() => {
        if (!isLoading && !user) {
            router.push("/auth/signin");
        } else if (user && token) {
            fetchTodos();
        }
    }, [user, isLoading, token, router]);

    const fetchTodos = async () => {
        try {
            const res = await fetch(`${API_URL}/todos/`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (res.ok) {
                const data = await res.json();
                setTodos(data);
            }
        } catch (error) {
            console.error("Failed to fetch todos", error);
        } finally {
            setLoading(false);
        }
    };

    const addTodo = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTodo.trim()) return;
        setAdding(true);

        try {
            const res = await fetch(`${API_URL}/todos/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ title: newTodo, completed: false }),
            });

            if (res.ok) {
                const todo = await res.json();
                setTodos([...todos, todo]);
                setNewTodo("");
            }
        } catch (error) {
            console.error("Failed to add todo", error);
        } finally {
            setAdding(false);
        }
    };

    const toggleTodo = async (id: string, currentStatus: boolean) => {
        // Optimistic update
        setTodos(todos.map(t => t.id === id ? { ...t, completed: !currentStatus } : t));

        try {
            await fetch(`${API_URL}/todos/${id}/toggle`, {
                method: "PATCH",
                headers: { Authorization: `Bearer ${token}` },
            });
        } catch (error) {
            // Revert if failed
            setTodos(todos.map(t => t.id === id ? { ...t, completed: currentStatus } : t));
        }
    };

    const deleteTodo = async (id: string) => {
        // Optimistic update
        const previousTodos = [...todos];
        setTodos(todos.filter(t => t.id !== id));

        try {
            await fetch(`${API_URL}/todos/${id}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${token}` },
            });
        } catch (error) {
            // Revert if failed
            setTodos(previousTodos);
        }
    };

    if (isLoading || loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 pb-20">
            <Navbar />

            <main className="pt-28 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                        <Layout className="w-8 h-8 text-blue-600" />
                        My Tasks
                    </h1>
                    <p className="text-gray-500 mt-2">Manage your daily goals effectively.</p>
                </header>

                {/* Add Todo Input */}
                <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-2 mb-8 focus-within:ring-4 focus-within:ring-blue-100 transition-all duration-300">
                    <form onSubmit={addTodo} className="flex gap-2">
                        <input
                            type="text"
                            value={newTodo}
                            onChange={(e) => setNewTodo(e.target.value)}
                            placeholder="What needs to be done?"
                            className="flex-1 px-4 py-3 bg-transparent text-gray-800 placeholder-gray-400 focus:outline-none text-lg"
                        />
                        <button
                            type="submit"
                            disabled={adding || !newTodo.trim()}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 hover:shadow-lg hover:shadow-blue-500/20 disabled:opacity-70 disabled:cursor-not-allowed"
                        >
                            {adding ? <Loader2 className="w-5 h-5 animate-spin" /> : <Plus className="w-5 h-5" />}
                            <span className="hidden sm:inline">Add Task</span>
                        </button>
                    </form>
                </div>

                {/* Todo List */}
                <div className="space-y-4">
                    {todos.length === 0 ? (
                        <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200">
                            <div className="bg-blue-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <CheckCircle className="w-8 h-8 text-blue-500" />
                            </div>
                            <h3 className="text-lg font-medium text-gray-900">All caught up!</h3>
                            <p className="text-gray-500">You have no tasks on your list.</p>
                        </div>
                    ) : (
                        todos.map((todo) => (
                            <div
                                key={todo.id}
                                className={`group flex items-center justify-between p-5 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-200 ${todo.completed ? 'opacity-75 bg-gray-50/50' : ''}`}
                            >
                                <div className="flex items-center gap-4 flex-1">
                                    <button
                                        onClick={() => toggleTodo(todo.id, todo.completed)}
                                        className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${todo.completed
                                                ? "bg-green-500 border-green-500 text-white"
                                                : "border-gray-300 text-transparent hover:border-blue-500"
                                            }`}
                                    >
                                        <CheckCircle className="w-4 h-4" />
                                    </button>
                                    <span className={`text-lg transition-all ${todo.completed ? "text-gray-400 line-through" : "text-gray-700"}`}>
                                        {todo.title}
                                    </span>
                                </div>

                                <div className="flex items-center gap-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <span className="text-xs text-gray-400 flex items-center gap-1">
                                        <Calendar className="w-3 h-3" />
                                        {new Date(todo.created_at).toLocaleDateString()}
                                    </span>
                                    <button
                                        onClick={() => deleteTodo(todo.id)}
                                        className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                        title="Delete task"
                                    >
                                        <Trash2 className="w-5 h-5" />
                                    </button>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </main>
        </div>
    );
}
