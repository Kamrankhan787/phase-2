'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, CheckCircle2, Trash2, Edit3, List } from 'lucide-react';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    tool_calls?: Array<{
        tool: string;
        input: any;
        output: any;
    }>;
}

interface ChatContainerProps {
    userId: string;
}

export default function ChatContainer({ userId }: ChatContainerProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [conversationId, setConversationId] = useState<number | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || loading) return;

        const userMessage: Message = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await fetch(`http://localhost:8000/api/${userId}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    conversation_id: conversationId,
                    message: input,
                }),
            });

            const data = await response.json();

            // Handle HTTP errors with structured error response
            if (!response.ok) {
                const errorDetail = data.detail || data;
                const errorCode = errorDetail.code || 'UNKNOWN_ERROR';
                const errorMessage = errorDetail.message || 'An error occurred';
                const requestId = errorDetail.request_id || 'N/A';

                console.error(`[${requestId}] Error ${errorCode}: ${errorMessage}`, errorDetail);

                throw new Error(errorMessage);
            }

            // Update conversation ID
            if (!conversationId) setConversationId(data.conversation_id);

            // Add assistant response
            const assistantMessage: Message = {
                role: 'assistant',
                content: data.response,
                tool_calls: data.tool_calls,
            };
            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error: any) {
            console.error('Chat error:', error);

            // Display specific error message
            const errorMessage = error.message || 'Network error. Please check your connection and try again.';

            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: `❌ Error: ${errorMessage}`,
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Header */}
            <div className="bg-black/30 backdrop-blur-lg border-b border-white/10 p-6">
                <h1 className="text-3xl font-bold text-white">AI Todo Assistant</h1>
                <p className="text-purple-300 text-sm mt-1">
                    Manage your tasks with natural language
                </p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.length === 0 && (
                    <div className="text-center text-white/60 mt-20">
                        <p className="text-lg mb-4">👋 Hi! I'm your AI todo assistant.</p>
                        <p className="text-sm">Try saying:</p>
                        <ul className="text-sm mt-2 space-y-1">
                            <li>"Add a task to buy groceries"</li>
                            <li>"Show me all my tasks"</li>
                            <li>"Mark task 1 as complete"</li>
                        </ul>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <MessageBubble key={idx} message={msg} />
                ))}

                {loading && (
                    <div className="flex items-center gap-2 text-purple-300">
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span className="text-sm">Thinking...</span>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="bg-black/30 backdrop-blur-lg border-t border-white/10 p-6">
                <div className="flex gap-3">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your message..."
                        className="flex-1 bg-white/10 text-white placeholder-white/40 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
                        disabled={loading}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={loading || !input.trim()}
                        className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>
            </div>
        </div>
    );
}

function MessageBubble({ message }: { message: Message }) {
    const isUser = message.role === 'user';

    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div
                className={`max-w-2xl rounded-2xl px-5 py-3 ${isUser
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                    : 'bg-white/10 backdrop-blur-lg text-white border border-white/20'
                    }`}
            >
                <p className="whitespace-pre-wrap">{message.content}</p>

                {/* Tool Calls Display */}
                {message.tool_calls && message.tool_calls.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-white/20 space-y-2">
                        {message.tool_calls.map((call, idx) => (
                            <ToolCallDisplay key={idx} toolCall={call} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

function ToolCallDisplay({ toolCall }: { toolCall: any }) {
    const icons: Record<string, any> = {
        add_task: CheckCircle2,
        list_tasks: List,
        complete_task: CheckCircle2,
        delete_task: Trash2,
        update_task: Edit3,
    };

    const Icon = icons[toolCall.tool] || CheckCircle2;

    return (
        <div className="flex items-start gap-2 text-xs bg-black/20 rounded-lg p-2">
            <Icon className="w-4 h-4 text-green-400 mt-0.5" />
            <div>
                <p className="font-semibold text-green-400">{toolCall.tool}</p>
                <p className="text-white/60 mt-1">
                    {toolCall.output.status || 'executed'}
                </p>
            </div>
        </div>
    );
}
